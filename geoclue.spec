%define		gitrev	50861a3ef3ba08707e4180504b8ab94421c5595c

Summary:	A modular geoinformation service
Name:		geoclue
Version:	0.12.0
%if "%{gitver}" != "%{nil}"
Release:	0.%{gitrev}.2
Source0:	http://cgit.freedesktop.org/geoclue/snapshot/geoclue-%{gitrev}.tar.gz
# Source0-md5:	d3b3f868bf97f477c8f630c8a21a5f71
%else
Release:	1
Source0:	http://folks.o-hand.com/jku/geoclue-releases/%{name}-%{version}.tar.gz
# Source0-md5:	d3b3f868bf97f477c8f630c8a21a5f71
%endif
License:	LGPL v2
Group:		Applications
URL:		http://geoclue.freedesktop.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib-gio-gsettings
BuildRequires:	gtk+-devel
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	glib-gio-gsettings
Requires:	dbus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/geoclue

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system. The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%package libs
Summary:	Geoclue modular geoinformation service library
Group:		Libraries

%description libs
geoclue modular geoinformation service library.

%package devel
Summary:	Development package for geoclue
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for development with geoclue.

%package apidocs
Summary:	Developer documentation for geoclue
Group:		Development/Libraries
Requires:	gtk-doc-common

%description apidocs
Developer documentation for geoclue.

%package provider-gypsy
Summary:	Gypsy provider for geoclue
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gypsy

%description provider-gypsy
A gypsy provider for geoclue.

%prep
%if "%{gitver}" != "%{nil}"
%setup -qn %{name}-%{gitrev}
%else
%setup -q
%endif

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--enable-conic=no		\
	--enable-gpsd=no		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%{_datadir}/GConf/gsettings/geoclue
%{_datadir}/glib-2.0/schemas/org.freedesktop.Geoclue.gschema.xml
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/geoclue-example
%attr(755,root,root) %{_libexecdir}/geoclue-geonames
%attr(755,root,root) %{_libexecdir}/geoclue-gsmloc
%attr(755,root,root) %{_libexecdir}/geoclue-hostip
%attr(755,root,root) %{_libexecdir}/geoclue-localnet
%attr(755,root,root) %{_libexecdir}/geoclue-manual
%attr(755,root,root) %{_libexecdir}/geoclue-master
%attr(755,root,root) %{_libexecdir}/geoclue-nominatim
%attr(755,root,root) %{_libexecdir}/geoclue-plazes
%attr(755,root,root) %{_libexecdir}/geoclue-yahoo
%dir %{_datadir}/geoclue-providers
%{_datadir}/geoclue-providers/geoclue-example.provider
%{_datadir}/geoclue-providers/geoclue-geonames.provider
%{_datadir}/geoclue-providers/geoclue-gsmloc.provider
%{_datadir}/geoclue-providers/geoclue-hostip.provider
%{_datadir}/geoclue-providers/geoclue-localnet.provider
%{_datadir}/geoclue-providers/geoclue-manual.provider
%{_datadir}/geoclue-providers/geoclue-nominatim.provider
%{_datadir}/geoclue-providers/geoclue-plazes.provider
%{_datadir}/geoclue-providers/geoclue-yahoo.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Master.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Example.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Geonames.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gsmloc.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Hostip.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Localnet.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Manual.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Nominatim.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Plazes.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Yahoo.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgeoclue.so.?
%attr(755,root,root) %{_libdir}/libgeoclue.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeoclue.so
%{_includedir}/geoclue
%{_pkgconfigdir}/geoclue.pc

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/geoclue

%files provider-gypsy
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/geoclue-gypsy
%{_datadir}/geoclue-providers/geoclue-gypsy.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gypsy.service

%files provider-skyhook
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/geoclue-skyhook
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Skyhook.service
%{_datadir}/geoclue-providers/geoclue-skyhook.provider
%endif

