%global forgeurl https://github.com/ryanoasis/nerd-fonts

Name:           nerd-fonts-firacode
Version:        3.4.0
Release:        1%{?dist}
Summary:        FiraCode font patched with programming glyphs from Nerd Fonts

BuildArch:      noarch

License:        OFL-1.1-no-RFN
URL:            %{forgeurl}
Source0:        %{forgeurl}/releases/download/v%{version}/FiraCode.zip

%description
FiraCode monospaced font patched with Nerd Fonts icon glyphs.

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
