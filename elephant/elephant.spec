%global debug_package %{nil}

Name:           elephant
Version:        2.9.3
Release:        1%{?dist}
Summary:        Data provider service for Walker launcher

License:        GPL-3.0-or-later
URL:            https://github.com/abenz1267/elephant
Source0:        %{url}/archive/v2.9.3/%{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.21
BuildRequires:  git-core
BuildRequires:  protobuf-compiler
BuildRequires:  systemd-rpm-macros
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

Requires:       systemd

%description
Elephant is a data provider service that supplies information to the Walker
launcher. It provides plugins for various data sources including applications,
clipboard history, Bluetooth devices, and more.

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
* Fri Oct 31 2025 Automated Update <noreply@github.com> - 2.9.3-1
- Update to 2.9.3

* Sun Oct 27 2024 Your Name <your.email@example.com> - 2.7.7-1
- Initial package for version 2.7.7
