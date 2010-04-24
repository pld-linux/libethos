#
# Conditional build
%bcond_without	apidocs #disable gtk-doc
#
%define     _packname ethos
Summary:	Reusable plugin framework for glib and gtk+
Name:		libethos
Version:	0.2.2
Release:	3
License:	LGPL v2.1
Group:		Libraries
Source0:	http://ftp.dronelabs.com/sources/%{_packname}/0.2/%{_packname}-%{version}.tar.gz
# Source0-md5:	36cf1ef444a224556bba4d441c400300
URL:		http://git.dronelabs.com/ethos/about/
Patch0:		%{name}-pyc.patch
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gjs-devel
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ethos is a plugin framework that is written in C using the GLib and
GObject libraries. The goal is to have a single framework for
applications that lower the barrier to entry for extensions. To enable
as many communities as possible, various language bindings are
provided to allow extensions in the language of choice.

Ethos includes a GUI library as well named libethos-ui. This library
provides a gtk+ widget for managing plugins within your application.
Typically, you can simply add this to a "Plugins" tab in your
applications preferences dialog.

%package devel
Summary:	Header files for libethos library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gobject-introspection-devel
Requires:	pkgconfig

%description devel
Header files for libethos library.

%package apidocs
Summary:	Ethos library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Ethos.
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Ethos library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Ethos.

%prep
%setup -q -n %{_packname}-%{version}
%patch0 -p0

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-introspection \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%find_lang %{_packname}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f %{_packname}.lang
%defattr(644,root,root,755)
%doc COPYING AUTHORS README NEWS
%attr(755,root,root) %{_libdir}/libethos*.so.*
%dir %{_libdir}/ethos
%dir %{_libdir}/ethos/plugin-loaders
%attr(755,root,root) %{_libdir}/ethos/plugin-loaders/lib*.so.*
%{_libdir}/girepository-1.0/Ethos-1.0.typelib
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/pygtk/2.0/defs/ethos*
%{py_sitedir}/gtk-2.0/ethos
%{py_sitedir}/gtk-2.0/_ethos*
%dir %{_datadir}/ethos/
%dir %{_datadir}/ethos/icons/
%{_datadir}/ethos/icons/*.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/ethos-1.0
%{_libdir}/ethos/plugin-loaders/lib*.so
%{_libdir}/ethos/plugin-loaders/lib*.la
%{_pkgconfigdir}/ethos*1.0.pc
%{_libdir}/*.so
%{_libdir}/*.la
%{_datadir}/gir-1.0/Ethos-1.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{_packname}
%endif
