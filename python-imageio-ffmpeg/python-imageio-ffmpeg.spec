%global debug_package %{nil}
%global forgeurl https://github.com/imageio/imageio-ffmpeg

Name:           python-imageio-ffmpeg
Version:        0.6.0
Release:        2%{?dist}
Summary:        FFMPEG wrapper for Python

License:        BSD-2-Clause
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/v%{version}/imageio-ffmpeg-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
FFMPEG wrapper for Python.}

%description %_description

%package -n python3-imageio-ffmpeg
Summary:        %{summary}
Requires:       /usr/bin/ffmpeg

%description -n python3-imageio-ffmpeg %_description

%prep
%autosetup -p1 -n imageio-ffmpeg-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files imageio_ffmpeg

%check
%pyproject_check_import

%files -n python3-imageio-ffmpeg -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Sun Oct 25 2026 Washkinazy <noreply@github.com> - 0.6.0-2
- Build with pyproject macros and check imports

* Tue Nov 05 2024 Automated Update <noreply@github.com> - 0.6.0-1
- Initial package for version 0.6.0
