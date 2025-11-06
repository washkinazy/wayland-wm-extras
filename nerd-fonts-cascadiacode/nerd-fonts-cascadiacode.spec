%global debug_package %{nil}
%global forgeurl https://github.com/ryanoasis/nerd-fonts

Name:           nerd-fonts-cascadiacode
Version:        3.4.0
Release:        2%{?dist}
Summary:        Cascadia Code font patched with programming glyphs from Nerd Fonts

BuildArch:      noarch

License:        OFL-1.1-RFN
URL:            %{forgeurl}
Source0:        %{forgeurl}/releases/download/v%{version}/CascadiaCode.zip

BuildRequires:  unzip
Requires(post): fontconfig
Requires(postun): fontconfig

%description
Cascadia Code monospaced font patched with Nerd Fonts icon glyphs.
Renamed to CaskaydiaCove per OFL Reserved Font Name requirements.

%prep
%autosetup -c

%install
# Install fonts
install -d %{buildroot}%{_datadir}/fonts/%{name}
install -m 0644 *.ttf %{buildroot}%{_datadir}/fonts/%{name}/ || true
install -m 0644 *.otf %{buildroot}%{_datadir}/fonts/%{name}/ || true

%post
/usr/bin/fc-cache -f %{_datadir}/fonts/%{name} &>/dev/null || :

%postun
/usr/bin/fc-cache -f %{_datadir}/fonts/%{name} &>/dev/null || :

%files
%{_datadir}/fonts/%{name}/

%changelog
* Wed Jan 08 2025 Washkinazy <noreply@github.com> - 3.4.0-2
- Add unzip BuildRequires
- Add fontconfig Requires for proper font cache handling
- Remove non-existent README.md from files

* Tue Nov 05 2024 Washkinazy <noreply@github.com> - 3.4.0-1
- Initial package for version 3.4.0
