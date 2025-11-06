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
xcur2png is a program which let you take PNG image from X cursor, and generate
config-file which is reusable by xcursorgen. To put it simply, it is
converter from X cursor to PNG image.

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
