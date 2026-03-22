%global debug_package %{nil}
%global commit f2aa9fe01103d7600553b505b298ff0bd47ff280
%global shortcommit f2aa9fe

Name:           xone-firmware
Version:        0.5.8^gitf2aa9fe
Release:        1%{?dist}
Summary:        Firmware for Xbox One wireless dongle (xone driver)

License:        Redistributable, no modification permitted
URL:            https://github.com/dlundqvist/xone

# Firmware .cab files from Microsoft Windows Update catalog
Source0:        https://catalog.s.download.windowsupdate.com/d/msdownload/update/driver/drvs/2017/03/2ea9591b-f751-442c-80ce-8f4692cdc67b_6b555a3a288153cf04aec6e03cba360afe2fce34.cab
Source1:        https://catalog.s.download.windowsupdate.com/c/msdownload/update/driver/drvs/2017/07/1cd6a87c-623f-4407-a52d-c31be49e925c_e19f60808bdcbfbd3c3df6be3e71ffc52e43261e.cab
Source2:        https://catalog.s.download.windowsupdate.com/c/msdownload/update/driver/drvs/2017/06/1dbd7cb4-53bc-4857-a5b0-5955c8acaf71_9081931e7d664429a93ffda0db41b7545b7ac257.cab
Source3:        https://catalog.s.download.windowsupdate.com/d/msdownload/update/driver/drvs/2017/08/aeff215c-3bc4-4d36-a3ea-e14bfa8fa9d2_e58550c4f74a27e51e5cb6868b10ff633fa77164.cab

BuildRequires:  bsdtar

BuildArch:      noarch

Supplements:    xone

%description
Firmware files for the Xbox One wireless dongle, required by the xone
kernel driver for wireless controller support. The firmware is subject
to Microsoft's Terms of Use: https://www.microsoft.com/en-us/legal/terms-of-use

%prep
# Extract firmware binaries from each .cab
bsdtar -xf %{SOURCE0} FW_ACC_00U.bin
sha256sum -c - <<'EOF'
080ce4091e53a4ef3e5fe29939f51fd91f46d6a88be6d67eb6e99a5723b3a223  FW_ACC_00U.bin
EOF
mv FW_ACC_00U.bin xone_dongle_02e6.bin

bsdtar -xf %{SOURCE1} FW_ACC_00U.bin
sha256sum -c - <<'EOF'
48084d9fa53b9bb04358f3bb127b7495dc8f7bb0b3ca1437bd24ef2b6eabdf66  FW_ACC_00U.bin
EOF
mv FW_ACC_00U.bin xone_dongle_02fe.bin

bsdtar -xf %{SOURCE2} FW_ACC_CL.bin
sha256sum -c - <<'EOF'
0023a7bae02974834500c665a281e25b1ba52c9226c84989f9084fa5ce591d9b  FW_ACC_CL.bin
EOF
mv FW_ACC_CL.bin xone_dongle_02f9.bin

bsdtar -xf %{SOURCE3} FW_ACC_BR.bin
sha256sum -c - <<'EOF'
e2710daf81e7b36d35985348f68a81d18bc537a2b0c508ffdfde6ac3eae1bad7  FW_ACC_BR.bin
EOF
mv FW_ACC_BR.bin xone_dongle_091e.bin

%build
# Firmware binaries, nothing to build

%install
install -d %{buildroot}%{_prefix}/lib/firmware
install -m 644 xone_dongle_02e6.bin %{buildroot}%{_prefix}/lib/firmware/
install -m 644 xone_dongle_02fe.bin %{buildroot}%{_prefix}/lib/firmware/
install -m 644 xone_dongle_02f9.bin %{buildroot}%{_prefix}/lib/firmware/
install -m 644 xone_dongle_091e.bin %{buildroot}%{_prefix}/lib/firmware/

%files
%{_prefix}/lib/firmware/xone_dongle_02e6.bin
%{_prefix}/lib/firmware/xone_dongle_02fe.bin
%{_prefix}/lib/firmware/xone_dongle_02f9.bin
%{_prefix}/lib/firmware/xone_dongle_091e.bin

%changelog
* Sun Mar 22 2026 Automated Update <noreply@github.com> - 0.5.8^gitf2aa9fe-1
- Initial package tracking master branch
