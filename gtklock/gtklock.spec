%global forgeurl https://github.com/jovanlanik/gtklock

Name:           gtklock
Version:        4.0.0
%forgemeta
Release:        1%{?dist}
Summary:        GTK-based lock screen for Wayland

License:        GPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  scdoc
BuildRequires:  gcc
BuildRequires:  /usr/bin/wayland-scanner
BuildRequires:  rpm_macro(_pam_confdir)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(gtk+-wayland-3.0)
BuildRequires:  pkgconfig(gtk-session-lock-0)
BuildRequires:  pkgconfig(gmodule-export-2.0)

%description
%{summary}

%prep
%forgeautosetup -p1

%build
%meson
%meson_build

%install
%meson_install
install -dm0755 %{buildroot}%{_libdir}/%{name}

%files
%{_bindir}/%{name}
%config(noreplace) %{_pam_confdir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_libdir}/%{name}
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%license LICENSE
%doc README.md

%changelog
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 4.0.0-1
- Update to 4.0.0

* Sun Oct 27 2024 Your Name <your.email@example.com> - 4.0.0-1
- Initial package for version 4.0.0
