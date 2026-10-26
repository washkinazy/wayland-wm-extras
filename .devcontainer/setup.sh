#!/usr/bin/env bash
set -euo pipefail
sudo dnf install -y rpm-build rpmdevtools rpmlint mock fedora-packager fedora-review \
    git curl jq just shellcheck python3-rpm python3-pyyaml python3-devel \
    redhat-rpm-config pyproject-rpm-macros cargo-rpm-macros systemd-rpm-macros \
    meson rust cargo rust2rpm golang
rpmdev-setuptree
sudo usermod -a -G mock "$(id -un)"
echo 'Setup complete. Re-enter the container to activate mock group membership.'
echo 'Run just check, then just mock PACKAGE. Build networking is enabled per invocation.'
