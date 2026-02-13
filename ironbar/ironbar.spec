%global debug_package %{nil}
%global forgeurl https://github.com/JakeStanger/ironbar
%global tag v%{version}

Name:           ironbar
Version:        0.18.0
%forgemeta
Release:        1%{?dist}
Summary:        Customizable GTK4 bar for Wayland compositors

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  gtk4-devel >= 4.12
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  dbus-devel
BuildRequires:  openssl-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libinput-devel
BuildRequires:  luajit-devel
BuildRequires:  libevdev-devel

Requires:       gtk4
Requires:       gtk4-layer-shell

%description
Customizable and feature-rich GTK4 bar for Wayland compositors such as Sway
and Hyprland. Supports modules for workspaces, tray, clock, notifications,
music, and more with CSS styling.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release

%install
install -Dm755 target/release/ironbar %{buildroot}%{_bindir}/ironbar

%files
%license LICENSE
%doc README.md
%{_bindir}/ironbar

%changelog
* Thu Feb 12 2026 Automated Update <noreply@github.com> - 0.18.0-1
- Initial package for version 0.18.0
