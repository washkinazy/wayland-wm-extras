%global debug_package %{nil}
%global forgeurl https://github.com/hyprwm/hyprland-protocols

Name:           hyprland-protocols
Version:        0.7.0
%forgemeta
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch
BuildRequires:  cmake

%description
Wayland protocol extensions used by Hyprland and related tools.

%prep
%forgeautosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_datadir}/hyprland-protocols/
%{_datadir}/pkgconfig/hyprland-protocols.pc

%changelog
* Fri Feb 13 2026 Automated Update <noreply@github.com> - 0.7.0-1
- Initial package for version 0.7.0
