# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a Fedora COPR packaging repository for Wayland/Hyprland ecosystem tools not available in official Fedora repos. It follows the solopasha/hyprlandRPM pattern: one repository with multiple subdirectories, each containing RPM spec files for different packages.

**Reference Model**: https://github.com/solopasha/hyprlandRPM

## Repository Structure

```
wayland-toolsRPM/
├── walker/          # Rust-based multi-purpose launcher
│   └── walker.spec
├── elephant/        # Go-based data provider service (walker dependency)
│   └── elephant.spec
├── swayosd/         # Vala/GTK on-screen display
│   └── swayosd.spec
└── swaync/          # Vala/GTK notification daemon
    └── swaync.spec
```

Each package directory contains a single `.spec` file. COPR auto-detects all spec files and builds each package.

## Package Details

### Elephant (Build First - Required Dependency)
- **Language**: Go 1.24.5+
- **Upstream**: https://github.com/abenz1267/elephant
- **Build System**: Go with protobuf
- **Key Requirements**:
  - Must build main binary + all provider plugins
  - Plugins install to `/usr/lib64/elephant/providers/`
  - Use `protobuf-compiler` at build time

### Walker (Depends on Elephant)
- **Language**: Rust
- **Upstream**: https://github.com/abenz1267/walker
- **Build System**: Cargo
- **Key Requirements**:
  - Generate initial spec with `rust2rpm`
  - GTK4 4.6+ required
  - Add `Requires: elephant` in spec file

### SwayOSD & SwayNC
- **Language**: Vala/GTK
- **Build System**: Meson
- **Upstreams**:
  - SwayOSD: https://github.com/ErikReider/SwayOSD
  - SwayNC: https://github.com/ErikReider/SwayNotificationCenter
- **Key Requirements**: Include systemd user service files if present

## Development Environment

**Host System**: Non-Fedora (all testing done in distrobox containers)

### Distrobox Setup

Multiple Fedora versions are supported (41, 42, 43/rawhide) for testing package builds across releases.

```bash
# Setup individual versions
just setup-41    # Fedora 41 stable
just setup-42    # Fedora 42 stable
just setup-43    # Fedora 43 rawhide

# Or setup all versions at once
just setup-all

# After setup, enter each container and add user to mock group:
just enter 41
sudo usermod -a -G mock $USER
# Exit and re-enter for changes to take effect
```

## Common Commands

All commands should be run inside the distrobox container. Use the `justfile` for common tasks:

```bash
# Enter a packaging container (default: Fedora 41)
just enter          # Enter Fedora 41
just enter 42       # Enter Fedora 42
just enter 43       # Enter Fedora 43

# Test a spec file with mock
just mock <package-name>            # Build for Fedora 41
just mock <package-name> 42         # Build for Fedora 42
just mock-all <package-name>        # Build for all versions (41, 42, 43)

# Build all packages
just build-all              # Build all packages for Fedora 41
just build-all 42           # Build all packages for Fedora 42
just build-matrix           # Build all packages for all versions

# Other commands
just build <package-name>           # Build with rpmbuild
just review <package-name>          # Check spec file quality
just rust-spec <package-name>       # Generate initial Rust spec
just update <package-name> <ver>    # Update package version helper
just list                           # List all packages
just clean                          # Clean mock build results
```

### Manual Commands (if not using justfile)
```bash
# Build a package for Fedora 41 (inside distrobox)
mock -r fedora-41-x86_64 path/to/package.spec

# Check spec file quality
fedora-review -n packagename

# Generate Rust spec file
rust2rpm packagename

# For Go packages (elephant): Manual spec creation required
# For Vala/Meson packages (swayosd, swaync): Manual spec creation required
```

## Spec File Requirements

Each spec file must include:
1. **Header**: Name, Version, Release, Summary, License, URL, Source0
2. **BuildRequires**: All build-time dependencies
3. **Requires**: Runtime dependencies (e.g., walker requires elephant)
4. **%description**: Package description
5. **%prep**: Source extraction
6. **%build**: Build commands (cargo build / go build / meson compile)
7. **%install**: Installation
8. **%files**: File list
9. **%changelog**: Version history

## Critical Dependencies

- **Walker → Elephant**: Walker spec must have `Requires: elephant`
- **Build Order**: Build elephant first, then walker
- **Plugin Architecture**: Elephant's Go plugins must all be built and packaged together

## COPR Integration

1. Create COPR project at https://copr.fedorainfracloud.org/
2. Configure COPR to build from this git repository
3. COPR automatically detects all `.spec` files in subdirectories
4. Push to GitHub triggers automatic rebuilds

## Packaging Guidelines

- Follow Fedora Packaging Guidelines: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- Target current Fedora stable and rawhide
- Each package is independent (can be installed separately)
- All packages are GPL v3.0 licensed
