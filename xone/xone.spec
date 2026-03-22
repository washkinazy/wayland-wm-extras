%global debug_package %{nil}
%global forgeurl https://github.com/dlundqvist/xone
%global commit f2aa9fe01103d7600553b505b298ff0bd47ff280
%global shortcommit f2aa9fe

Name:           xone
Version:        0.5.8^gitf2aa9fe
%forgemeta
Release:        1%{?dist}
Summary:        Linux kernel driver for Xbox One and Xbox Series X|S accessories

License:        GPL-2.0-only
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel
BuildRequires:  elfutils-libelf-devel

Requires:       dkms
Requires:       kernel-devel
Requires:       xone-firmware

Provides:       xone-kmod = %{version}-%{release}

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S accessories.
It serves as a modern replacement for xpad, providing support for Xbox
wireless dongles, wired controllers, chatpads, headsets, and third-party
accessories from MadCatz and PDP.

%prep
%autosetup -n xone-%{commit}

%build
# DKMS modules are built at install time, nothing to build here

%install
# Install DKMS source tree
install -d %{buildroot}%{_usrsrc}/%{name}-%{version}
cp -a auth bus driver transport Kbuild Makefile dkms.conf %{buildroot}%{_usrsrc}/%{name}-%{version}/

# Stamp version into dkms.conf and source files
sed -i 's/#VERSION#/%{version}/g' %{buildroot}%{_usrsrc}/%{name}-%{version}/dkms.conf
find %{buildroot}%{_usrsrc}/%{name}-%{version} -name '*.c' -exec sed -i 's/#VERSION#/%{version}/g' {} +

# Install modprobe blacklist
install -D -m 644 install/modprobe.conf %{buildroot}/usr/lib/modprobe.d/xone-blacklist.conf

%post
dkms add -m %{name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{name} -v %{version} || :
dkms install -m %{name} -v %{version} --force || :

%preun
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{name}-%{version}/
/usr/lib/modprobe.d/xone-blacklist.conf

%changelog
* Sun Mar 22 2026 Automated Update <noreply@github.com> - 0.5.8^gitf2aa9fe-1
- Initial package tracking master branch
