Summary: Emulateur Minitel X11
Name: xtel
Version: 3.3.0
Release: 8mdk
Source0: http://pficheux.free.fr/xtel/download/xtel-%{version}.tar.bz2
Source1: %{name}-fr-doc.tar.bz2
# FHS compliant XTEL
Patch0: xtel-mdk.patch.bz2
License: GPL
Group: Networking/Other
Buildrequires: XFree86-devel jpeg-devel XFree86
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
PreReq: chkfontpath
URL: http://pficheux.free.fr/xtel/
Requires: xinetd

%description
Ce programme émule un Minitel dans un environnement UNIX/X11. Il utilise
une architecture client/serveur (xtel/xteld). Le démon 'xteld' se charge de
gérer les connexions Télétel (par modem) demandées par les clients via
TCP/IP. Xtel émule le Minitel 1B, 2 et TVR. Xteld permet également d'utiliser
HyperTerminal Private Edition (3.0 ou 4.0) comme client Minitel Windows95/NT.


%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -a1
%patch0 -p1 -z .fhs
%build
perl -pi -e 's|(#define.*DEBUG_XTELD.*)|/* $1 */|' Config.tmpl
# do not leak information in the config file
imake -DREDHAT  -DUseInstalled -I/usr/X11R6/lib/X11/config

make Xtel

%install
rm -rf  $RPM_BUILD_ROOT


%makeinstall_std
make install.man DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT/usr/X11R6/bin/mdmdetect
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/xtel
# default: on
# description: xteld provide services for MINITEL.

service xtel
{
    disable             = no
    socket_type         = stream
    protocol            = tcp
    wait                = no
    user                = root
	group				= nogroup
    server              = /usr/X11R6/bin/xteld
}

EOF
cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/xtelw
# default: on
# description: xteld provide services for MINITEL.

service xtelw
{
    disable             = no
    socket_type         = stream
    protocol            = tcp
    wait                = no
    user                = root
	group				= nogroup
    server              = /usr/X11R6/bin/xteld
}

EOF

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="/usr/X11R6/bin/xtel"\
title="Xtel"\
longtitle="Minitel emulation"\
needs="x11"\
section="Networking/Other"
EOF

# fix symlinks
mv $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults.bak
mkdir -p $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults
cp -Rf $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults.bak/* $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults
rm -f $RPM_BUILD_ROOT/usr/X11R6/lib/X11/app-defaults.bak

%clean
rm -fr $RPM_BUILD_ROOT


%post
if [ "`grep xtel /etc/services`" = "" ]; then
	echo -n "Mise à jour de /etc/services..."
	echo -e "xtel\t\t1313/tcp\t\t\t# Xtel" >> /etc/services
	echo -e "xtelw\t\t1314/tcp\t\t\t# Xtel HyperTerminal" >> /etc/services
	echo "OK"
fi

service xinetd restart

chkfontpath --list | grep /usr/X11R6/lib/X11/fonts/xtel > /dev/null 2>&1

if [ $? != 0 ]; then
   chkfontpath --add /usr/X11R6/lib/X11/fonts/xtel
fi

%{update_menus}
 
%postun
service xinetd restart

if [ "$1" = "0" ]; then 
  chkfontpath --remove /usr/X11R6/lib/X11/fonts/xtel
fi
%{clean_menus}  


%files
%defattr(-,root,root)
%doc COPYING LISEZMOI.txt FAQ.txt HISTOIRE.txt
%doc xtel-fr-doc/*
/usr/X11R6/bin/*
/usr/X11R6/lib/X11/app-defaults/XTel
/usr/X11R6/lib/X11/app-defaults/XTel-msg
/usr/X11R6/lib/X11/fonts/xtel/fonts.alias
/usr/X11R6/lib/X11/fonts/xtel/g08x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g08x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g016x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g016x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g032x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g016x40.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g032x40.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g18x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g116x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g1s8x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g1s16x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s8x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s8x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s16x10.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s16x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s32x20.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s16x40.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/g0s32x40.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/xteldigit.pcf.gz
/usr/X11R6/lib/X11/fonts/xtel/fonts.dir
/usr/X11R6/lib/X11/fonts/xtel/fonts.scale

%dir /usr/X11R6/lib/X11/fonts/xtel

/usr/X11R6/lib/X11/xtel/modem.list
/usr/X11R6/lib/X11/xtel/connect_iminitel

%dir /usr/X11R6/lib/X11/xtel/

%doc /usr/X11R6/man/man1/*
%doc /usr/X11R6/lib/X11/doc/html/*

%dir %{_sysconfdir}/xtel/
%config(noreplace) %{_sysconfdir}/xtel/xtel.services
%config(noreplace) %{_sysconfdir}/xtel/xtel.lignes
%config(noreplace) %{_sysconfdir}/ppp/*iminitel
%config(noreplace) %{_sysconfdir}/ppp/peers/iminitel
%config(noreplace) %{_sysconfdir}/xinetd.d/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*

%{_menudir}/*
