%global debug_package %{nil}
%global forgeurl https://github.com/hyprwm/hypridle

Name:           hypridle
Version:        0.1.7
%forgemeta
Release:        1%{?dist}
Summary:        Hyprland idle daemon

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  hyprwayland-scanner >= 0.4.4
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(sdbus-c++) >= 0.2.0

%description
An idle daemon for Hyprland that monitors user activity and triggers actions
such as screen locking or display power management.

%prep
%forgeautosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE
%{_bindir}/hypridle
%{_userunitdir}/hypridle.service

%changelog
* Fri Feb 13 2026 Automated Update <noreply@github.com> - 0.1.7-1
- Initial package for version 0.1.7
