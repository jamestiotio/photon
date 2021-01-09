Summary:        DNS proxy with integrated DHCP server
Name:           dnsmasq
Version:        2.82
Release:        1%{?dist}
License:        GPLv2 or GPLv3
Group:          System Environment/Daemons
URL:            http://www.thekelleys.org.uk/dnsmasq/
Source:         %{name}-%{version}.tar.xz
%define sha1    dnsmasq=4eb84825d5a3b7e4d7de1fc58c56dd4eb8cace71
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       dnsmasq
Patch0:         0001-Fix-remote-buffer-overflow-CERT-VU-434904.patch
Patch1:         0002-Check-destination-of-DNS-UDP-query-replies.patch
Patch2:         0003-Use-SHA-256-to-provide-security-against-DNS-cache-po.patch
Patch3:         0004-Handle-multiple-identical-near-simultaneous-DNS-quer.patch
Patch4:         0005-Support-hash-function-from-nettle-only.patch
Patch5:         0006-Small-cleanups-in-frec_src-datastucture-handling.patch

%description
Dnsmasq a lightweight, caching DNS proxy with integrated DHCP server.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sharedstatedir}/dnsmasq
mkdir -p %{buildroot}%{_sysconfdir}/dnsmasq.d
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_bindir}
install src/dnsmasq %{buildroot}%{_sbindir}/dnsmasq
install dnsmasq.conf.example %{buildroot}%{_sysconfdir}/dnsmasq.conf
install dbus/dnsmasq.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
install -m 644 man/dnsmasq.8 %{buildroot}%{_mandir}/man8/
install -D trust-anchors.conf %{buildroot}%{_datadir}/%{name}/trust-anchors.conf

install -m 755 contrib/wrt/lease_update.sh %{buildroot}%{_sbindir}/lease_update.sh

mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >> %{buildroot}/usr/lib/systemd/system/dnsmasq.service
[Unit]
Description=A lightweight, caching DNS proxy
After=network.target

[Service]
ExecStart=/usr/sbin/dnsmasq -k
Restart=always

[Install]
WantedBy=multi-user.target
EOF

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/systemd/*
%exclude %{_libdir}/debug
%{_sbindir}/*
%{_mandir}/*
%{_sysconfdir}/dnsmasq.d
%config(noreplace) %{_sysconfdir}/dnsmasq.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dnsmasq.conf
%dir %{_sharedstatedir}
%config  /usr/share/dnsmasq/trust-anchors.conf

%changelog
*   Sat Jan 09 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.82-1
-   Fix CVE-2020-25681,CVE-2020-25682,CVE-2020-25683,CVE-2020-25684
-   CVE-2020-25685,CVE-2020-25686,CVE-2020-25687
*   Tue Jan 14 2020 Ashwin H <ashwinh@vmware.com> 2.79-1
-   Fix CVE-2019-14834 and update to 2.79
*   Fri Aug 31 2018 Dweep Advani <dadvani@vmware.com> 2.76-6
-   Preserve configuration files during package upgrade
*   Tue Feb 13 2018 Xiaolin Li <xiaolinl@vmware.com> 2.76-5
-   Fix CVE-2017-15107
*   Mon Nov 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-4
-   Always restart dnsmasq service on exit
*   Wed Oct 11 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-3
-   Fix CVE-2017-13704
*   Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> 2.76-2
-   Fix CVE-2017-14491..CVE-2017-14496
*   Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.76-1
-   Upgrade to 2.76 to address CVE-2015-8899
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.75-2
-   GA - Bump release of all rpms
*   Mon Apr 18 2016 Xiaolin Li <xiaolinl@vmware.com> 2.75-1
-   Initial version
