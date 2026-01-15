%global debug_package %{nil}
%global forgeurl https://github.com/abenz1267/elephant

Name:           elephant
Version:        2.18.2
%forgemeta
Release:        1%{?dist}
Summary:        Data provider service for Walker launcher

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  golang >= 1.21
BuildRequires:  git-core
BuildRequires:  protobuf-compiler
BuildRequires:  systemd-rpm-macros
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

Requires:       systemd

%description
Data provider service for Walker launcher with plugins for applications,
clipboard history, and Bluetooth devices.

%prep
%autosetup -n %{name}-%{version}

%build
# Build main binary
cd cmd/elephant
go build -buildvcs=false -trimpath -o elephant
cd ../..

# Build all provider plugins
mkdir -p _build/providers
for provider_dir in internal/providers/*/; do
    if [ -f "${provider_dir}/makefile" ]; then
        provider_name=$(basename "$provider_dir")
        echo "Building provider: $provider_name"
        (cd "$provider_dir" && make build)
        cp "${provider_dir}/${provider_name}.so" "_build/providers/"
    fi
done

%install
# Install main binary
install -Dm755 cmd/elephant/elephant %{buildroot}%{_bindir}/elephant

# Install provider plugins
mkdir -p %{buildroot}%{_sysconfdir}/xdg/elephant/providers
install -Dm755 _build/providers/*.so %{buildroot}%{_sysconfdir}/xdg/elephant/providers/

%files
%license LICENSE
%doc README.md
%{_bindir}/elephant
%dir %{_sysconfdir}/xdg/elephant
%dir %{_sysconfdir}/xdg/elephant/providers
%{_sysconfdir}/xdg/elephant/providers/*.so

%changelog
* Thu Jan 15 2026 Automated Update <noreply@github.com> - 2.18.2-1
- Update to 2.18.2

* Sat Jan 10 2026 Automated Update <noreply@github.com> - 2.18.1-1
- Update to 2.18.1

* Fri Jan 09 2026 Automated Update <noreply@github.com> - 2.18.0-1
- Update to 2.18.0

* Mon Dec 15 2025 Automated Update <noreply@github.com> - 2.17.2-1
- Update to 2.17.2

* Tue Dec 09 2025 Automated Update <noreply@github.com> - 2.17.1-1
- Update to 2.17.1

* Sun Dec 07 2025 Automated Update <noreply@github.com> - 2.17.0-1
- Update to 2.17.0

* Sat Nov 22 2025 Automated Update <noreply@github.com> - 2.16.1-1
- Update to 2.16.1

* Wed Nov 19 2025 Automated Update <noreply@github.com> - 2.16.0-1
- Update to 2.16.0

* Tue Nov 11 2025 Automated Update <noreply@github.com> - 2.15.0-1
- Update to 2.15.0

* Sun Nov 09 2025 Automated Update <noreply@github.com> - 2.14.4-1
- Update to 2.14.4

* Fri Nov 07 2025 Automated Update <noreply@github.com> - 2.14.3-1
- Update to 2.14.3

* Wed Jan 08 2025 Manual Update <noreply@github.com> - 2.10.4-1
- Temporary downgrade to 2.10.4 for Fedora 42 compatibility (Go 1.24.9)
- Version 2.14.3+ requires Go 1.25.0+

* Sat Nov 01 2025 Automated Update <noreply@github.com> - 2.10.4-1
- Update to 2.10.4

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.9.3-1
- Update to 2.9.3

* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.9.3-1
- Update to 2.9.3

* Sun Oct 27 2024 Your Name <your.email@example.com> - 2.7.7-1
- Initial package for version 2.7.7
