%global debug_package %{nil}
%global forgeurl https://github.com/nwg-piotr/nwg-look

Name:           nwg-look
Version:        1.0.6
%forgemeta
Release:        1%{?dist}
Summary:        GTK3 settings editor for Wayland compositors

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  golang >= 1.21
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  desktop-file-utils

Requires:       /usr/bin/gsettings
Requires:       xcur2png

%description
nwg-look is a GTK3 settings editor adapted to work in the wlroots-based
Wayland compositors. It provides an interface for managing GTK themes,
icons, cursor themes, and other GTK settings.

%prep
%autosetup -n %{name}-%{version}

%build
# Build with online access to fetch dependencies
go build -buildvcs=false -trimpath -mod=readonly -o %{name}

%install
# Install binary
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

# Install data files
install -Dm644 stuff/main.glade %{buildroot}%{_datadir}/%{name}/main.glade

# Install language files
for lang_file in langs/*.json; do
    install -Dm644 "$lang_file" %{buildroot}%{_datadir}/%{name}/langs/$(basename "$lang_file")
done

# Install desktop file
install -Dm644 stuff/nwg-look.desktop %{buildroot}%{_datadir}/applications/nwg-look.desktop

# Install icon
install -Dm644 stuff/nwg-look.svg %{buildroot}%{_datadir}/pixmaps/nwg-look.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/nwg-look.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/nwg-look.desktop
%{_datadir}/pixmaps/nwg-look.svg

%changelog
* Tue Nov 05 2024 Washkinazy <noreply@github.com> - 1.0.6-1
- Initial package for version 1.0.6
