%global debug_package %{nil}
%global forgeurl https://github.com/hyprwm/hyprwayland-scanner

Name:           hyprwayland-scanner
Version:        0.4.5
%forgemeta
Release:        1%{?dist}
Summary:        Wayland protocol scanner for Hyprland

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pugixml-devel

%description
A Wayland protocol scanner that generates C++ code for Hyprland projects.

%prep
%forgeautosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprwayland-scanner
%{_datadir}/pkgconfig/hyprwayland-scanner.pc
%{_libdir}/cmake/hyprwayland-scanner/

%changelog
* Fri Feb 13 2026 Automated Update <noreply@github.com> - 0.4.5-1
- Initial package for version 0.4.5
