Name:           winboat
Version:        0.9.0
Release:        1%{?dist}
Summary:        <one line>
License:        <SPDX id>
URL:            https://github.com/easton57/winboat
Source0:        %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  bun
Requires:       bun

%description
<longer description>

%prep
%autosetup -n %{name}-%{version}

%build
export HOME=%{_builddir}
bun install --frozen-lockfile
bun run build:linux-gs

%install
install -d %{buildroot}%{_libdir}/%{name}
cp -r dist/* %{buildroot}%{_libdir}/%{name}/
install -Dm755 %{_builddir}/%{name}-%{version}/launcher.sh %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_libdir}/%{name}

%changelog
* Fri Aug 28 2026 Easton Seidel <eastonseidel@proton.me> - 0.9.0
- Initial package