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

## Automated Updates

This repository uses GitHub Actions to automatically monitor upstream releases and update packages:

- **Daily monitoring**: Checks for new releases every day at midnight UTC
- **Automatic PRs**: Creates pull requests with updated spec files when new versions are detected
- **Auto-merge**: PRs automatically merge once validation passes
- **Manual updates**: Can trigger updates for individual packages via GitHub Actions UI

