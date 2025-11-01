#!/bin/bash
set -e

echo "==> Setting up Fedora RPM packaging environment..."

sudo dnf update -y

sudo dnf install -y \
    rpm-build \
    rpmdevtools \
    rpmlint \
    mock \
    fedora-packager \
    fedora-review \
    spectool \
    git \
    curl \
    jq \
    just

sudo dnf install -y \
    rust \
    cargo \
    cargo-rpm-macros \
    golang \
    python3-devel

# Setup rpmdev tree
rpmdev-setuptree

# Add user to mock group (requires re-login to take effect)
sudo usermod -a -G mock vscode || true

# Configure mock (allow network access for rust/go builds)
sudo mkdir -p /etc/mock
echo "config_opts['use_host_resolv'] = True" | sudo tee -a /etc/mock/site-defaults.cfg
echo "config_opts['rpmbuild_networking'] = True" | sudo tee -a /etc/mock/site-defaults.cfg

echo ""
echo "==> Setup complete!"
echo ""
echo "Note: You may need to restart your terminal or container for mock group membership to take effect."
echo ""
echo "Available commands:"
echo "  just list          - List all packages"
echo "  just mock <pkg>    - Test build a package with mock"
echo "  just build <pkg>   - Build a package with rpmbuild"
echo "  just review <pkg>  - Run fedora-review on a package"
echo ""
