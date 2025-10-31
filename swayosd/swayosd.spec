%global origname SwayOSD
%global forgeurl https://github.com/ErikReider/SwayOSD

Name:           swayosd
Version:        0.2.1
%forgemeta
Release:        1%{?dist}
Summary:        A GTK based on screen display for keyboard shortcuts like caps-lock and volume

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        swayosd.sysusers

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  meson
BuildRequires:  gtk4-devel >= 4.0.0
BuildRequires:  glib2-devel
BuildRequires:  sassc
BuildRequires:  libudev-devel
BuildRequires:  libevdev-devel
BuildRequires:  atk-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  libinput-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  systemd

Requires:       gtk4
Requires:       gtk4-layer-shell
Requires:       libinput
Requires:       gdk-pixbuf2
Requires:       pango
Requires:       libevdev
Requires:       pulseaudio-libs
Requires:       systemd-libs
Requires:       glib2
Requires:       cairo
Requires:       dbus-libs

%description
A GTK based on-screen display (OSD) for common actions like volume changes,
brightness, caps-lock state, and other keyboard shortcuts in Wayland compositors.

%prep
%autosetup -n %{origname}-%{version}

%build
%meson
%meson_build

%install
%meson_install
rm -f %{buildroot}/usr/share/licenses/swayosd/LICENSE

%pre
%sysusers_create_compat %{SOURCE1}

%files
%license LICENSE
%doc README.md
%{_bindir}/swayosd-client
%{_bindir}/swayosd-libinput-backend
%{_bindir}/swayosd-server
%{_sysconfdir}/xdg/swayosd/backend.toml
%{_sysconfdir}/xdg/swayosd/config.toml
%{_sysconfdir}/xdg/swayosd/style.css
%{_unitdir}/swayosd-libinput-backend.service
%{_libdir}/udev/rules.d/99-swayosd.rules
%{_datadir}/dbus-1/system-services/org.erikreider.swayosd.service
%{_datadir}/dbus-1/system.d/org.erikreider.swayosd.conf
%{_datadir}/polkit-1/actions/org.erikreider.swayosd.policy
%{_datadir}/polkit-1/rules.d/org.erikreider.swayosd.rules

%changelog
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 0.2.1-1
- Update to 0.2.1

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 0.2.1-1
- Update to 0.2.1

* Sun Oct 27 2024 Your Name <your.email@example.com> - 0.2.1-1
- Update to version 0.2.1
- Latest stable release with bug fixes
