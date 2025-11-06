%global debug_package %{nil}
%global forgeurl https://github.com/rr-/screeninfo

Name:           python-screeninfo
Version:        0.8.1
Release:        1%{?dist}
Summary:        Fetch location and size of physical screens

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/%{version}/screeninfo-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%global _description %{expand:
Fetch location and size of physical screens.}

%description %_description

%package -n python3-screeninfo
Summary:        %{summary}

%description -n python3-screeninfo %_description

%prep
%autosetup -p1 -n screeninfo-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files screeninfo

%check
%pytest

%files -n python3-screeninfo -f %{pyproject_files}
%doc README.md
%license LICENSE.md

%changelog
* Tue Nov 05 2024 Automated Update <noreply@github.com> - 0.8.1-1
- Initial package for version 0.8.1
