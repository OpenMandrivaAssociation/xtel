%define name	xtel
%define version	3.3.0
%define release	%mkrel 9

Summary: Emulateur Minitel
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pficheux.free.fr/xtel/download/xtel-%{version}.tar.bz2
Source1: %{name}-fr-doc.tar.bz2
# FHS compliant XTEL
Patch0: xtel-mdk.patch
Patch1: xtel-3.3.0-debian_symlink_security.patch
Patch2: xtel-3.3.0-debian_a2ps.patch
Patch3: xtel-3.3.0-debian_motif.patch
License: GPLv2+
Group: Networking/Other
Buildrequires: XFree86-devel 
Buildrequires: jpeg-devel
Buildrequires: gccmakedep
BuildRequires: imake
BuildRequires: lesstif-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://pficheux.free.fr/xtel/
Requires: xinetd

%description
Ce programme émule un Minitel dans un environnement UNIX/X11. Il utilise
une architecture client/serveur (xtel/xteld). Le démon 'xteld' se charge de
gérer les connexions Télétel (par modem) demandées par les clients via
TCP/IP. Xtel émule le Minitel 1B, 2 et TVR. Xteld permet également d'utiliser
HyperTerminal Private Edition (3.0 ou 4.0) comme client Minitel Windows95/NT.

%prep
%setup -q -a1
%patch0 -p1 -b .fhs
%patch1 -p1 -b .symlink
%patch2 -p1 -b .a2ps
%patch3 -p1 -b .motif
%build
perl -pi -e 's|(#define.*DEBUG_XTELD.*)|/* $1 */|' Config.tmpl
# do not leak information in the config file
imake -DREDHAT  -DUseInstalled -I/usr/share/X11/config

make Xtel

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
make install.man DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_bindir}/mdmdetect
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
    server              = %{_bindir}/xteld
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
    server              = %{_bindir}/xteld
}

EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Xtel
Comment=Minitel emulation
Exec=%{_bindir}/%{name} 
Icon=terminals_section.png
Terminal=false
Type=Application
StartupNotify=true
MimeType=foo/bar;foo2/bar2;
Categories=Motif;System;TerminalEmulator;
EOF

# fix symlinks
mv $RPM_BUILD_ROOT/usr/lib/X11/app-defaults $RPM_BUILD_ROOT/usr/lib/X11/app-defaults.bak
mkdir -p $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
cp -Rf $RPM_BUILD_ROOT/usr/lib/X11/app-defaults.bak/* $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
rm -f $RPM_BUILD_ROOT/usr/lib/X11/app-defaults.bak

mkdir -p %{buildroot}%_sysconfdir/X11/fontpath.d/
ln -s ../../../usr/lib/X11/fonts/xtel \
    %{buildroot}%_sysconfdir/X11/fontpath.d/xtel:pri=50

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
%{update_menus}
 
%postun
service xinetd restart
%{clean_menus}  

%files
%defattr(-,root,root)
%doc LISEZMOI.txt FAQ.txt HISTOIRE.txt
%doc xtel-fr-doc/*
%{_bindir}*
%{_libdir}/X11/app-defaults/XTelm
%{_libdir}/X11/app-defaults/XTelm-msg
%{_libdir}/X11/fonts/%{name}
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/X11/fontpath.d/xtel:pri=50
%{_libdir}/X11/%{name}
%{_mandir}/man1/*

%config(noreplace) %{_sysconfdir}/%{name}/xtel.services
%config(noreplace) %{_sysconfdir}/%{name}/xtel.lignes
%config(noreplace) %{_sysconfdir}/ppp/*iminitel
%config(noreplace) %{_sysconfdir}/ppp/peers/iminitel
%config(noreplace) %{_sysconfdir}/xinetd.d/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*

%{_datadir}/applications/mandriva-%{name}.desktop

