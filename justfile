# Wayland Tools RPM Packaging - justfile
# All packaging tasks run inside distrobox

# Default recipe - show available commands
default:
    @just --list

# Enter a Fedora packaging distrobox container
enter version="41":
    distrobox enter fedora-packaging-{{version}}

# Create and setup the Fedora 41 packaging container
setup-41:
    distrobox create --name fedora-packaging-41 --image registry.fedoraproject.org/fedora:41
    distrobox enter fedora-packaging-41 -- sudo dnf install -y just mock fedora-packager rpm-build rpmdevtools spectool rust2rpm golang
    @echo "Fedora 41 container created. Run 'just enter 41' then 'sudo usermod -a -G mock \$USER' and re-enter."

# Create and setup the Fedora 42 packaging container
setup-42:
    distrobox create --name fedora-packaging-42 --image registry.fedoraproject.org/fedora:42
    distrobox enter fedora-packaging-42 -- sudo dnf install -y just mock fedora-packager rpm-build rpmdevtools spectool rust2rpm golang
    @echo "Fedora 42 container created. Run 'just enter 42' then 'sudo usermod -a -G mock \$USER' and re-enter."

# Create and setup the Fedora 43 packaging container (rawhide)
setup-43:
    distrobox create --name fedora-packaging-43 --image registry.fedoraproject.org/fedora:rawhide
    distrobox enter fedora-packaging-43 -- sudo dnf install -y just mock fedora-packager rpm-build rpmdevtools spectool rust2rpm golang
    @echo "Fedora 43 (rawhide) container created. Run 'just enter 43' then 'sudo usermod -a -G mock \$USER' and re-enter."

# Setup all Fedora versions (41, 42, 43)
setup-all:
    just setup-41
    just setup-42
    just setup-43
    @echo ""
    @echo "All containers created. Enter each and run: sudo usermod -a -G mock \$USER"

# Build a package using mock (run inside distrobox)
mock package fedora_version="41":
    #!/usr/bin/env bash
    set -e
    if [ ! -f "{{package}}/{{package}}.spec" ]; then
        echo "Error: Spec file not found at {{package}}/{{package}}.spec"
        exit 1
    fi

    # Setup rpmbuild directories
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

    # Copy local source files (Source1, Source2, etc.) to SOURCES FIRST
    echo "Copying local source files for {{package}}..."
    for file in {{package}}/*; do
        filename=$(basename "$file")
        if [ -f "$file" ] && [ "$filename" != "{{package}}.spec" ] && [ "$filename" != "README.md" ]; then
            echo "Copying $filename to ~/rpmbuild/SOURCES/"
            cp "$file" ~/rpmbuild/SOURCES/
        fi
    done

    # Download remote sources using spectool (only downloads URLs, skips local files)
    echo "Downloading remote sources for {{package}}..."
    spectool -g -C ~/rpmbuild/SOURCES {{package}}/{{package}}.spec

    # Build source RPM
    echo "Building source RPM for {{package}}..."
    rpmbuild -bs {{package}}/{{package}}.spec

    # Find the generated SRPM
    SRPM=$(find ~/rpmbuild/SRPMS -name "{{package}}-*.src.rpm" | head -1)

    if [ -z "$SRPM" ]; then
        echo "Error: Source RPM not found"
        exit 1
    fi

    echo "Building with mock for Fedora {{fedora_version}}..."
    mock -r fedora-{{fedora_version}}-x86_64 "$SRPM"

    echo "Build complete! Results in: /var/lib/mock/fedora-{{fedora_version}}-x86_64/result/"

# Build a package with rpmbuild (run inside distrobox)
build package:
    #!/usr/bin/env bash
    if [ ! -f "{{package}}/{{package}}.spec" ]; then
        echo "Error: Spec file not found at {{package}}/{{package}}.spec"
        exit 1
    fi
    cd {{package}}
    rpmbuild -ba {{package}}.spec

# Review spec file quality with fedora-review (run inside distrobox)
review package:
    fedora-review -n {{package}}

# Generate initial spec file for Rust package (run inside distrobox)
rust-spec package:
    #!/usr/bin/env bash
    mkdir -p {{package}}
    cd {{package}}
    rust2rpm {{package}}

# Update package version in spec file
update package version:
    #!/usr/bin/env bash
    if [ ! -f "{{package}}/{{package}}.spec" ]; then
        echo "Error: Spec file not found at {{package}}/{{package}}.spec"
        exit 1
    fi
    echo "Updating {{package}} to version {{version}}"
    echo "Remember to:"
    echo "  1. Update Version: field to {{version}}"
    echo "  2. Update Source0 URL if needed"
    echo "  3. Add %changelog entry"
    echo "  4. Test with 'just mock {{package}}'"

# Vendor Rust dependencies for swayosd (run inside distrobox)
vendor-swayosd version="0.2.1":
    #!/usr/bin/env bash
    set -e
    cd swayosd

    NAME="swayosd"
    GITNAME="SwayOSD"
    VERSION="{{version}}"

    echo "Vendoring dependencies for SwayOSD ${VERSION}..."

    # Download source if not present
    if [ ! -f "${GITNAME}-${VERSION}.tar.gz" ]; then
        echo "Downloading ${GITNAME}-${VERSION}.tar.gz..."
        curl -L -o "${GITNAME}-${VERSION}.tar.gz" \
            "https://github.com/ErikReider/SwayOSD/archive/v${VERSION}/${GITNAME}-${VERSION}.tar.gz"
    fi

    # Extract source
    echo "Extracting source..."
    tar xf "${GITNAME}-${VERSION}.tar.gz"

    # Vendor dependencies
    echo "Running cargo vendor..."
    cd "${GITNAME}-${VERSION}"
    cargo vendor

    # Create vendor tarball
    echo "Creating vendor tarball..."
    tar Jcvf "../${NAME}-${VERSION}-vendor.tar.xz" vendor/

    # Clean up extracted directory
    cd ..
    rm -rf "${GITNAME}-${VERSION}"

    echo "Done! Created ${NAME}-${VERSION}-vendor.tar.xz"

# Clean mock build results (run inside distrobox)
clean:
    rm -rf /var/lib/mock/fedora-*/result/*.rpm

# List all packages in repository
list:
    #!/usr/bin/env bash
    echo "Packages in repository:"
    for dir in */; do
        if [ -f "$dir$(basename $dir).spec" ]; then
            echo "  - $(basename $dir)"
        fi
    done

# Run mock build for all packages (run inside distrobox)
build-all fedora_version="41":
    #!/usr/bin/env bash
    for dir in */; do
        package=$(basename "$dir")
        if [ -f "$dir$package.spec" ]; then
            echo "Building $package..."
            just mock "$package" {{fedora_version}} || echo "Failed to build $package"
        fi
    done

# Build a package for all Fedora versions (41, 42, 43)
mock-all package:
    #!/usr/bin/env bash
    echo "Building {{package}} for Fedora 41..."
    just mock {{package}} 41
    echo "Building {{package}} for Fedora 42..."
    just mock {{package}} 42
    echo "Building {{package}} for Fedora 43..."
    just mock {{package}} 43

# Build all packages for all Fedora versions
build-matrix:
    #!/usr/bin/env bash
    for version in 41 42 43; do
        echo "===== Building all packages for Fedora $version ====="
        just build-all $version
    done
