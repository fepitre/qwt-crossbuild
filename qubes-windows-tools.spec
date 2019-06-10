
%define devbranch mingw
%define user marmarek

Name:		qubes-windows-tools
Version:	4.0
Release:	223
Summary:	Qubes Tools for Windows VMs
Group:		Qubes
License:	GPL
Obsoletes:	qubes-core-dom0-pvdrivers
BuildRequires:	genisoimage
BuildRequires:	mingw64-gcc
BuildRequires:	mingw64-winpthreads-static
BuildRequires:	mingw64-gcc-c++
BuildRequires:	wine
BuildRequires:	svn
BuildArch:	noarch
# Retrieve devcon tool from windows samples
# svn export https://github.com/microsoft/Windows-driver-samples/trunk/setup/devcon | tar -czvf devcon.tar.gz devcon
Source0:	devcon.tar.gz
# Get the latest qwt source tree
Source1:	https://codeload.github.com/marmarek/qubes-core-vchan-xen/zip/%{devbranch}#/qubes-core-vchan-xen-%{devbranch}.zip
Source2:	https://codeload.github.com/marmarek/qubes-core-agent-windows/zip/%{devbranch}#/qubes-core-agent-windows-%{devbranch}.zip
Source3:	https://codeload.github.com/marmarek/qubes-windows-utils/zip/%{devbranch}#/qubes-windows-utils-%{devbranch}.zip
Source4:	https://codeload.github.com/marmarek/qubes-core-qubesdb/zip/%{devbranch}#/qubes-core-qubesdb-%{devbranch}.zip
Source5:	https://codeload.github.com/marmarek/qubes-gui-common/zip/%{devbranch}#/qubes-gui-common-%{devbranch}.zip
Source6:	https://codeload.github.com/marmarek/qubes-gui-agent-windows/zip/%{devbranch}#/qubes-gui-agent-windows-%{devbranch}.zip
Source7:	https://codeload.github.com/marmarek/qubes-installer-qubes-os-windows-tools/zip/%{devbranch}#/qubes-installer-qubes-os-windows-tools-%{devbranch}.zip
Source8:	https://codeload.github.com/marmarek/qubes-vmm-xen-windows-pvdrivers/zip/%{devbranch}#/qubes-vmm-xen-windows-pvdrivers-%{devbranch}.zip
Source9:	https://codeload.github.com/marmarek/qubes-vmm-xen-win-pvdrivers-xeniface/zip/%{devbranch}#/qubes-vmm-xen-win-pvdrivers-xeniface-%{devbranch}.zip

Source10: 	https://raw.githubusercontent.com/llvm-mirror/compiler-rt/master/lib/builtins/assembly.h

# Add local sources
Source16:	disable_svc.bat
Source17:	pkihelper.c
#Source18:	qubes-tools.wxs
Source19:	diskpart.txt
Source100:	Makefile

# Download the latest stable xen binary drivers
Source21:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenbus.tar
Source22:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xeniface.tar
Source23:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenvif.tar
Source24:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xennet.tar
Source25:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenvbd.tar

patch0:         devcon-headers.patch

# remove confusing DriverEntry
#patch31:        qwt-gdi-fake-driverentry.patch

# remove CreateEvent from event processing loop
patch40:        qwt-gui-agent-cpu-usage.patch

# dirty
patch50:        qwt-xenvchan-test.patch
patch51:        qwt-vchan-test.patch

# build with inlined __chkstk_ms
patch52:	qwt-chkstk.patch

%prep
%setup -c
for i in $(ls %{_sourcedir}/qubes*.zip);
do unzip $i; done;
cat %{_sourcedir}/xen*.tar | tar -xvf - -i
cp -f %{S:100} %{S:16} %{S:19} ./
mkdir -p include

cp -f %{S:10} include

cp -f %{S:17} qubes-gui-agent-windows-*/install-helper/pkihelper/pkihelper.c

%autopatch -p1

%description
PV Drivers and Qubes Tools for Windows AppVMs.

%build

make all

cp -f /build/WixFragments/*.wxs ./
export WINEMU=wine; export WINEPREFIX=/opt/wine; export WINEARCH=win32
export WINEDEBUG=fixme-all; export WIXPATH=/opt/wix; export MSIOS=win7
export MSIARCH=x64; export WIN_BUILD_TYPE=chk; export DDK_ARCH=x64
export VERSION=4.0.0.0;
${WINEMU} ${WIXPATH}/candle.exe -arch ${DDK_ARCH} -ext WixDifxAppExtension -ext WixIIsExtension *.wxs;
${WINEMU} ${WIXPATH}/light.exe -sval *.wixobj -ext WixDifxAppExtension -ext WixUIExtension -ext WixIIsExtension -ext WixUtilExtension "Z:/opt/wix/difxapp_${DDK_ARCH}.wixlib" -o qubes-tools-${DDK_ARCH}.msi

mkdir -p iso-content
cp qubes-tools-${DDK_ARCH}.msi iso-content/
genisoimage -o qubes-windows-tools-%{version}.%{release}.iso -m .gitignore -JR iso-content

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/qubes/
cp qubes-windows-tools-%{version}.%{release}.iso $RPM_BUILD_ROOT/usr/lib/qubes/
ln -s qubes-windows-tools-%{version}.%{release}.iso $RPM_BUILD_ROOT/usr/lib/qubes/qubes-windows-tools.iso

%files
/usr/lib/qubes/qubes-windows-tools-%{version}.%{release}.iso
/usr/lib/qubes/qubes-windows-tools.iso

%changelog

