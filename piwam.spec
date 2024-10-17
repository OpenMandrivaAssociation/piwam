%define       name    piwam
%define       version 1.1.2
%define       release %mkrel 1

Summary:      Piwam Is A Wonderful Association Manager
Name:         %{name}
Version:      %{version}
Release:      %{release}
Source0:      %{name}-%{version}-xmas.tar.gz
License:      AGPLv3
Group:        Monitoring
Url:          https://code.google.com/p/piwam/
BuildRoot:    %{_tmppath}/%{name}-buildroot
BuildRequires: apache-base
Requires:     php >= 4.1
Requires:     apache-base
Requires:     apache-mod_php
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:    noarch

%description
Association Manager, written in PHP with Symfony framework. 
But it has been developped for French  associations only, 
which respect specific French laws. That is why this project 
space will be only in French

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%attr(-,apache,apache) %_datadir/%name
%config(noreplace) %_sysconfdir/httpd/conf/webapps.d/%{name}.conf

#--------------------------------------------------------------------


%prep
%setup -q -n %{name}-%{version}-xmas

%install
rm -rf $RPM_BUILD_ROOT

%__mkdir -p %buildroot%_datadir
(
cd %buildroot%_datadir
tar xzf %{SOURCE0}
mv -fv %{name}-%{version}-xmas %{name}/
cd %{name}/
chmod 777 -R cache
chmod 777 -R log
chmod 777 -R config/databases.yml 
chmod 777 -R web/uploads/*
)


mkdir -p %buildroot%_sysconfdir/httpd/conf/webapps.d
cat > %buildroot%_sysconfdir/httpd/conf/webapps.d/%{name}.conf <<EOF
# %{name} configuration
Alias /%name %_datadir/%name
<Directory %_datadir/%name>
    Order allow,deny
    Allow from all
</Directory>

EOF

%clean
rm -rf $RPM_BUILD_ROOT


