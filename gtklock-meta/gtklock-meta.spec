%global debug_package %{nil}

Name:           gtklock-meta
Version:        1.0
Release:        1%{?dist}
Summary:        Meta package to install gtklock with all modules

License:        MIT
URL:            https://github.com/jovanlanik/gtklock
BuildArch:      noarch

Requires:       gtklock
Requires:       gtklock-playerctl-module
Requires:       gtklock-powerbar-module
Requires:       gtklock-userinfo-module

%description
Meta package that installs gtklock along with all available modules:
- gtklock: GTK-based lockscreen for Wayland
- gtklock-playerctl-module: Media player control module
- gtklock-powerbar-module: Power/session control module
- gtklock-userinfo-module: User information display module

%files
%doc

%changelog
* Wed Jan 08 2025 Washkinazy <noreply@github.com> - 1.0-1
- Initial meta package for gtklock with all modules
