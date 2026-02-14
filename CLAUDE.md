# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of RPM spec files for Wayland window manager tools and utilities, packaged for Fedora and distributed via COPR (washkinazy/wayland-wm-extras). The repository automates package updates through GitHub Actions that monitor upstream releases and trigger COPR rebuilds.

## Package Structure

Each package lives in its own directory with the following structure:
- `<package>/<package>.spec` - RPM spec file
- `<package>/<additional-sources>` - Local source files (configs, patches, etc.)
- All packages are defined in `packages.yml` which maps package names to upstream GitHub repos

Key packages include:
- **walker**: GTK4/Rust application launcher (depends on elephant)
- **elephant**: Data provider service for walker (Go, builds plugins)
- **regreet**: GTK4/Rust greeter for greetd
- **gtklock** family: Screen lock and modules (C/Meson)
- **swayosd**: On-screen display for Sway
- Various supporting libraries and Python dependencies

## Build System

### Just Commands (Primary Interface)

All development tasks use `just` (justfile):

**Building packages:**
```bash
just mock <package> [fedora_version]  # Build with mock (default: F43)
just mock-all <package>               # Build for F42, F43, F44
just build <package>                  # Quick rpmbuild (no mock)
just build-all [fedora_version]       # Build all packages
just build-matrix                     # Build all packages for all versions
```

**Package management:**
```bash
just list                             # List all packages
just update <package> <version>       # Update package version (interactive)
```

**Environment setup (distrobox):**
```bash
just setup-42                         # Create F42 container
just setup-43                         # Create F43 container
just setup-44                         # Create F44/rawhide container
just enter [version]                  # Enter container
```

### Build Process Details

The mock build recipe (lines 31-71 of justfile):
1. Creates ~/rpmbuild directories
2. Copies local source files (Source1, Source2, etc.) to SOURCES
3. Downloads remote sources with spectool (Source0)
4. Builds SRPM with rpmbuild -bs
5. Runs mock with the SRPM

Important: Local source files must be copied BEFORE spectool runs to avoid conflicts.

## Spec File Patterns

### Go Packages (elephant)
```spec
%global forgeurl https://github.com/...
Version:        X.Y.Z
%forgemeta
Source0:        %{forgesource}
BuildRequires:  golang >= 1.21
```
Build section builds main binary and provider plugins via makefiles.

### Rust Packages (walker, regreet)
```spec
%global forgeurl https://github.com/...
Version:        X.Y.Z
%forgemeta
Source0:        %{forgesource}
BuildRequires:  rust, cargo, cargo-rpm-macros >= 25
```
Build with `cargo build --release` (online mode, fetches from crates.io).

### Local Source Files
Additional sources (configs, patches) are referenced as:
```spec
Source1:        filename.conf
Source2:        filename.patch
```
Install with: `install -Dm644 %{SOURCE1} %{buildroot}/path/to/file`

### Changelog Format
```spec
%changelog
* Day Month Date Year Name <email> - version-release
- Change description
```
Automated updates use: `Automated Update <noreply@github.com>`

## Automated Update System

### GitHub Actions Workflow

**update-package.yml** (reusable workflow):
1. Fetches latest upstream release via GitHub API (falls back to tags if no releases exist)
2. Extracts version from tag (strips leading 'v')
3. Compares with current spec Version field
4. If update needed:
   - Runs `.github/scripts/update-spec.sh` to modify spec
   - Runs `.github/scripts/validate-spec.sh` for syntax check
   - Runs `.github/scripts/check-source.sh` to verify source accessibility
   - Creates PR with auto-merge

**monitor-all-packages.yml**: Daily cron job that calls update-package.yml for each package in packages.yml

**update-single-package.yml**: Manual workflow_dispatch for individual package updates

### Update Scripts

Located in `.github/scripts/`:
- `update-spec.sh`: Updates Version, Source0 URL, adds changelog entry
- `validate-spec.sh`: Basic spec file syntax validation
- `check-source.sh`: Verifies source tarballs are accessible

### COPR Integration

Main branch pushes trigger COPR webhook → automatic rebuilds for all Fedora versions.

## Development Environment

### Dev Container (Recommended)

The repository includes a Fedora 42-based dev container (`.devcontainer/devcontainer.json`):
- Auto-installs RPM packaging tools via setup script
- Mounts host's .gitconfig, .ssh, .local/bin
- Configured for nested containers (mock support)
- VSCode extensions: rust-analyzer, Go, YAML, shell tools

**Usage:**
1. "Reopen in Container" (VSCode) or create Codespace
2. Run `just mock <package>` to test builds

### Distrobox (Alternative)

For local development without containers:
```bash
just setup-43          # Create F43 distrobox
just enter 43          # Enter container
sudo usermod -a -G mock $USER  # Add user to mock group
exit                   # Re-enter for group to take effect
just mock <package>    # Build packages
```

## Common Development Workflows

### Adding a New Package

1. Create directory: `mkdir <package>`
2. Add spec file: `<package>/<package>.spec`
3. Add to `packages.yml`:
   ```yaml
   - name: package-name
     repo: owner/repo
     spec_dir: package-name
   ```
4. Test build: `just mock <package>`
5. Add to README.md package list

### Updating a Package Manually

1. Edit spec file: Update Version, Source0, %changelog
2. Copy any new local sources to package directory
3. Test build: `just mock <package>` (all versions: `just mock-all <package>`)
4. Commit and push to trigger COPR rebuild

### Debugging Build Failures

1. Check mock results: `/var/lib/mock/fedora-<version>-x86_64/result/`
2. Examine build.log and root.log in results directory
3. Enter mock chroot for investigation: `mock -r fedora-<version>-x86_64 --shell`
4. Verify sources downloaded: `ls ~/rpmbuild/SOURCES/`

### Testing Spec Changes

After modifying a spec file:
```bash
just mock <package> 43              # Test F43 build
just mock-all <package>             # Test all versions
```

Mock builds are isolated and safe - they won't affect the system.

## Git Workflow

- Main branch: `main` (protected, requires PR)
- Feature branches: Descriptive names
- Auto-update branches: `auto-update/<package>-<version>` (auto-merged)
- Current branch `deps/nwg-look` appears to be a dependency work branch

## Important Notes

- Mock requires user to be in mock group: `sudo usermod -a -G mock $USER`
- Rust/Go builds use online mode (fetch dependencies during build)
- COPR rebuilds are triggered by webhook on main branch pushes only
- Spec files use `%forgemeta` macro for automatic source URL generation
- Package dependencies (walker→elephant) must be built in order
- ReGreet uses Fedora-specific greetd user instead of Arch's greeter user
