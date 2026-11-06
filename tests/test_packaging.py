import importlib.util
import json
import os
import re
import shutil
import urllib.error
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / '.github/scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packages = load('packages')
sources = load('sources')


class Updates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'package.spec'

    def copy(self, name):
        self.path.write_text((ROOT / name / f'{name}.spec').read_text())

    def snapshot(self):
        # Synthetic snapshot fixture keeps updater coverage independent of inventory.
        self.path.write_text(
            '%global commit f2aa9fe01103d7600553b505b298ff0bd47ff280\n'
            '%global shortcommit f2aa9fe\n'
            'Name: package\nVersion: 0.5.8^gitf2aa9fe\nRelease: 1%{?dist}\n'
            '%changelog\n'
        )

    def test_direct_source_url_preserved(self):
        for name in ('waypaper', 'python-screeninfo', 'python-imageio-ffmpeg', 'nerd-fonts-firacode'):
            with self.subTest(name=name):
                self.copy(name)
                source = packages.field(self.path.read_text(), 'Source0')
                packages.update_spec(self.path, '99.0', 'v99.0')
                self.assertEqual(source, packages.field(self.path.read_text(), 'Source0'))

    def test_forge_exact_tag(self):
        self.copy('walker')
        packages.update_spec(self.path, '99.0', '99.0')
        self.assertIn('%global tag 99.0\n', self.path.read_text())
        parsed = subprocess.check_output(['rpmspec', '-P', str(self.path)], text=True)
        self.assertIn('/archive/99.0/', packages.field(parsed, 'Source0'))

    def test_reject_injection_and_downgrade_without_mutating(self):
        self.copy('waypaper')
        original = self.path.read_text()
        for version, tag in [('2.8', 'v2.8$(id)'), ('2.8\nBAD', '2.8'), ('1.0', '1.0')]:
            with self.assertRaises(ValueError):
                packages.update_spec(self.path, version, tag)
            self.assertEqual(original, self.path.read_text())

    def test_idempotency_and_force_release(self):
        self.copy('waypaper')
        original = self.path.read_text()
        version = packages.field(original, 'Version')
        release = int(packages.field(original, 'Release').split('%')[0]) + 1
        self.assertFalse(packages.update_spec(self.path, version, version))
        self.assertEqual(original, self.path.read_text())
        self.assertTrue(packages.update_spec(self.path, version, version, force=True))
        self.assertEqual(f'{release}%{{?dist}}', packages.field(self.path.read_text(), 'Release'))
        self.assertIn(f'{version}-{release}\n- Rebuild {version}', self.path.read_text())

    def test_commit_snapshot_and_identity(self):
        self.snapshot()
        sha = 'a' * 40
        version = '0.5.8^20261025000000.gitaaaaaaa'
        packages.update_spec(self.path, version, sha, 'commit')
        self.assertIn('%global commit ' + sha, self.path.read_text())
        self.assertTrue(packages.newer(version, '0.5.8^gitf2aa9fe'))
        self.assertFalse(packages.newer('0.5.8^20260101000000.gitbbbbbbb', version))

    def test_inventory_covers_every_spec_and_manual_packages(self):
        data = packages.inventory()
        self.assertEqual({p.parent.name for p in ROOT.glob('*/*.spec')}, {p['name'] for p in data})
        manual = {p['name'] for p in data if not p.get('update', True)}
        self.assertEqual({'gtklock-meta'}, manual)

    def test_missing_changelog_is_atomic(self):
        self.copy('waypaper')
        self.path.write_text(self.path.read_text().split('%changelog')[0])
        original = self.path.read_text()
        with self.assertRaises(ValueError):
            packages.update_spec(self.path, '99.0', '99.0')
        self.assertEqual(original, self.path.read_text())

    def test_unchanged_commit_does_not_rewrite_snapshot_version(self):
        self.snapshot()
        original = self.path.read_text()
        package = {'name': 'package', 'spec_dir': '.', 'repo': 'owner/repo', 'track': 'master'}
        with patch.object(packages, 'ROOT', self.path.parent), patch.object(packages, 'api', return_value={'sha': 'f2aa9fe01103d7600553b505b298ff0bd47ff280'}), patch.object(packages, 'output') as output:
            packages.discover(package, False)
        self.assertEqual(original, self.path.read_text())
        self.assertFalse(output.call_args.args[0]['changed'])

    def test_api_errors_do_not_silently_fall_back(self):
        with patch.dict(os.environ, {'GH_TOKEN': 'test'}):
            for code in (403, 429, 500):
                error = urllib.error.HTTPError('https://api.github.com', code, 'failure', {}, None)
                with patch.object(packages.urllib.request, 'urlopen', side_effect=error):
                    with self.assertRaises(urllib.error.HTTPError):
                        packages.api('owner/repo', 'releases/latest', allow_missing=True)
            error = urllib.error.HTTPError('https://api.github.com', 404, 'missing', {}, None)
            with patch.object(packages.urllib.request, 'urlopen', side_effect=error):
                self.assertIsNone(packages.api('owner/repo', 'releases/latest', allow_missing=True))

    def test_rpm_numeric_order(self):
        self.assertTrue(packages.newer('2.10', '2.9'))
        self.assertFalse(packages.newer('2.9', '2.10'))


