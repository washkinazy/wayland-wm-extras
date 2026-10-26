#!/usr/bin/env bash
set -euo pipefail
package=${1:?Missing package or all}
shift
if [ "$#" -eq 0 ]; then set -- 43 44; fi
if [ "$package" = all ]; then
    names=$(python3 .github/scripts/packages.py names)
    mapfile -t packages <<< "$names"
else
    packages=("$package")
fi
failed=()
for version in "$@"; do
    for package in "${packages[@]}"; do
        if ! bash .github/scripts/build-package.sh mock "$package" "$version"; then
            failed+=("$package/fedora-$version")
        fi
    done
done
if [ "${#failed[@]}" -gt 0 ]; then
    printf 'Failed: %s\n' "${failed[@]}" >&2
    exit 1
fi
