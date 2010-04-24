%define     _packname ethos
Summary:	Reusable plugin framework for glib and gtk+
Name:		libethos
Version:	0.2.2
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://ftp.dronelabs.com/sources/%{_packname}/0.2/%{_packname}-%{version}.tar.gz
# Source0-md5:	36cf1ef444a224556bba4d441c400300
URL:		http://git.dronelabs.com/ethos/about/
Patch0:		%{name}-pyc.patch
BuildRequires:	gjs-devel
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
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

%prep
%setup -q -n %{_packname}-%{version}
%patch0 -p0

%build
./autogen.sh \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--disable-static \
	--enable-introspection \
	--enable-python \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

make

%install
rm -rf $RPM_BUILD_ROOT
install -p -d $RPM_BUILD_ROOT/%{name}-%{version}
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS README NEWS
%doc %{_datadir}/doc/gtk-doc/html/ethos/*
%attr(755,root,root) %{_libdir}/libethos*.so.*
%dir %{_libdir}/ethos
%dir %{_libdir}/ethos/plugin-loaders
%attr(755,root,root) %{_libdir}/ethos/plugin-loaders/lib*.so.*
%{_libdir}/girepository-1.0/Ethos-1.0.typelib
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/pygtk/2.0/defs/ethos*
%{py_sitedir}/gtk-2.0/ethos
%{py_sitedir}/gtk-2.0/_ethos*
%{_datadir}/ethos/icons/*png
%{_localedir}/*/LC_MESSAGES/ethos*

%files devel
%defattr(644,root,root,755)
%{_includedir}/ethos-1.0
%{_libdir}/ethos/plugin-loaders/lib*.so
%{_pkgconfigdir}/ethos*1.0.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/Ethos-1.0.gir
