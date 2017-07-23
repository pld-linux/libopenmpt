#
# Conditional build:
%bcond_without	openmpt123	# openmpt123 CLI player
%bcond_with	sdl		# SDL2 output in openmpt123
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# unit tests
#
Summary:	Tracker module player based on OpenMPT
Summary(pl.UTF-8):	Odtwarzacz modułów ścieżkowych oparty na OpenMPT
Name:		libopenmpt
Version:	0.2.8461
Release:	1
License:	BSD
Group:		Libraries
# "betaNN" is only information, not element of version number
Source0:	https://lib.openmpt.org/files/libopenmpt/src/%{name}-%{version}-beta26-autotools.tar.gz
# Source0-md5:	29ac490b6444be3f123d95650811b17d
URL:		https://lib.openmpt.org/
BuildRequires:	doxygen
BuildRequires:	libmpg123-devel
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig >= 1:0.24
BuildRequires:	zlib-devel
%if %{with openmpt123}
%{?with_sdl:BuildRequires:	SDL2-devel >= 2}
BuildRequires:	flac-devel >= 1.3.0
BuildRequires:	libsndfile-devel
BuildRequires:	portaudio-devel >= 19
BuildRequires:	portaudio-c++-devel >= 19
BuildRequires:	pulseaudio-devel
%endif
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation and examples for OpenMPT library.

%description apidocs -l pl.UTF-8
Dokumentacja API i przykłady do biblioteki OpenMPT.

%package -n openmpt123
Summary:	Command line module music player based on libopenmpt
Summary(pl.UTF-8):	Działający z linii poleceń odtwarzacz modułów muzycznych oparty na libopenmpt
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description -n openmpt123
Command line module music player based on libopenmpt.

%description -n openmpt123 -l pl.UTF-8
Działający z linii poleceń odtwarzacz modułów muzycznych oparty na
libopenmpt.

%prep
%setup -q -n %{name}-%{version}-autotools

%build
%configure \
	%{!?with_openmpt123:--disable-openmpt123} \
	%{!?with_static_libs:--disable-static} \
	%{?with_sdl:--with-sdl2}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
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
%doc LICENSE TODO
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

%files apidocs
%defattr(644,root,root,755)
%doc doxygen-doc/html/*
%{_examplesdir}/%{name}-%{version}

%if %{with openmpt123}
%files -n openmpt123
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/openmpt123
%{_mandir}/man1/openmpt123.1*
%endif
