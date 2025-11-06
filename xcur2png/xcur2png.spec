%global debug_package %{nil}
%global build_type_safety_c 0
%global forgeurl https://github.com/eworm-de/xcur2png
%global tag %{version}

Name:           xcur2png
Version:        0.7.1
%forgemeta
Release:        2%{?dist}
Summary:        Convert X cursors to PNG images

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
Patch0:         0001-fix-wrong-math.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xcursor)

%description
Converts X cursor files to PNG images and generates xcursorgen config files.

%prep
%autosetup -n %{name}-%{version}

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
* Tue Nov 05 2024 Washkinazy <noreply@github.com> - 0.7.1-2
- Initial package for nwg-look dependency
