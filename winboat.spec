# WinBoat is an Electron application. Rather than rebuilding it from source
# (which requires Bun, Go and a ~100MB Electron download and is fragile in a
# mock/COPR environment), this spec repackages the official prebuilt
# "linux-unpacked" tarball published on GitHub releases.

Name:           winboat
Version:        0.9.0
Release:        1%{?dist}
Summary:        Windows for Penguins - run Windows apps on Linux

License:        MIT
URL:            https://github.com/easton57/winboat
%ifarch x86_64
%global upstream_arch x64
%endif
%ifarch aarch64
%global upstream_arch arm64
%endif
Source0:        https://github.com/easton57/winboat/releases/download/v%{version}/%{name}-%{version}-%{upstream_arch}.tar.gz
# Application icon, taken from the tagged source tree.
Source1:        https://github.com/easton57/winboat/raw/v%{version}/icons/winboat_logo.svg
# MIT license text, taken from the tagged source tree.
Source2:        https://github.com/easton57/winboat/raw/v%{version}/LICENSE

# No build-time dependencies beyond the standard toolchain (tar).
BuildRequires:  tar

# The app bundles its own Electron runtime, so we disable automatic
# requirement generation (the bundled .so files would otherwise generate
# bogus dependencies on system libraries) and declare the real runtime
# libraries explicitly.
AutoReq:        no
Requires:       alsa-lib
Requires:       at-spi2-atk
Requires:       at-spi2-core
Requires:       atk
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       fontconfig
Requires:       freetype
Requires:       glib2
Requires:       gtk3
Requires:       libX11
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXrandr
Requires:       libXrender
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       libdrm
Requires:       libnotify
Requires:       libxcb
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango

# WinBoat composites Windows apps as native windows via FreeRDP.
Requires:       freerdp

# Indicate that we ship our own Electron copy.
Provides:       bundled(electron) = 43

ExclusiveArch:  x86_64 aarch64

%description
WinBoat is an Electron app that lets you run Windows applications on Linux
using a containerized approach. Windows runs as a VM inside a Docker/Podman
container and is reached through the WinBoat Guest Server; applications are
composited as native OS-level windows using FreeRDP and the RemoteApp protocol.

This package repackages the official upstream prebuilt Linux binary.

%prep
%setup -q -n %{name}-%{version}-%{upstream_arch}

%build
# Prebuilt upstream artifact - nothing to compile.

%install
# Install the whole unpacked application under /opt/winboat.
mkdir -p %{buildroot}/opt/%{name}
cp -a ./* %{buildroot}/opt/%{name}/

# Make the launcher and the Chromium sandbox executable.
chmod 0755 %{buildroot}/opt/%{name}/%{name}
chmod 4755 %{buildroot}/opt/%{name}/chrome-sandbox

# Wrapper that launches the bundled binary from its own directory so it can
# locate its resources/ directory.
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/bin/sh
cd /opt/%{name}
exec /opt/%{name}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Desktop entry.
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=WinBoat
Comment=Windows for Penguins
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Utility;
Keywords=windows;remote;rdp;wine;
EOF

# Icon.
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files
%license %{SOURCE2}
%doc LICENSE.electron.txt LICENSES.chromium.html
/opt/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Wed Aug 26 2026 WinBoat Maintainers <staff@winboat.app> - 0.9.2-1
- Repackage upstream WinBoat 0.9.2 prebuilt Linux binary.
