%global debug_package %{nil}
%global forgeurl https://github.com/hyprwm/hyprutils

Name:           hyprutils
Version:        0.11.0
%forgemeta
Release:        1%{?dist}
Summary:        Hyprland utility library

License:        BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)

%description
A utility library used by Hyprland and related projects.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.

%prep
%forgeautosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libhyprutils.so.*

%files devel
%{_includedir}/hyprutils/
%{_libdir}/libhyprutils.so
%{_libdir}/pkgconfig/hyprutils.pc

%changelog
* Fri Feb 13 2026 Automated Update <noreply@github.com> - 0.11.0-1
- Initial package for version 0.11.0