class Sources(unittest.TestCase):
    def test_all_sources_and_patches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / 'test.spec'
            spec.touch()
            (root / 'fix.patch').write_text('patch')
            dest = root / 'sources'
            dest.mkdir()
            parsed = 'Source0: https://example.com/one.tar.gz\nSource1: https://example.com/two.cab\nPatch0: fix.patch\n'
            with patch.object(sources.subprocess, 'check_output', return_value=parsed), patch.object(sources.subprocess, 'run') as download:
                sources.stage(spec, dest)
            self.assertEqual(2, download.call_count)
            self.assertEqual('patch', (dest / 'fix.patch').read_text())
            self.assertEqual('https://example.com/two.cab', download.call_args.args[0][-1])

    def test_missing_local_source_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(sources.subprocess, 'check_output', return_value='Source1: missing.conf\n'):
                with self.assertRaises(FileNotFoundError):
                    sources.stage(root / 'test.spec', root)

    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(sources.subprocess, 'check_output', return_value='Patch0: ../outside.patch\n'):
                with self.assertRaises(ValueError):
                    sources.stage(root / 'test.spec', root)


class PullRequests(unittest.TestCase):
    def run_updater(self, number='', lookup_failure=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binaries = root / 'bin'
            binaries.mkdir()
            (binaries / 'git').write_text('#!/bin/sh\nexit 0\n')
            (binaries / 'gh').write_text(
                '#!/usr/bin/env python3\n'
                'import json, os, pathlib, sys\n'
                'args = sys.argv[1:]\n'
                'record = {"args": args}\n'
                'for arg in args:\n'
                '    if arg.startswith("body=@"):\n'
                '        record["body"] = pathlib.Path(arg[6:]).read_text()\n'
                'with open("calls", "a") as stream:\n'
                '    stream.write(json.dumps(record) + "\\n")\n'
                'if args[:3] == ["api", "--method", "GET"]:\n'
                '    if os.environ["LOOKUP_FAILURE"] == "1": sys.exit(1)\n'
                '    print(os.environ["PR_NUMBER"])\n'
            )
            for binary in binaries.iterdir():
                binary.chmod(0o755)
            env = dict(os.environ, PATH=str(binaries) + ':' + os.environ['PATH'],
                       PACKAGE='sample', VERSION='2.0', PREVIOUS='1.0',
                       GITHUB_REPOSITORY='owner/repo', PR_NUMBER=number,
                       LOOKUP_FAILURE=str(int(lookup_failure)))
            result = subprocess.run(['bash', str(ROOT / '.github/scripts/open-update-pr.sh')],
                                    cwd=root, env=env, capture_output=True, text=True)
            calls = [json.loads(line) for line in (root / 'calls').read_text().splitlines()]
            return result, calls

    def test_create_and_edit_use_repository_rest_endpoints(self):
        for number, method, endpoint in [('', 'POST', 'repos/owner/repo/pulls'),
                                         ('42', 'PATCH', 'repos/owner/repo/pulls/42')]:
            with self.subTest(method=method):
                result, calls = self.run_updater(number)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(2, len(calls))
                self.assertEqual(['api', '--method', 'GET', 'repos/owner/repo/pulls'], calls[0]['args'][:4])
                self.assertIn('head=owner:auto-update/sample', calls[0]['args'])
                self.assertIn('base=main', calls[0]['args'])
                self.assertIn('state=open', calls[0]['args'])
                self.assertEqual(['api', '--method', method, endpoint], calls[1]['args'][:4])
                self.assertIn('title=chore: update sample to 2.0', calls[1]['args'])
                self.assertTrue(calls[1]['body'].startswith('Updates sample from 1.0 to 2.0.\n\n'))
                if method == 'POST':
                    self.assertIn('head=auto-update/sample', calls[1]['args'])
                    self.assertIn('base=main', calls[1]['args'])

    def test_lookup_failure_does_not_create_duplicate_pr(self):
        result, calls = self.run_updater(lookup_failure=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(1, len(calls))


class ValidationAndBuilds(unittest.TestCase):
    def test_malformed_spec_rejected_by_real_parser(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.spec'
            original = (ROOT / 'waypaper/waypaper.spec').read_text()
            malformed, count = re.subn(r'^Version:.*$', 'Version:        invalid version', original, flags=re.M)
            self.assertEqual(1, count)
            path.write_text(malformed)
            result = subprocess.run(['bash', str(ROOT / '.github/scripts/validate-spec.sh'), directory, 'bad'], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('error:', result.stderr)

    def test_meta_package_without_source_validates(self):
        result = subprocess.run(['bash', str(ROOT / '.github/scripts/validate-spec.sh'), str(ROOT / 'gtklock-meta'), 'gtklock-meta'], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_build_uses_only_new_srpm_and_unique_directories(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            scripts = root / '.github/scripts'
            scripts.mkdir(parents=True)
            shutil.copyfile(ROOT / '.github/scripts/build-package.sh', scripts / 'build-package.sh')
            (scripts / 'sources.py').write_text('# Source downloader stub for this fixture.\n')
            (root / 'sample').mkdir()
            (root / 'sample/sample.spec').touch()
            stale = root / '.build/stale/SRPMS'
            stale.mkdir(parents=True)
            (stale / 'sample-0.src.rpm').touch()
            binaries = root / 'bin'
            binaries.mkdir()
            commands = {
                'rpm': '#!/bin/bash\necho x86_64\n',
                'rpmbuild': '#!/bin/bash\nwork=${2#_topdir }\ntouch "$work/SRPMS/sample-1.src.rpm"\n',
                'mock': '#!/bin/bash\nprintf "%s\\n" "${@: -1}" >> calls\n',
            }
            for name, content in commands.items():
                path = binaries / name
                path.write_text(content)
                path.chmod(0o755)
            env = dict(os.environ, PATH=str(binaries) + ':' + os.environ['PATH'])
            for _ in range(2):
                result = subprocess.run(['bash', str(scripts / 'build-package.sh'), 'mock', 'sample', '44'], cwd=root, env=env, capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stderr)
            calls = (root / 'calls').read_text().splitlines()
            self.assertEqual(2, len(set(calls)))
            self.assertTrue(all(path.endswith('/sample-1.src.rpm') for path in calls))

    def test_matrix_aggregates_failures_and_continues(self):
        # A fixture project uses the real matrix driver with fake child builds.
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            scripts = root / '.github/scripts'
            scripts.mkdir(parents=True)
            (scripts / 'packages.py').write_text('print("first\\nsecond")\n')
            (scripts / 'build-package.sh').write_text('echo "$2/$3" >> calls\n[ "$2" != first ]\n')
            result = subprocess.run(['bash', str(ROOT / '.github/scripts/build-matrix.sh'), 'all'], cwd=root, capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertEqual(['first/44', 'second/44'], (root / 'calls').read_text().splitlines())
            self.assertIn('first/fedora-44', result.stderr)


if __name__ == '__main__':
    unittest.main()
