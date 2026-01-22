%global debug_package %{nil}
%global forgeurl https://github.com/MalpenZibo/ashell
%global tag %{version}

Name:           ashell
Version:        0.7.0
%forgemeta
Release:        1%{?dist}
Summary:        A ready to go Wayland status bar for Hyprland and Niri

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  clang-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  dbus-devel
BuildRequires:  wayland-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pkgconfig(xkbcommon)

Requires:       libxkbcommon
Requires:       dbus-libs
Requires:       pipewire-libs
Requires:       pulseaudio-libs

%description
A customizable status bar for Wayland compositors, specifically designed for
Hyprland and Niri window managers. Features include workspace management,
system monitoring (CPU, RAM, temperature), audio controls, network management,
Bluetooth connectivity, battery status, and a settings panel.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release

%install
install -Dm755 target/release/ashell %{buildroot}%{_bindir}/ashell

%files
%license LICENSE
%doc README.md
%{_bindir}/ashell

%changelog
* Wed Jan 22 2025 Your Name <your.email@example.com> - 0.7.0-1
- Initial package for version 0.7.0
