# SwayOSD Package

A GTK based on-screen display (OSD) for common actions like volume changes, brightness, caps-lock state, and other keyboard shortcuts in Wayland compositors.

## Upstream

- **Repository**: https://github.com/ErikReider/SwayOSD
- **Current Version**: 0.2.1
- **License**: GPL-3.0-or-later

## Packaging Notes

This package uses the modern Fedora Rust packaging approach with `cargo-rpm-macros`:

- **No vendor tarball needed** - COPR/mock automatically handles Rust dependency vendoring via `%cargo_prep`
- **Release tarballs** - Uses official GitHub release tarballs instead of git commits
- **Automatic dependency management** - `cargo-rpm-macros` handles the entire Rust build chain

### Build Requirements

- Rust toolchain (rust, cargo, cargo-rpm-macros)
- GTK3 and layer-shell support
- Meson build system
- Audio: PulseAudio libraries
- Input: libinput, libevdev, libudev

### Runtime Requirements

- Wayland compositor
- GTK3 and gtk-layer-shell
- PulseAudio
- systemd (for swayosd-libinput-backend.service)

## Files

- `swayosd.spec` - RPM spec file
- `swayosd.sysusers` - Creates video group for hardware access

## Building

```bash
# Test build with mock for Fedora 41
just mock swayosd

# Build for all supported versions
just mock-all swayosd
```

## Differences from Other Packages

Unlike older packaging approaches that use pre-vendored Rust dependencies (vendor tarballs), this package leverages Fedora's modern `cargo-rpm-macros` which:

1. Automatically vendors dependencies during `%prep`
2. Ensures builds use current dependency resolution
3. Simplifies spec file maintenance
4. Is the recommended approach per Fedora Rust packaging guidelines
