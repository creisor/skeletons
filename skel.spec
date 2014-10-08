# see: http://fedoraproject.org/wiki/How_to_create_an_RPM_package

Summary: <summary text> - packaged by 
Name: <software name - later used by %{name}>
Version: <software version>
Release: 1%{?dist}
License: BSD
Group: <run 'less /usr/share/doc/rpm-*/GROUPS' for a list>
Packager: Chris Reisor <username@exmaple.com>
Source: <tarball, preferably a url pointing to a tarball using %{name} and %{version}>
BuildArch: noarch
autoreq: false
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
#BuildRequires: comma,separated,list,of,packages
#BuildRequires: something >= 3.08
#Requires: comma,separated,list,of,packages

%description
<description text>

# Undefine these macros.  The libraries we are delivering were supplied by older
# OS's and we want to deliver them exactly as is, no further post-processing
# so this will short-circuit the strip functions.  You may see some errors on
# the build output lines where __strip is undefined, but that is OK.
# Un-comment the next two lines if you're delivering libraries
#%define __strip  %{nil}
#%define __objdump  %{nil}

# This prevents making debuginfo RPMs & running file checks (which often fail)
%global debug_package %{nil}
%undefine __check_files

%prep
# reads out of %_sourcedir, writes into %_builddir
%setup -c

%build
# reads out of %_builddir, writes into %_builddir
# usually a "./configure && make" type situation

#%check
# reads/writes in %_builddir
# usually "make test", if applicable

%install
# reads in %_builddir, writes to %_buildrootdir 
rm -rf %{buildroot}
# Define any directory where bits will go - one entry per unique path. Examples:
#install -d %{buildroot}/usr/lib64
#install -d %{buildroot}/etc/X11
# Might also be:
#  make install DESTDIR=$RPM_BUILD_ROOT

# One line for every file - see the commented lines below as examples
#install -v -p usr/lib64/libldap_r.so.2.0.130  %{buildroot}/usr/lib64/
#install -v -p etc/X11/xorg.conf  %{buildroot}/etc/X11

%files
%defattr(-,root,root,-)
# Fully pathed list of files.  See examples below:
#/usr/lib64/libldap.so.2.0.130
#/etc/X11/xorg.conf

%post
# If installing libraries, comment out the line above & uncomment the line below
#%post -p /sbin/ldconfig

%postun
# what to do when running 'rpm -e'
# If installing libraries, comment out the line above & uncomment the line below
#%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%changelog
* Fri Apr 29 2011 Chris Reisor <username@example.com>
- Initial revision
