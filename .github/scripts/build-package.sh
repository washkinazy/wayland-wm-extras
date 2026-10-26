#!/usr/bin/env bash
set -euo pipefail
mode=${1:?Usage: build-package.sh MODE PACKAGE [FEDORA_VERSION]}
package=${2:?Missing package}
version=${3:-44}
[[ "$package" =~ ^[a-z0-9][a-z0-9+_.-]*$ ]] || exit 2
[[ "$version" =~ ^[0-9]+$ ]] || exit 2
[[ "$mode" = mock || "$mode" = build ]] || exit 2
root=$(cd "$(dirname "$0")/../.." && pwd)
cd "$root"
spec="$root/$package/$package.spec"
test -f "$spec"
# Every invocation has its own SRPM/source tree and retained result directory.
mkdir -p "$root/.build"
work=$(mktemp -d "$root/.build/$package-f$version.XXXXXX")
trap 'echo "Build files and logs: $work"' EXIT
mkdir -p "$work"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS,result}
python3 .github/scripts/sources.py "$spec" --destination "$work/SOURCES"
if [ "$mode" = build ]; then
    rpmbuild --define "_topdir $work" -ba "$spec"
else
    rpmbuild --define "_topdir $work" -bs "$spec"
    shopt -s nullglob
    srpms=("$work"/SRPMS/*.src.rpm)
    if [ "${#srpms[@]}" -ne 1 ]; then
        echo 'Expected exactly one newly generated SRPM' >&2
        exit 1
    fi
    arch=$(rpm --eval '%{_arch}')
    # Dependencies such as gtk-session-lock are supplied by this COPR.
    mock --isolation="${MOCK_ISOLATION:-nspawn}" -r "fedora-$version-$arch" --uniqueext "$(basename "$work")" \
        --enable-network --resultdir "$work/result" \
        --addrepo "https://download.copr.fedorainfracloud.org/results/washkinazy/wayland-wm-extras/fedora-$version-$arch/" \
        --rebuild "${srpms[0]}"
fi
