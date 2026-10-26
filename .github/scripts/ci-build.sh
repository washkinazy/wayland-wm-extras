#!/usr/bin/env bash
set -euo pipefail
dnf install -y mock git curl python3 rpm-build redhat-rpm-config python3-devel \
    pyproject-rpm-macros cargo-rpm-macros systemd-rpm-macros meson
MOCK_ISOLATION=simple bash .github/scripts/build-package.sh mock "$PACKAGE" "$FEDORA"
