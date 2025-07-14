# TODO
# - ui subpackage?
# - subpackage for python?
# - add -avoid-version libtool to avoid versioned libraries in %{_libdir}/ethos/plugin-loaders
#
# Conditional build
%bcond_without	apidocs # disable gtk-doc

%define     packname ethos
Summary:	Reusable plugin framework for glib and gtk+
Name:		libethos
Version:	0.2.2
Release:	3
License:	LGPL v2.1
Group:		Libraries
Source0:	http://ftp.dronelabs.com/sources/%{packname}/0.2/%{packname}-%{version}.tar.gz
# Source0-md5:	36cf1ef444a224556bba4d441c400300
URL:		http://git.dronelabs.com/ethos/about/
Patch0:		%{name}-pyc.patch
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	gjs-devel
BuildRequires:	glibc-misc
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala
Requires:	python-pygtk-gtk
Requires:	vala
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
%setup -q -n %{packname}-%{version}
%patch -P0 -p0

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
	INSTALL="install -p" \
	HTML_DIR=%{_gtkdocdir}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%py_postclean

rm -f $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/ethos/plugin-loaders/*.la

# TODO use -avoid-version in libtool instead
rm -f $RPM_BUILD_ROOT%{_libdir}/ethos/plugin-loaders/*.so.0
for a in $RPM_BUILD_ROOT%{_libdir}/ethos/plugin-loaders/lib*.so.*.*.*; do
	l=${a%.0.0.0}
	mv $a $l
done

%find_lang %{packname}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{packname}.lang
%defattr(644,root,root,755)
%doc COPYING AUTHORS README NEWS
%attr(755,root,root) %{_libdir}/libethos-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libethos-1.0.so.0
%attr(755,root,root) %{_libdir}/libethos-ui-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libethos-ui-1.0.so.0

%dir %{_libdir}/ethos
%dir %{_libdir}/ethos/plugin-loaders
%attr(755,root,root) %{_libdir}/ethos/plugin-loaders/libcloader.so
%attr(755,root,root) %{_libdir}/ethos/plugin-loaders/libjsloader.so
%attr(755,root,root) %{_libdir}/ethos/plugin-loaders/libpythonloader.so

%dir %{_datadir}/ethos
%dir %{_datadir}/ethos/icons
%{_datadir}/ethos/icons/*.png

%{_libdir}/girepository-1.0/Ethos-1.0.typelib

%{_datadir}/vala/vapi/ethos-1.0.vapi
%{_datadir}/vala/vapi/ethos-ui-1.0.vapi

%{_datadir}/pygtk/2.0/defs/ethos.defs
%{_datadir}/pygtk/2.0/defs/ethosui.defs

%attr(755,root,root) %{py_sitedir}/gtk-2.0/_ethos.so
%attr(755,root,root) %{py_sitedir}/gtk-2.0/_ethosui.so
%dir %{py_sitedir}/gtk-2.0/ethos
%{py_sitedir}/gtk-2.0/ethos/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/ethos-1.0
%{_pkgconfigdir}/ethos-1.0.pc
%{_pkgconfigdir}/ethos-ui-1.0.pc
%{_libdir}/libethos-1.0.so
%{_libdir}/libethos-ui-1.0.so
%{_libdir}/libethos-1.0.la
%{_libdir}/libethos-ui-1.0.la
%{_datadir}/gir-1.0/Ethos-1.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{packname}
%endif
