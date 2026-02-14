%global debug_package %{nil}
%global forgeurl https://github.com/hyprwm/hyprlang

Name:           hyprlang
Version:        0.6.8
%forgemeta
Release:        1%{?dist}
Summary:        Hyprland configuration language library

License:        LGPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils) >= 0.7.1

%description
A configuration language library used by Hyprland and related projects.

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
%{_libdir}/libhyprlang.so.*

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc

%changelog
* Fri Feb 13 2026 Automated Update <noreply@github.com> - 0.6.8-1
- Initial package for version 0.6.8
