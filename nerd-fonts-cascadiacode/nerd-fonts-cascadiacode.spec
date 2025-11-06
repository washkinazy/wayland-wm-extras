%global forgeurl https://github.com/ryanoasis/nerd-fonts

Name:           nerd-fonts-cascadiacode
Version:        3.4.0
Release:        1%{?dist}
Summary:        Cascadia Code font patched with programming glyphs from Nerd Fonts

BuildArch:      noarch

License:        OFL-1.1-RFN
URL:            %{forgeurl}
Source0:        %{forgeurl}/releases/download/v%{version}/CascadiaCode.zip

%description
Cascadia Code is a monospaced font designed by Microsoft for the Windows Terminal
and modern development environments. This version has been patched with additional
glyphs from Nerd Fonts, including icons from Font Awesome, Devicons, Octicons,
Powerline, and many more. The patched version is renamed to "CaskaydiaCove" to
comply with OFL Reserved Font Name requirements.

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
%doc README.md
%{_datadir}/fonts/%{name}/

%changelog
* Tue Nov 05 2024 Washkinazy <noreply@github.com> - 3.4.0-1
- Initial package for version 3.4.0
