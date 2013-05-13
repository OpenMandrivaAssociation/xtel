%define name	xtel
%define version	3.3.0
%define release 	18

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
BuildRequires: pkgconfig(x11)
BuildRequires: lesstif-devel
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xmu)
BuildRequires: pkgconfig(xaw7)
BuildRequires: libxp-devel
Buildrequires: jpeg-devel
BuildRequires: x11-data-bitmaps
BuildRequires: imake
BuildRequires: gccmakedep
BuildRequires: mkfontdir
BuildRequires: bdftopcf
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
imake -DREDHAT  -DUseInstalled -I/usr/share/X11/config LIBDIR=%{_libdir}

make Xtel LIBDIR=%{_libdir} CXXOPTIONS="%optflags" EXTRA_LDOPTIONS="%ldflags"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std LIBDIR=%{_libdir}
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
Name=Xtel
Comment=Minitel emulation
Exec=%{_bindir}/%{name} 
Icon=terminals_section
Terminal=false
Type=Application
StartupNotify=true
MimeType=foo/bar;foo2/bar2;
Categories=Motif;System;TerminalEmulator;
EOF

# fix symlinks
rm -rf $RPM_BUILD_ROOT%{_libdir}/app-defaults
mkdir -p $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults
ln -s %{_sysconfdir}/X11/app-defaults/XTelm $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XTelm
ln -s %{_sysconfdir}/X11/app-defaults/XTelm-msg $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XTelm-msg

mkdir -p %{buildroot}%_sysconfdir/X11/fontpath.d/
ln -s ../../..%{_datadir}/fonts/xtel \
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
%if %mdkversion < 200900
%{update_menus}
%endif
 
%postun
service xinetd restart
%if %mdkversion < 200900
%{clean_menus}  
%endif

%files
%defattr(-,root,root)
%doc LISEZMOI.txt FAQ.txt HISTOIRE.txt
%doc xtel-fr-doc/*
%{_bindir}*
%{_libdir}/X11/app-defaults/XTelm
%{_libdir}/X11/app-defaults/XTelm-msg
%{_datadir}/fonts/*
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/X11/fontpath.d/xtel:pri=50
%{_libdir}/%{name}
%{_mandir}/man1/*

%config(noreplace) %{_sysconfdir}/%{name}/xtel.services
%config(noreplace) %{_sysconfdir}/%{name}/xtel.lignes
%config(noreplace) %{_sysconfdir}/ppp/*iminitel
%config(noreplace) %{_sysconfdir}/ppp/peers/iminitel
%config(noreplace) %{_sysconfdir}/xinetd.d/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*

%{_datadir}/applications/mandriva-%{name}.desktop



%changelog
* Fri Jan 28 2011 Funda Wang <fwang@mandriva.org> 3.3.0-17mdv2011.0
+ Revision: 633645
- simplify BR

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.0-16mdv2011.0
+ Revision: 615739
- the mass rebuild of 2010.1 packages

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 3.3.0-15mdv2010.0
+ Revision: 435376
- BuildRequires libxp-devel
- rebuild

* Mon Aug 04 2008 Thierry Vignaud <tv@mandriva.org> 3.3.0-14mdv2009.0
+ Revision: 262737
- rebuild

* Thu Jul 31 2008 Thierry Vignaud <tv@mandriva.org> 3.3.0-13mdv2009.0
+ Revision: 257818
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 3.3.0-11mdv2008.1
+ Revision: 140994
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Wed Aug 15 2007 Adam Williamson <awilliamson@mandriva.org> 3.3.0-11mdv2008.0
+ Revision: 63561
- okay, let's fix this up for x86-64 better, fix the symlinks better, and put the fonts in the right place
- bump for stupid bs bug
- oops, fix app-defaults stuff for x86-64
- buildrequires mkfontdir and bdftopcf
- buildrequires x11-data-bitmaps
- rebuild for 2008
- clean file list
- XDG menu
- use modern X layout (no more X11R6)
- new location for imake templates
- fix buildrequires
- patch3 (Debian): build against lesstif
- patch2 (Debian): correct calls to a2ps
- patch1 (Debian): fix symlink security issue
- use Fedora license policy (GPLv2+)
- spec clean

  + Ademar de Souza Reis Jr <ademar@mandriva.com.br>
    - fontpath.d conversion (#31756)
    - Import xtel



* Sat Mar 12 2005 Michael Scherer <misc@mandrake.org> 3.3.0-8mdk
- disable debug output in the log, thanks to Gerard Quequet

* Mon Feb 21 2005 Franck Villaume <fvill@freesurf.fr> 3.3.0-7mdk
- add missing files

* Wed Oct 20 2004 Michael Scherer <misc@mandrake.org> 3.3.0-6mdk
- Rebuild
- add missing file, to correct the size of the screen

* Tue Dec 30 2003 Michael Scherer <misc@mandrake.org> 3.3.0-5mdk 
- fix compilation
- remove some [DIRM]
- use service xinetd restart instead of sending SIGHUP

* Wed Jul 23 2003 Lenny Cartier <lenny@mandrakesoft.com> 3.3.0-4mdk
- buildrequires from Michael Scherer

* Tue May 06 2003 Lenny Cartier <lenny@mandrakesoft.com> 3.3.0-3mdk
- buildrequires

* Fri Jan 24 2003 Lenny Cartier <lenny@mandrakesoft.com> 3.3.0-2mdk
- rebuild

* Thu Jun 13 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 3.3.0-1mdk
- Release 3.3.0
- Regenerate patch0

* Sat Sep  1 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 3.2.1-7mdk
- Don't uninstall font when upgrading

* Thu Aug 23 2001 Etienne Faure <etienne@mandrakesoft.com> 3.2.1-6mdk
- rebuild

* Wed Feb 21 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.2.1-5mdk
- rebuild

* Tue Nov 07 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.2.1-4mdk
- added configuration examples and some documentation from 
  Pierre Jarillon <jarillon@atlantic-line.fr>

* Thu Sep 21 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.2.1-3mdk
- build release
- menu

* Thu May 04 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.2.1-2mdk
- fix group
- spechelper cleanups

* Fri Dec 31 1999 Frederic Lepied <flepied@mandrakesoft.com> 3.2.1-1mdk
- first mandrake release
