Name:           walker
Version:        2.7.5
Release:        1%{?dist}
Summary:        Fast, customizable Wayland application launcher

License:        GPL-3.0-or-later
URL:            https://github.com/abenz1267/walker
Source0:        %{url}/archive/v2.7.5/%{name}-%{version}.tar.gz

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
Walker is a fast, customizable application launcher built with GTK4 and Rust
for Wayland compositors. It provides multiple built-in providers including
application launching, calculator, file browser, command runner, clipboard
history, and more.

%prep
%autosetup -n %{name}-%{version}

%build
%cargo_build

%install
%cargo_install

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
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.7.5-1
- Update to 2.7.5

* Sun Oct 27 2024 Your Name <your.email@example.com> - 2.7.1-1
- Initial package for version 2.7.1
