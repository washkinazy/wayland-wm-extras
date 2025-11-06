# wayland-wm-extras

A collection of Wayland window manager tools and utilities for Fedora, packaged for COPR.

## Packages

- **[Elephant](https://github.com/abenz1267/elephant)** [(spec)](elephant/elephant.spec)
- **[Walker](https://github.com/abenz1267/walker)** [(spec)](walker/walker.spec)
- **[ReGreet](https://github.com/rharish101/ReGreet)** [(spec)](regreet/regreet.spec)
- **[SwayOSD](https://github.com/ErikReider/SwayOSD)** [(spec)](swayosd/swayosd.spec)
- **[gtk-session-lock](https://github.com/Cu3PO42/gtk-session-lock)** [(spec)](gtk-session-lock/gtk-session-lock.spec)
- **[gtklock](https://github.com/jovanlanik/gtklock)** [(spec)](gtklock/gtklock.spec)
- **[gtklock-playerctl-module](https://github.com/jovanlanik/gtklock-playerctl-module)** [(spec)](gtklock-playerctl-module/gtklock-playerctl-module.spec)
- **[gtklock-powerbar-module](https://github.com/jovanlanik/gtklock-powerbar-module)** [(spec)](gtklock-powerbar-module/gtklock-powerbar-module.spec)
- **[gtklock-userinfo-module](https://github.com/jovanlanik/gtklock-userinfo-module)** [(spec)](gtklock-userinfo-module/gtklock-userinfo-module.spec)
- **[nwg-look](https://github.com/nwg-piotr/nwg-look)** [(spec)](nwg-look/nwg-look.spec)
- **[sway-audio-idle-inhibit](https://github.com/ErikReider/SwayAudioIdleInhibit)** [(spec)](sway-audio-idle-inhibit/sway-audio-idle-inhibit.spec)
- **[python-screeninfo](https://github.com/rr-/screeninfo)** [(spec)](python-screeninfo/python-screeninfo.spec)
- **[python-imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg)** [(spec)](python-imageio-ffmpeg/python-imageio-ffmpeg.spec)
- **[waypaper](https://github.com/anufrievroman/waypaper)** [(spec)](waypaper/waypaper.spec)
- **[xcur2png](https://github.com/eworm-de/xcur2png)** [(spec)](xcur2png/xcur2png.spec)
- **[Nerd Fonts - FiraCode](https://github.com/ryanoasis/nerd-fonts)** [(spec)](nerd-fonts-firacode/nerd-fonts-firacode.spec)
- **[Nerd Fonts - JetBrainsMono](https://github.com/ryanoasis/nerd-fonts)** [(spec)](nerd-fonts-jetbrainsmono/nerd-fonts-jetbrainsmono.spec)
- **[Nerd Fonts - CascadiaCode](https://github.com/ryanoasis/nerd-fonts)** [(spec)](nerd-fonts-cascadiacode/nerd-fonts-cascadiacode.spec)

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
