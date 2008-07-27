Summary:	PHP-based, extensible, customizable, semantic website revision system
Summary(pl.UTF-8):	Oparty na PHP, rozszerzalny, konfigurowalny, semantyczny system kontroli rewizji
Name:		sovix
Version:	0.0.1.5
Release:	0.1
License:	AGPL v3+
Group:		Applications/WWW
Source0:	http://ftp.gnu.org/gnu/sovix/%{name}-%{version}.tar.gz
# Source0-md5:	3fa4b29de3ab2290e8a4a2115b88288b
Patch0:		%{name}-config.patch
URL:		http://www.sovix.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Sovix is the PHP-based, extensible, customizable, semantic website
revision system.

Some of the features of GNU Sovix include:

 - Mechanisms to receive the software code over network protected by
   the GNU Affero General Public License.
 - Semantically valid HTML and XHTML markup.
 - Agnostic RDBMS support for PostgreSQL and MySQL via Sovix web
   template engine.
 - Cross platform/web server/browser compatible.
 - Online documentation available direct from Sovix, including a
   tutorial for new users.

%description -l pl.UTF-8
Sovix to oparty na PHP, rozszerzalny, konfigurowalny, semantyczny
system kontroli rewizji.

Niektóre z cech GNU Sovix:

 - mechanizmy do pobierania kodu ,
 - składnia zgodnia z HTML i XHTML,
 - wsparcie baz danych takich jak PostgreSQL czy MySQL za pomocą
   systemu szablonów Sovix,
 - kompatybilny z różnymi platformami / serwerami http /
   przeglądarkami,
 - dostępna dokumentacja online wraz z przewodnikiem dla nowych
   użytkowników.

%prep
%setup -q
%patch0 -p0

# fix path
for i in $(find . -name "*.php" -o -name "*.inc");
do
	#perl -pli -e "s|=\\\$\_SERVER\\['DOCUMENT_ROOT'\\].\"/sovix|=\"%{_appdir}|" $i
	perl -pli -e "s|=\\\$\_SERVER\\['DOCUMENT_ROOT'\\].\"/sovix|=\"%{_appdir}|" $i
	perl -pli -e "s|\\\$\_SERVER\\['DOCUMENT_ROOT'\\]|'%{_datadir}'|" $i
done

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a *.php *.inc $RPM_BUILD_ROOT%{_appdir}
cp -a copy dev dotsovix etc include Sandbox src Templates websrc $RPM_BUILD_ROOT%{_appdir}

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
