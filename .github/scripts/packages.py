#!/usr/bin/env python3
"""Package inventory, safe upstream discovery, and narrowly scoped spec updates."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

import rpm
import yaml

ROOT = Path(__file__).resolve().parents[2]
NAME = r"[a-z0-9][a-z0-9+_.-]*"
VERSION = r"[0-9][A-Za-z0-9.+~^]*"
TAG = r"v?[0-9][A-Za-z0-9.+~^]*"


def inventory():
    data = yaml.safe_load((ROOT / 'packages.yml').read_text())
    packages = data['packages']
    names = set()
    for package in packages:
        name = package['name']
        if not re.fullmatch(NAME, name) or name in names:
            raise ValueError(f'Invalid or duplicate package: {name!r}')
        names.add(name)
        if package['spec_dir'] != name or not (ROOT / name / f'{name}.spec').is_file():
            raise ValueError(f'Invalid spec directory for {name}')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', package['repo']):
            raise ValueError(f'Invalid upstream repository for {name}')
    actual = {p.parent.name for p in ROOT.glob('*/*.spec')}
    if actual != names:
        raise ValueError(f'Inventory/spec mismatch: {actual ^ names}')
    return packages


def output(values):
    for key, value in values.items():
        text = str(value).lower() if isinstance(value, bool) else str(value)
        if '\n' in text or '\r' in text:
            raise ValueError('Multiline workflow output rejected')
        print(f'{key}={text}')
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
                stream.write(f'{key}={text}\n')


def api(repo, endpoint, allow_missing=False):
    request = urllib.request.Request(
        f'https://api.github.com/repos/{repo}/{endpoint}',
        headers={'Accept': 'application/vnd.github+json',
                 'Authorization': f'Bearer {os.environ["GH_TOKEN"]}',
                 'User-Agent': 'wayland-wm-extras-updater'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if allow_missing and error.code == 404:
            return None
        raise


def field(text, name):
    match = re.search(rf'^{re.escape(name)}:\s*(\S+)', text, re.M)
    if not match:
        raise ValueError(f'Missing {name}')
    return match[1]


def newer(candidate, current):
    return rpm.labelCompare(('0', candidate, '0'), ('0', current, '0')) > 0


def update_spec(path, version, tag, mode='release', force=False):
    if not re.fullmatch(VERSION, version):
        raise ValueError(f'Unsupported RPM version: {version!r}')
    pattern = r'[0-9a-f]{40}' if mode == 'commit' else TAG
    if not re.fullmatch(pattern, tag):
        raise ValueError(f'Unsupported upstream reference: {tag!r}')
    text = path.read_text()
    current = field(text, 'Version')
    if not re.fullmatch(VERSION, current):
        raise ValueError('Version must be a literal RPM version')
    if version != current and not newer(version, current):
        raise ValueError(f'Refusing downgrade: {current} -> {version}')
    if version == current and not force:
        return False
    release = 1
    if version == current:
        match = re.fullmatch(r'(\d+)%\{\?dist\}', field(text, 'Release'))
        if not match:
            raise ValueError('Cannot increment nonstandard Release')
        release = int(match[1]) + 1
    text = re.sub(r'^Version:.*$', f'Version:        {version}', text, flags=re.M)
    text = re.sub(r'^Release:.*$', f'Release:        {release}%{{?dist}}', text, flags=re.M)
    if mode == 'commit':
        for key, value in [('commit', tag), ('shortcommit', tag[:7])]:
            line = f'%global {key} {value}'
            if re.search(rf'^%global {key} .*$', text, re.M):
                text = re.sub(rf'^%global {key} .*$', line, text, flags=re.M)
            else:
                text = line + '\n' + text
    else:
        # Forge macros consume an explicit tag, including the upstream v prefix.
        if '%{forgesource}' in text:
            line = f'%global tag {tag}'
            if re.search(r'^%global tag .*$', text, re.M):
                text = re.sub(r'^%global tag .*$', line, text, flags=re.M)
            else:
                text = line + '\n' + text
        # Direct macro-based source URLs already follow Version; never rewrite paths.
    if '%changelog\n' not in text:
        raise ValueError('Missing changelog')
    date = dt.datetime.now(dt.timezone.utc).strftime('%a %b %d %Y')
    entry = (f'%changelog\n* {date} Automated Update <noreply@github.com> - '
             f'{version}-{release}\n- {"Rebuild" if version == current else "Update to"} {version}\n\n')
    text = text.replace('%changelog\n', entry, 1)
    path.write_text(text)
    return True


def discover(package, force):
    if package.get('update', True) is False:
        raise ValueError(f'{package["name"]} is maintained manually')
    path = ROOT / package['spec_dir'] / (package['name'] + '.spec')
    text = path.read_text()
    current = field(text, 'Version')
    repo = package['repo']
    branch = package.get('track')
    if branch:
        commit = api(repo, 'commits/' + urllib.parse.quote(branch, safe=''))
        tag = commit['sha']
        if not re.fullmatch(r'[0-9a-f]{40}', tag):
            raise ValueError('Invalid commit SHA')
        old = re.search(r'^%global commit (\S+)', text, re.M)
        if old and old[1] == tag:
            version = current
        else:
            # Keep the release base stable; timestamp snapshots have RPM ordering.
            stamp = dt.datetime.fromisoformat(commit['commit']['committer']['date'].replace('Z', '+00:00'))
            version = current.split('^')[0] + '^' + stamp.strftime('%Y%m%d%H%M%S') + '.git' + tag[:7]
        mode = 'commit'
    else:
        release = api(repo, 'releases/latest', allow_missing=True)
        if release is not None:
            tag = release['tag_name']
        else:
            tags = api(repo, 'tags?per_page=100')
            stable = [item['name'] for item in tags if re.fullmatch(r'v?[0-9]+(?:\.[0-9]+)*', item['name'])]
            if not stable:
                raise ValueError('No stable release/tag found')
            tag = stable[0]
            for candidate in stable[1:]:
                if newer(candidate.removeprefix('v'), tag.removeprefix('v')):
                    tag = candidate
        if not re.fullmatch(TAG, tag):
            raise ValueError(f'Unsupported upstream tag: {tag!r}')
        version = tag.removeprefix('v')
        mode = 'release'
    if version != current and not newer(version, current):
        print(f'Skipping older upstream version {version}; current is {current}')
        output({'changed': False})
        return
    changed = update_spec(path, version, tag, mode, force)
    output({'changed': changed, 'version': version, 'previous': current})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['matrix', 'names', 'update', 'changed', 'validate'])
    parser.add_argument('package', nargs='?')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--base')
    args = parser.parse_args()
    packages = inventory()
    if args.command == 'matrix':
        output({'matrix': json.dumps([p for p in packages if p.get('update', True)], separators=(',', ':'))})
    elif args.command == 'names':
        print('\n'.join(p['name'] for p in packages))
    elif args.command == 'changed':
        paths = subprocess.check_output(['git', 'diff', '--name-only', args.base, 'HEAD'], text=True).splitlines()
        global_change = any(p.startswith(('.github/', 'tests/')) or p in ('justfile', 'packages.yml') for p in paths)
        selected = [p['name'] for p in packages if global_change or any(f.startswith(p['spec_dir'] + '/') for f in paths)]
        output({'matrix': json.dumps(selected), 'any': bool(selected)})
    elif args.command == 'update':
        matches = [p for p in packages if p['name'] == args.package]
        if not matches:
            parser.error('Unknown package; use names to list the inventory')
        discover(matches[0], args.force)


if __name__ == '__main__':
    main()
