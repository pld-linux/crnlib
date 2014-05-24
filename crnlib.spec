# NOTE: we use "crnlib" because plain "crunch" or "libcrunch" isn't unique project name
Summary:	crunch/crnlib - advanced DXTn texture compression library
Summary(pl.UTF-8):	crunch/crnlib - zaawansowana biblioteka do kompresji tekstur DXTn
Name:		crnlib
Version:	1.04
Release:	1
License:	ZLib
Group:		Libraries
#Source0Download: http://code.google.com/p/crunch/downloads/list
# but no Linux-supporting releases there
# svn co http://crunch.googlecode.com/svn/tags/v104 crunch
# rm -rf crunch/bin*
# tar cJf crunch-104.tar.xz -x .svn crunch
Source0:	crunch-104.tar.xz
# Source0-md5:	f92837bba95abf27d6bd9ae0b2b04863
Patch0:		%{name}-c++.patch
Patch1:		%{name}-types.patch
URL:		http://code.google.com/p/crunch/
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
crnlib is a lossy texture compression library for developers that ship
content using the DXT1/5/N or 3DC compressed color/normal map/cubemap
mipmapped texture formats.

%description -l pl.UTF-8
crnlib to biblioteka stratnej kompresji dla programistów
dostarczających dane przy użyciu formatów tekstur (kolorów, map
normalnych i innych) z zastosowaną kompresją DXT1/5/N lub 3DC.

%package devel
Summary:	Header files for crnlib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki crnlib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for crnlib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki crnlib.

%package static
Summary:	Static crnlib library
Summary(pl.UTF-8):	Statyczna biblioteka crnlib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static crnlib library.

%description static -l pl.UTF-8
Statyczna biblioteka crnlib.

%prep
%setup -q -n crunch
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '/g++.*COMPILE_OPTIONS/s/g++/$(CXX)/' crnlib/Makefile
%{__sed} -i -e '/g++.*LINKER_OPTIONS/s/g++/$(CXXLINK)/' crnlib/Makefile

%build
%{__make} -C crnlib \
	CXX="libtool --mode=compile %{__cxx}" \
	CXXLINK="libtool --mode=link %{__cxx}" \
	COMPILE_OPTIONS="%{rpmcflags} -fomit-frame-pointer -ffast-math -fno-math-errno -fno-strict-aliasing -Wall -Wno-unused-value -Wno-unused" \
	LINKER_OPTIONS="%{rpmldflags} -lpthread"

libtool --mode=link %{__cxx} %{rpmldflags} -o crnlib/libcrunch.la crnlib/{crnlib,crn_*,lzma_*}.lo -rpath %{_libdir} -lpthread
# relink using shared library
libtool --mode=link %{__cxx} %{rpmldflags} -o crnlib/crunch crnlib/{crunch,corpus_gen,corpus_test}.o crnlib/libcrunch.la -lpthread

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir}}

libtool --mode=install install crnlib/libcrunch.la $RPM_BUILD_ROOT%{_libdir}
cp -p inc/*.h $RPM_BUILD_ROOT%{_includedir}
install crnlib/crunch $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc license.txt readme.txt
%attr(755,root,root) %{_bindir}/crunch
%attr(755,root,root) %{_libdir}/libcrunch.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrunch.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcrunch.so
%{_libdir}/libcrunch.la
%{_includedir}/crn_decomp.h
%{_includedir}/crnlib.h
%{_includedir}/dds_defs.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcrunch.a
