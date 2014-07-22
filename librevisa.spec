#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open-source VISA library for GPIB/USBTMC/LXI
Summary(pl.UTF-8):	Mająca otwarte źródła biblioteka VISA dla urządzeń GPIB/USBTMC/LXI
Name:		librevisa
Version:	0.0.20130812
Release:	1
License:	GPL v3+
Group:		Libraries
# upstream (pre)releases
#Source0:	http://www.librevisa.org/download/%{name}-%{version}.tar.gz
# for now we need newer snapshot, (ab)use debian's ftp
Source0:	http://ftp.debian.org/debian/pool/main/libr/librevisa/%{name}_%{version}.orig.tar.gz
# Source0-md5:	d403b6926ba733df7e13a374c94e0b38
URL:		http://www.librevisa.org/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake >= 1:1.10
BuildRequires:	avahi-devel >= 0.6
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0.8
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	vxi-devel
Requires:	libusb >= 1.0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The VISA API provides a common interface to test and measurement
equipment that can be accessed via GPIB, USB or VXI-11 interfaces.

%description -l pl.UTF-8
VISA API dostarcza ogólny interfejs do urządzeń testowych i
pomiarowych, z którymi można łączyć się przez interfejsy GPIB, USB
albo VXI-11.

%package devel
Summary:	Header files for VISA library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki VISA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-devel >= 0.6
Requires:	libusb-devel >= 1.0.6

%description devel
Header files for VISA library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki VISA.

%package static
Summary:	Static VISA library
Summary(pl.UTF-8):	Statyczna biblioteka VISA
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static VISA library.

%description static -l pl.UTF-8
Statyczna biblioteka VISA.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# fake AC_CHECK_LIB([vxiclient], [create_link_1]) success
# (simple AC_CHECK_LIB won't succeed on shared library requiring application symbols)
%configure \
	ac_cv_lib_vxiclient_create_link_1=yes \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvisa.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvisa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvisa.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvisa.so
%{_includedir}/visa.h
%{_includedir}/visatype.h
%{_pkgconfigdir}/librevisa.pc
%{_mandir}/man3/viClose.3visa*
%{_mandir}/man3/viOpenDefaultRM.3visa*
%{_mandir}/man7/visa.7visa*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvisa.a
%endif
