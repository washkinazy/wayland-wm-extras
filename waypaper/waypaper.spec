%global forgeurl https://github.com/anufrievroman/waypaper

Name:           waypaper
Version:        2.7
Release:        1%{?dist}
Summary:        GUI wallpaper setter for Wayland

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/refs/tags/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel

Recommends:     swww

%description
GUI wallpaper setter for Wayland and Xorg window managers. It works as
a frontend for popular wallpaper backends like swaybg, swww, wallutils and feh.

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files waypaper

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/waypaper
%{_datadir}/applications/waypaper.desktop
%{_datadir}/icons/hicolor/scalable/apps/waypaper.svg
%{_datadir}/man/man1/waypaper.1.*

%changelog
* Tue Nov 05 2024 Automated Update <noreply@github.com> - 2.7-1
- Initial package for version 2.7