%global forgeurl https://github.com/rharish101/ReGreet

Name:           regreet
Version:        0.2.0
%forgemeta
Release:        1%{?dist}
Summary:        Clean and customizable greeter for greetd

License:        GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        regreet.toml

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  gtk4-devel >= 4.0.0
BuildRequires:  glib2-devel
BuildRequires:  systemd-rpm-macros

Requires:       gtk4
Requires:       greetd
Provides:       greetd-greeter

%description
ReGreet is a clean and customizable GTK-based greeter for greetd, designed
for Wayland compositors. It provides a simple login interface with support
for session selection and user management.

%prep
%autosetup -n ReGreet-%{version}

%build
%cargo_build

%install
%cargo_install

# Install configuration file
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/greetd/regreet.toml

# Install sample configuration
install -Dm644 regreet.sample.toml %{buildroot}%{_docdir}/regreet/regreet.sample.toml

# Install systemd tmpfiles configuration
install -Dm644 systemd-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/regreet.conf

%files
%license LICENSES/*
%doc README.md
%doc %{_docdir}/regreet/regreet.sample.toml
%{_bindir}/regreet
%config(noreplace) %{_sysconfdir}/greetd/regreet.toml
%{_tmpfilesdir}/regreet.conf

%changelog
* Sun Oct 27 2024 Your Name <your.email@example.com> - 0.2.0-1
- Initial package for version 0.2.0
