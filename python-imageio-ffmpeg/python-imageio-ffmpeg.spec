%global debug_package %{nil}
%global forgeurl https://github.com/imageio/imageio-ffmpeg

Name:           python-imageio-ffmpeg
Version:        0.6.0
Release:        1%{?dist}
Summary:        FFMPEG wrapper for Python

License:        BSD-2-Clause
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/v%{version}/imageio-ffmpeg-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global _description %{expand:
FFMPEG wrapper for Python.}

%description %_description

%package -n python3-imageio-ffmpeg
Summary:        %{summary}
Requires:       /usr/bin/ffmpeg

%description -n python3-imageio-ffmpeg %_description

%prep
%autosetup -p1 -n imageio-ffmpeg-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-imageio-ffmpeg
%doc README.md
%license LICENSE
%{python3_sitelib}/imageio_ffmpeg-*.egg-info/
%{python3_sitelib}/imageio_ffmpeg/

%changelog
* Tue Nov 05 2024 Automated Update <noreply@github.com> - 0.6.0-1
- Initial package for version 0.6.0
