#
# Conditional build:
%bcond_without	apidocs		# API documentation (doxygen based)
%bcond_without	openmpt123	# openmpt123 CLI player
%bcond_without	portaudio	# PortAudio support
%bcond_with	sdl		# SDL2 output in openmpt123
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# unit tests
#
Summary:	Tracker module player based on OpenMPT
Summary(pl.UTF-8):	Odtwarzacz modułów ścieżkowych oparty na OpenMPT
Name:		libopenmpt
Version:	0.6.2
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://lib.openmpt.org/files/libopenmpt/src/%{name}-%{version}+release.autotools.tar.gz
# Source0-md5:	d21fb799695cbe10a1e9aeaea23ed708
URL:		https://lib.openmpt.org/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libmpg123-devel >= 1.14.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig >= 1:0.24
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	zlib-devel
%if %{with openmpt123}
%{?with_sdl:BuildRequires:	SDL2-devel >= 2.0.4}
BuildRequires:	flac-devel >= 1.3.0
BuildRequires:	libsndfile-devel
%if %{with portaudio}
BuildRequires:	portaudio-devel >= 19
BuildRequires:	portaudio-c++-devel >= 19
%endif
BuildRequires:	pulseaudio-devel
%endif
Requires:	libmpg123 >= 1.14.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tracker module player based on OpenMPT.

%description -l pl.UTF-8
Odtwarzacz modułów ścieżkowych oparty na OpenMPT.

%package devel
Summary:	Header files for OpenMPT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenMPT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libmpg123-devel
Requires:	libogg-devel
Requires:	libvorbis-devel
Requires:	zlib-devel

%description devel
Header files for OpenMPT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenMPT.

%package static
Summary:	Static OpenMPT library
Summary(pl.UTF-8):	Statyczna biblioteka OpenMPT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenMPT library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenMPT.

%package apidocs
Summary:	API documentation for OpenMPT library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenMPT
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation and examples for OpenMPT library.

%description apidocs -l pl.UTF-8
Dokumentacja API i przykłady do biblioteki OpenMPT.

%package -n openmpt123
Summary:	Command line module music player based on libopenmpt
Summary(pl.UTF-8):	Działający z linii poleceń odtwarzacz modułów muzycznych oparty na libopenmpt
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}
Requires:	flac >= 1.3.0

%description -n openmpt123
Command line module music player based on libopenmpt.

%description -n openmpt123 -l pl.UTF-8
Działający z linii poleceń odtwarzacz modułów muzycznych oparty na
libopenmpt.

%prep
%setup -q -n %{name}-%{version}+release.autotools

%build
%configure \
	--disable-examples \
	%{!?with_openmpt123:--disable-openmpt123} \
	%{!?with_static_libs:--disable-static} \
	%{!?with_portaudio:--without-portaudio} \
	%{!?with_portaudio:--without-portaudiocpp} \
	%{?with_sdl:--with-sdl2}
%{__make}

%if %{with tests}
%{__make} check
%endif

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
# packaged as %doc / examples
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopenmpt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# don't package README.md here, it contains only packager and libopenmpt developer information
%doc LICENSE
%attr(755,root,root) %{_libdir}/libopenmpt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenmpt.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenmpt.so
%{_includedir}/libopenmpt
%{_pkgconfigdir}/libopenmpt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopenmpt.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen-doc/html/*
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with openmpt123}
%files -n openmpt123
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/openmpt123
%{_mandir}/man1/openmpt123.1*
%endif
