%global debug_package %{nil}
%global forgeurl https://github.com/jovanlanik/gtklock-userinfo-module

Name:           gtklock-userinfo-module
Version:        4.0.1
%forgemeta
Release:        1%{?dist}
Summary:        Gtklock module adding user info to the lock screen

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(accountsservice)

Requires:       gtklock%{?_isa} >= 3.0.0

Supplements:    gtklock%{?_isa}

%description
%{summary}

%prep
%forgeautosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%{_libdir}/gtklock/*.so
%license LICENSE
%doc README.md

%changelog
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 4.0.1-1
- Update to 4.0.1

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 4.0.1-1
- Update to 4.0.1

* Sun Oct 27 2024 Your Name <your.email@example.com> - 4.0.1-1
- Initial package for version 4.0.1
