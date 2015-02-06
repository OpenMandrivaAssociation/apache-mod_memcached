#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_memcached
%define mod_conf B30_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.3
Release:	11
Group:		System/Servers
License:	Apache License
URL:		http://tangent.org/
Source0:	http://download.tangent.org/mod_memcached-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRequires:  libmemcached-devel

%description
This is an Apache module that provides GET, PUT, and DELETE services to
Memcached clusters. Using this you can serve content directly from memcached
through Apache to clients.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build
echo "#define VERSION \"%{version}\"" > version.h

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc ChangeLog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.3-10mdv2012.0
+ Revision: 772687
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3-9
+ Revision: 678346
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-8mdv2011.0
+ Revision: 588031
- rebuild

* Thu Mar 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3-7mdv2010.1
+ Revision: 518183
- bump release
- fix deps
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3-5mdv2010.0
+ Revision: 406618
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3-4mdv2009.1
+ Revision: 326120
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-3mdv2009.0
+ Revision: 235055
- rebuild

* Sat Jun 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-2mdv2009.0
+ Revision: 216711
- rebuild

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdv2009.0
+ Revision: 205390
- 0.3

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2008.1
+ Revision: 182975
- import apache-mod_memcached


* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdv2008.1
- initial Mandriva package
