%global debug_package %{nil}
%global forgeurl https://github.com/abenz1267/walker

Name:           walker
Version:        2.14.2
%forgemeta
Release:        1%{?dist}
Summary:        Fast, customizable Wayland application launcher

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  gtk4-devel >= 4.6.0
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  glib2-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  protobuf-compiler

Requires:       gtk4
Requires:       gtk4-layer-shell
Requires:       poppler-glib
Requires:       cairo
Requires:       glib2
Requires:       elephant

%description
Application launcher for Wayland compositors with built-in providers for
applications, calculator, file browser, command runner, and clipboard history.

%prep
%autosetup -n %{name}-%{version}

%build
# Build with online access to fetch dependencies from crates.io
cargo build --release

%install
install -Dm755 target/release/walker %{buildroot}%{_bindir}/walker

# Install configuration files
install -Dm644 resources/config.toml %{buildroot}%{_sysconfdir}/xdg/walker/config.toml

# Install theme files
mkdir -p %{buildroot}%{_sysconfdir}/xdg/walker/themes/default
install -Dm644 resources/themes/default/*.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/
install -Dm644 resources/themes/default/*.css %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/

%files
%license LICENSE
%doc README.md
%{_bindir}/walker
%dir %{_sysconfdir}/xdg/walker
%config(noreplace) %{_sysconfdir}/xdg/walker/config.toml
%dir %{_sysconfdir}/xdg/walker/themes
%dir %{_sysconfdir}/xdg/walker/themes/default
%{_sysconfdir}/xdg/walker/themes/default/*.xml
%{_sysconfdir}/xdg/walker/themes/default/*.css

%changelog
* Sun Feb 15 2026 Automated Update <noreply@github.com> - 2.14.2-1
- Update to 2.14.2

* Fri Jan 23 2026 Automated Update <noreply@github.com> - 2.14.1-1
- Update to 2.14.1

* Thu Jan 22 2026 Automated Update <noreply@github.com> - 2.14.0-1
- Update to 2.14.0

* Fri Jan 09 2026 Automated Update <noreply@github.com> - 2.13.0-1
- Update to 2.13.0

* Wed Dec 10 2025 Automated Update <noreply@github.com> - 2.12.2-1
- Update to 2.12.2

* Tue Dec 09 2025 Automated Update <noreply@github.com> - 2.12.1-1
- Update to 2.12.1

* Sun Dec 07 2025 Automated Update <noreply@github.com> - 2.12.0-1
- Update to 2.12.0

* Fri Nov 28 2025 Automated Update <noreply@github.com> - 2.11.3-1
- Update to 2.11.3

* Sat Nov 22 2025 Automated Update <noreply@github.com> - 2.11.2-1
- Update to 2.11.2

* Wed Nov 19 2025 Automated Update <noreply@github.com> - 2.11.1-1
- Update to 2.11.1

* Tue Nov 11 2025 Automated Update <noreply@github.com> - 2.10.0-1
- Update to 2.10.0

* Thu Nov 06 2025 Automated Update <noreply@github.com> - 2.9.3-1
- Update to 2.9.3

* Sat Nov 01 2025 Automated Update <noreply@github.com> - 2.8.0-1
- Update to 2.8.0

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.7.5-1
- Update to 2.7.5

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.7.5-1
- Update to 2.7.5

* Sun Oct 27 2024 Your Name <your.email@example.com> - 2.7.1-1
- Initial package for version 2.7.1
