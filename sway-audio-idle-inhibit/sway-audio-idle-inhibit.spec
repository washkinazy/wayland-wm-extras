%global forgeurl https://github.com/ErikReider/SwayAudioIdleInhibit

Name:           sway-audio-idle-inhibit
Version:        0.2.0
%forgemeta
Release:        1%{?dist}
Summary:        Prevents swayidle from sleeping while audio is in use

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-client) >= 1.14.91
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)

%description
Prevents swayidle from sleeping while any application
is outputting or receiving audio. Should work with all Wayland
desktops that support the zwp_idle_inhibit_manager_v1
protocol but only tested in Sway.

This only works for Pulseaudio / Pipewire Pulse.

%prep
%forgeautosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%changelog
* Sun Oct 27 2024 Your Name <your.email@example.com> - 0.2.0-1
- Initial package for version 0.2.0
