Name: libpcap
Epoch: 14
Version: 1.0.0
Release: 6.20091201git117cb5%{?dist}
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD with advertising
URL: http://www.tcpdump.org
BuildRequires: glibc-kernheaders >= 2.2.0 bison flex bluez-libs-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Source: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
# git snapshot from git://bpf.tcpdump.org/libpcap
Source: libpcap-1.0.0-20091201git117cb5.tar.bz2
Patch1: libpcap-man.patch
Patch2: libpcap-multilib.patch
Patch3: libpcap-s390.patch
Patch4: libpcap-0.8.3-ppp.patch

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package devel
Summary: Libraries and header files for the libpcap library
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other 
resources needed for developing libpcap applications.
 
%prep
%setup -q -n libpcap
echo '1.0.0' > VERSION

%patch1 -p1 -b .man 
%patch2 -p1 -b .multilib
%patch3 -p1 -b .s390
%patch4 -p0 -b .ppp

#sparc needs -fPIC 
%ifarch %{sparc}
sed -i -e 's|-fpic|-fPIC|g' configure
%endif

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing $(getconf LFS_CFLAGS)"
%configure --enable-ipv6 --enable-bluetooth
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/libpcap.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc LICENSE README CHANGES CREDITS doc/pcap.txt
%{_libdir}/libpcap.so.*
%{_mandir}/man7/pcap*.7*

%files devel
%defattr(-,root,root)
%{_bindir}/pcap-config
%{_includedir}/pcap*.h
%{_includedir}/pcap
%{_libdir}/libpcap.so
%{_mandir}/man1/pcap-config.1*
%{_mandir}/man3/pcap*.3*
%{_mandir}/man5/pcap*.5*

%changelog
* Fri Jun 18 2010 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-6.20091201git117cb5
- compile with -fno-strict-aliasing (#605080)

* Wed Dec 16 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-5.20091201git117cb5
- update to snapshot 20091201git117cb5

* Sat Oct 17 2009 Dennis Gilmore <dennis@ausil.us> 14:1.0.0-4.20090922gite154e2
- use -fPIC on sparc arches

* Wed Sep 23 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-3.20090922gite154e2
- update to snapshot 20090922gite154e2
- drop old soname

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:1.0.0-2.20090716git6de2de
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Miroslav Lichvar <mlichvar@redhat.com> 14:1.0.0-1.20090716git6de2de
- update to 1.0.0, git snapshot 20090716git6de2de

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14:0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 27 2008 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-3
- use CFLAGS when linking (#445682)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 14:0.9.8-2
- Autorebuild for GCC 4.3

* Wed Oct 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.8-1
- update to 0.9.8

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-3
- update license tag

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 14:0.9.7-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.7-1
- update to 0.9.7

* Tue Jun 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.6-1
- update to 0.9.6

* Tue Nov 28 2006 Miroslav Lichvar <mlichvar@redhat.com> 14:0.9.5-1
- split from tcpdump package (#193657)
- update to 0.9.5
- don't package static library
- maintain soname
