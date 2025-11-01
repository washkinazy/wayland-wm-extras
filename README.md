# wayland-wm-extras

A collection of Wayland window manager tools and utilities for Fedora, packaged for COPR.

## Packages

- **[Elephant](https://github.com/abenz1267/elephant)** [(spec)](elephant/elephant.spec) - Data provider service for Walker launcher with plugins for applications, clipboard, files, and more.
- **[ReGreet](https://github.com/rharish101/ReGreet)** [(spec)](regreet/regreet.spec) - Clean and customizable GTK-based greeter for greetd.
- **[SwayOSD](https://github.com/ErikReider/SwayOSD)** [(spec)](swayosd/swayosd.spec) - GTK-based on-screen display for keyboard shortcuts, volume, and brightness in Wayland compositors.
- **[Walker](https://github.com/abenz1267/walker)** [(spec)](walker/walker.spec) - Fast, customizable application launcher built with GTK4 and Rust for Wayland.
- **[gtk-session-lock](https://github.com/Cu3PO42/gtk-session-lock)** [(spec)](gtk-session-lock/gtk-session-lock.spec) - Library for creating Wayland screen lockers using ext-session-lock protocol.
- **[gtklock](https://github.com/jovanlanik/gtklock)** [(spec)](gtklock/gtklock.spec) - GTK-based lock screen for Wayland.
- **[gtklock-playerctl-module](https://github.com/jovanlanik/gtklock-playerctl-module)** [(spec)](gtklock-playerctl-module/gtklock-playerctl-module.spec) - Media player controls module for gtklock.
- **[gtklock-powerbar-module](https://github.com/jovanlanik/gtklock-powerbar-module)** [(spec)](gtklock-powerbar-module/gtklock-powerbar-module.spec) - Power controls module for gtklock.
- **[gtklock-userinfo-module](https://github.com/jovanlanik/gtklock-userinfo-module)** [(spec)](gtklock-userinfo-module/gtklock-userinfo-module.spec) - User info module for gtklock.
- **[sway-audio-idle-inhibit](https://github.com/ErikReider/SwayAudioIdleInhibit)** [(spec)](sway-audio-idle-inhibit/sway-audio-idle-inhibit.spec) - Prevents idle sleep while audio is playing.

## Installation

```bash
# Enable the COPR repository
sudo dnf copr enable washkinazy/wayland-wm-extras

# Install packages
sudo dnf install walker elephant gtklock
```

## Automated Updates

This repository uses GitHub Actions to automatically monitor upstream releases and update packages:

- **Daily monitoring**: Checks for new releases every day at midnight UTC
- **Automatic spec updates**: Creates pull requests with updated spec files when new versions are detected
- **Auto-merge**: PRs merge automatically once validation passes
- **COPR webhook**: Merged changes trigger automatic rebuilds in COPR
- **Manual trigger**: Updates can be triggered for individual packages via GitHub Actions UI

## Building

All packages are built automatically in COPR. Builds are triggered:
- Automatically via webhook when commits are pushed to main
- When the automated update system merges PRs
- Manually via COPR web interface

## Development

### Using Dev Container (Recommended)

This repository includes a Fedora-based dev container configuration for VSCode/Codespaces:

1. **Open in dev container:**
   - VSCode: Install "Dev Containers" extension, then "Reopen in Container"
   - GitHub Codespaces: Click "Code" → "Create codespace on main"

2. **Build and test packages:**
   ```bash
   # Test build a package with mock
   just mock elephant

   # Build with rpmbuild
   just build walker

   # Run fedora-review
   just review gtklock

   # Build all packages for all versions
   just build-matrix
   ```

### Alternative: Local Distrobox

If you prefer distrobox on your local machine:

```bash
# Setup distrobox (see justfile for version-specific setup)
just setup-41    # or setup-42, setup-43

# Enter container
just enter 41

# Test build a package
just mock elephant
```