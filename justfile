# Parameters are passed as positional arguments rather than interpolated shell code.
set positional-arguments

default:
    @just --list

enter version="44":
    distrobox enter "fedora-packaging-$1"

setup version="44":
    #!/usr/bin/env bash
    set -euo pipefail
    [[ "$1" =~ ^[0-9]+$ ]] || exit 2
    distrobox create --name "fedora-packaging-$1" --image "registry.fedoraproject.org/fedora:$1"
    distrobox enter "fedora-packaging-$1" -- bash .devcontainer/setup.sh

setup-43:
    just setup 43

setup-44:
    just setup 44

mock package fedora_version="44":
    bash .github/scripts/build-package.sh mock "$1" "$2"

build package:
    bash .github/scripts/build-package.sh build "$1"

review package:
    fedora-review -n "$1"

rust-spec package:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p -- "$1"
    cd -- "$1"
    rust2rpm "$1"

# Discover and apply an upstream update (requires GH_TOKEN).
update package:
    python3 .github/scripts/packages.py update "$1"

list:
    python3 .github/scripts/packages.py names

build-all fedora_version="44":
    bash .github/scripts/build-matrix.sh all "$1"

mock-all package:
    bash .github/scripts/build-matrix.sh "$1" 43 44

build-matrix:
    bash .github/scripts/build-matrix.sh all 43 44

check:
    #!/usr/bin/env bash
    set -euo pipefail
    python3 .github/scripts/packages.py validate
    python3 -m unittest discover -s tests -v
    shellcheck .github/scripts/*.sh .devcontainer/setup.sh
    for spec in */*.spec; do rpmspec -P "$spec" >/dev/null; done

# Clean only artifacts created by this repository.
clean:
    rm -rf -- .build
