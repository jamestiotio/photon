Summary:         Math libraries
Name:            gmp
Version:         6.1.2
Release:         1%{?dist}
License:         LGPLv3+
URL:             http://www.gnu.org/software/gmp
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon
Source0:         http://ftp.gnu.org/gnu/gmp/%{name}-%{version}.tar.xz
%define sha1 gmp=9dc6981197a7d92f339192eea974f5eca48fcffe

%description
The GMP package contains math libraries. These have useful functions
for arbitrary precision arithmetic.

%package    devel
Summary:    Header and development files for gmp
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%setup -q

%build

%ifarch x86_64
# Do not detect host's CPU. Generate generic library (-mtune=k8)
cp -v configfsf.guess config.guess
cp -v configfsf.sub config.sub
%endif

%configure \
    --disable-silent-rules \
    --disable-static \
    --disable-assembly
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{isa_abi_headache,configuration} doc/*.html %{buildroot}%{_defaultdocdir}/%{name}-%{version}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libgmp.so.*

%files devel
%{_includedir}/gmp.h
%{_libdir}/libgmp.so
%{_docdir}/%{name}-%{version}/tasks.html
%{_docdir}/%{name}-%{version}/projects.html
%{_docdir}/%{name}-%{version}/configuration
%{_docdir}/%{name}-%{version}/isa_abi_headache

%changelog
*   Mon Sep 28 2020 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-1
-   Upgrade version to 6.1.2 as a part of gnutls-3.6.15 upgrade
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.0a-3
-	GA - Bump release of all rpms
*   Thu Apr 14 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 6.0.0a-2
-   Disable assembly and use generic C code
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 6.0.0a-1
-   Updated to version 6.0.0
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.1.3-1
-   Initial build. First version
