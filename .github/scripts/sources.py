#!/usr/bin/env python3
"""Resolve RPM source/patch declarations and download their exact URLs."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit


def stage(spec, destination):
    parsed = subprocess.check_output(['rpmspec', '-P', str(spec)], text=True)
    declarations = re.findall(r'^(?:Source|Patch)\d*:\s*(\S+)\s*$', parsed, re.M)
    seen = {}
    for value in declarations:
        if '%{' in value:
            raise ValueError(f'Unexpanded source macro: {value}')
        url = urlsplit(value)
        if url.scheme and url.scheme != 'https':
            raise ValueError(f'Only HTTPS sources are supported: {value}')
        name = Path(url.fragment if url.fragment.startswith('/') else url.path).name
        if not name or name in ('.', '..'):
            raise ValueError(f'Invalid source filename: {value}')
        if name in seen and seen[name] != value:
            raise ValueError(f'Conflicting source filenames: {name}')
        seen[name] = value
        target = destination / name
        if url.scheme:
            subprocess.run(['curl', '--fail', '--location', '--show-error', '--silent',
                            '--retry', '3', '--connect-timeout', '30', '--max-time', '600',
                            '--proto', '=https', '--proto-redir', '=https',
                            '--output', str(target), value.split('#', 1)[0]], check=True)
        else:
            source = (spec.parent / value).resolve()
            if not source.is_relative_to(spec.parent.resolve()):
                raise ValueError(f'Local source escapes package directory: {value}')
            shutil.copyfile(source, target)
        print(f'Checked {name}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    parser.add_argument('--destination', type=Path)
    args = parser.parse_args()
    if args.destination:
        args.destination.mkdir(parents=True, exist_ok=True)
        stage(args.spec.resolve(), args.destination)
    else:
        with tempfile.TemporaryDirectory(prefix='rpm-sources-') as directory:
            stage(args.spec.resolve(), Path(directory))


if __name__ == '__main__':
    main()
