# Wayland Tools COPR - Fedora Packaging Project

## Project Overview
Create a Fedora COPR repository following the solopasha/hyprlandRPM pattern to package Wayland/Hyprland ecosystem tools that are not currently available in official Fedora repositories.

## Reference Pattern
- **Model Repository**: https://github.com/solopasha/hyprlandRPM
- **Pattern**: One repository with multiple subdirectories, each containing a spec file for a different package
- **COPR Integration**: Single COPR project that builds all packages from one repository

## Repository Structure
```
wayland-toolsRPM/
├── README.md
├── walker/
│   └── walker.spec
├── elephant/
│   └── elephant.spec
├── swayosd/
│   └── swayosd.spec
├── swaync/
│   └── swaync.spec
└── .github/
    └── workflows/
        └── (optional CI/CD)
```

## Packages to Include

### 1. Walker
- **Upstream**: https://github.com/abenz1267/walker
- **Description**: Multi-purpose launcher with GTK4 and Rust
- **Language**: Rust
- **Dependencies**: GTK4 (4.6+), gtk4-layer-shell, protobuf-compiler, cairo, poppler-glib
- **License**: GPL v3.0
- **Notes**: Requires elephant as runtime dependency

### 2. Elephant
- **Upstream**: https://github.com/abenz1267/elephant
- **Description**: Data provider service and backend for application launchers
- **Language**: Go (1.24.5+)
- **Dependencies**: protobuf-compiler
- **License**: GPL v3.0
- **Notes**: Go plugin architecture, all providers should be built and packaged together

### 3. SwayOSD
- **Upstream**: https://github.com/ErikReider/SwayOSD
- **Description**: GTK-based on-screen display for volume and brightness
- **Language**: Vala/GTK
- **Dependencies**: gtk3, gtk-layer-shell, pulse-audio, libudev
- **License**: GPL v3.0

### 4. SwayNotificationCenter (swaync)
- **Upstream**: https://github.com/ErikReider/SwayNotificationCenter
- **Description**: Simple notification daemon with GTK GUI for notifications and control center
- **Language**: Vala/GTK
- **Dependencies**: gtk3, gtk-layer-shell, json-glib, libgee, dbus
- **License**: GPL v3.0

## Technical Requirements

### Rust Packages (Walker)
- Use `rust2rpm` to generate initial spec file
- BuildRequires: rust, cargo, gtk4-devel, gtk4-layer-shell-devel, protobuf-compiler, cairo-devel, poppler-glib-devel
- Requires: elephant

### Go Packages (Elephant)
- BuildRequires: golang >= 1.24.5, protobuf-compiler
- Build main binary + all provider plugins
- Install plugins to `/usr/lib64/elephant/providers/`
- Include configuration examples

### Vala/GTK Packages (SwayOSD, SwayNC)
- BuildRequires: vala, meson, gtk3-devel, gtk-layer-shell-devel, etc.
- Standard meson build system
- Include systemd user service files if present

## Spec File Components

Each spec file should include:
1. **Header**: Name, Version, Release, Summary, License, URL, Source0
2. **BuildRequires**: All build-time dependencies
3. **Requires**: All runtime dependencies
4. **%description**: Clear description of the package
5. **%prep**: Extract source tarball
6. **%build**: Build commands (cargo build, go build, meson compile, etc.)
7. **%install**: Installation commands
8. **%files**: List of installed files
9. **%changelog**: Version history

## COPR Setup Steps

1. Create repository: `wayland-toolsRPM`
2. Initialize git repository
3. Create subdirectory for each package with spec file
4. Create COPR project at https://copr.fedorainfracloud.org/
5. Configure COPR to build from git repository
6. COPR will auto-detect all spec files and build each package

## README.md Content Structure

Follow solopasha's pattern:
- Brief introduction
- List of all packages with:
  - Package name (linked to upstream)
  - Link to spec file in repo
  - Brief description
- Installation instructions
- COPR enable command

## Development Workflow

1. **Adding a new package**:
   - Create subdirectory with package name
   - Research upstream build system
   - Create spec file
   - Test locally with `rpmbuild` or `mock`
   - Commit to repository
   - COPR rebuilds automatically

2. **Updating a package**:
   - Update Version field in spec
   - Update Source0 URL if needed
   - Add changelog entry
   - Commit and push
   - COPR rebuilds

3. **Testing builds locally**:
   ```bash
   # Install mock
   sudo dnf install mock fedora-packager
   
   # Add user to mock group
   sudo usermod -a -G mock $USER
   
   # Build package
   mock -r fedora-41-x86_64 packagename.spec
   ```

## Initial Tasks

1. Create repository structure
2. Generate spec file for elephant (dependency)
3. Generate spec file for walker (depends on elephant)
4. Generate spec file for SwayOSD
5. Generate spec file for SwayNC
6. Create comprehensive README.md
7. Test builds locally
8. Push to GitHub
9. Configure COPR project
10. Verify all packages build successfully

## Notes

- Packages should target current Fedora stable and rawhide
- Follow Fedora packaging guidelines: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- Use `fedora-review` tool to check spec file quality
- Each package is independent - can be installed separately
- Walker requires elephant, specify this in Requires field