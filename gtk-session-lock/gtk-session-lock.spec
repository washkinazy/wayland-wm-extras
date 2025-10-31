%global forgeurl https://github.com/Cu3PO42/gtk-session-lock

Name:           gtk-session-lock
Version:        0.2.0
%forgemeta
Release:        1%{?dist}
Summary:        Library to create screen lockers for Wayland using ext-session-lock

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gtk3-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala

Requires:       gtk3

%description
gtk-session-lock is a library to create screen lockers for Wayland compositors
using the ext-session-lock-v1 protocol. It provides GTK3 bindings for building
lock screens with proper Wayland session lock support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files and headers for building applications using gtk-session-lock.

%prep
%forgeautosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE_GPL.txt LICENSE_MIT.txt
%doc README.md
%{_libdir}/libgtk-session-lock.so.0*
%{_libdir}/girepository-1.0/GtkSessionLock-0.1.typelib

%files devel
%{_includedir}/gtk-session-lock/
%{_libdir}/libgtk-session-lock.so
%{_libdir}/pkgconfig/gtk-session-lock-0.pc
%{_datadir}/gir-1.0/GtkSessionLock-0.1.gir
%{_datadir}/vala/vapi/gtk-session-lock-0.deps
%{_datadir}/vala/vapi/gtk-session-lock-0.vapi

%changelog
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 0.2.0-1
- Update to 0.2.0

* Sun Oct 27 2024 Your Name <your.email@example.com> - 0.2.0-2
- Initial package for version 0.2.0
