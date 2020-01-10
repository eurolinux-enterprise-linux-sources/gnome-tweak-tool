%global major_version %%(cut -d "." -f 1-2 <<<%{version})

Name:           gnome-tweak-tool
Version:        3.14.3
Release:        2%{?dist}
Summary:        A tool to customize advanced GNOME 3 options

License:        GPLv3
URL:            http://live.gnome.org/GnomeTweakTool
Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/%{major_version}/gnome-tweak-tool-%{version}.tar.xz

Patch1:   0001-xkb-Blacklist-grp-and-grp_led-XKB-options.patch
Patch2:   0002-xkb-Switch-to-expanders-and-radio-buttons-instead-of.patch
Patch3:   0003-AutostartFile-add-support-to-create-a-user-autostart.patch
Patch4:   0004-Add-a-way-to-inhibit-systemd-s-default-behavior-on-l.patch
Patch5:   0005-gshellwrapper-Add-missing-extension-state-and-type.patch
Patch6:   0006-gshellwrapper-Proxy-the-extension-status-changed-sig.patch
Patch7:   0007-shell_extensions-Add-remove-tweaks-as-extensions-are.patch
Patch8:   0008-shell_extensions-Add-a-sort-func-to-keep-the-list-or.patch
Patch9:   0009-ExtensionInstaller-load-extension-after-installing-i.patch
Patch10:   0010-shell_extensions-SESSION_MODE-extensions-can-t-be-en.patch
Patch11:   0011-GSettingsFontButtonTweak-filter-out-fonts-that-gtk-3.patch
Patch12:   0012-font-Remove-document-font-tweak-since-nothing-honors.patch
Patch13:   0001-Avoid-GSettings-aborting-when-missing-classic-overri.patch

BuildArch:      noarch
BuildRequires:  intltool
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  desktop-file-utils
Requires:       gnome-shell
Requires:       pygobject3

%description
GNOME Tweak Tool is an application for changing the advanced settings
of GNOME 3.

Features:
* Install and switch gnome-shell themes
* Switch gtk/icon/cursor themes
* Switch window manager themes
* Change:
        * The user-interface and titlebar fonts
        * Icons in menus and buttons
        * Behavior on laptop lid close
        * Shell font size
        * File manager desktop icons
        * Titlebar click action
        * Shell clock to show date
        * Font hinting and antialiasing 

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

autoreconf -i -f

%build
PYTHON=%{__python}
export PYTHON
%configure
make %{?_smp_mflags}


%install
PYTHON=%{__python}
export PYTHON
make install DESTDIR=$RPM_BUILD_ROOT

sed -i '1s|^#!/usr/bin/env python|#!%{__python}|' $RPM_BUILD_ROOT%{_bindir}/%{name}

%find_lang %{name}


%check
# Leave the desktop file validation, but don't return an error value ("Phanteon"
# value not supported yet by validator in "OnlyShowIn" key)
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop || true


%post
/bin/touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/%{name}
%{python_sitelib}/gtweak/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libexecdir}/%{name}-lid-inhibitor


%changelog
* Fri Aug 28 2015 Rui Matos <rmatos@redhat.com> - 3.14.3-2
- Fix a crash when classic session gsettings schema isn't available
Resolves: #1256644

* Sat Apr 11 2015 Kalev Lember <kalevlember@gmail.com> - 3.14.3-1
- Update to 3.14.3

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.12.0-1
- Update to 3.12.0

* Wed Nov 20 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.10.1-2
- Drop now useless dependency on Nautilus (RHBZ #1030449)

* Wed Nov 13 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Sat Oct 19 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.10.0-2
- Fix extension update checks
- Fix RHBZ #1017801

* Wed Sep 25 2013 Mohamed El Morabity - 3.10.0-1
- Update to 3.10.0

* Thu Sep 19 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.9.92-1
- Update to 3.9.92

* Wed Sep 04 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90.1-1
- Update to 3.9.90.1

* Thu Aug 22 2013 Adam Williamson <awilliam@redhat.com> - 3.9.90-1
- bump to latest version
- drop shell_themes.patch as #703760 is marked FIXED

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.8.1-1
- Update to 3.8.1
- Drop gnome-tweak-tool-3.8.0-pref.js.patch patch (merged upstream)

* Sun Jul 07 2013 Mohamed El Morabity <pikachu.2014@gmail.com> - 3.8.0-3
- Add patch to make gnome-tweak-tool look shell themes only in ~/.themes

* Sat May 25 2013 Mohamed El Morabity <pikachu.2014@gmail.com> - 3.8.0-2
- Add patch to allow pref.js for system extensions (thanks to Ralph Bean)

* Mon Apr 08 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.8.0-1
- Update to 3.8.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.7.4-1
- Update to 3.7.4
- Drop remove_lid_close_settings patch, fixed upstream
- Spec cleanup

* Fri Nov  2 2012 Michel Salim <salimma@fedoraproject.org> - 3.6.1-2
- Drop lid close configuration options that are now handled by systemd

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Oct  3 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Aug  9 2012 Michel Salim <salimma@fedoraproject.org> - 3.5.4-1
- Update to 3.5.4

* Sun Aug  5 2012 Michel Salim <salimma@fedoraproject.org> - 3.5.0-0.1.20120717git3869087
- Update to 3.5.0 snapshot for GNOME 3.5.x compatibility

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun  4 2012 Michel Salim <salimma@fedoraproject.org> - 3.4.0.1-2
- Add R: on user theme extension (# 826129)

* Mon May 14 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Mon May 14 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Sat Jan 21 2012 Michel Salim <salimma@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Michel Salim <salimma@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Thu Sep  1 2011 Michel Salim <salimma@fedoraproject.org> - 3.1.90-1
- Update to 3.1.90

* Sun Aug 21 2011 Michel Salim <salimma@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Tue Jul 19 2011 Michel Salim <salimma@fedoraproject.org> - 3.0.5-2
- Depend on nautilus (# 722541)

* Thu Jun 30 2011 Michel Salim <salimma@fedoraproject.org> - 3.0.5-1
- Update to 3.0.5
- upstream news:
  http://ftp.gnome.org/pub/GNOME/sources/gnome-tweak-tool/3.0/gnome-tweak-tool-3.0.5.news
  * autostart fixes
  * appearance improvements
  * focus follow mouse mode
  * finer-grained desktop item visibility
  * streamlined shell restart offer when enabling extensions

* Mon Jun 13 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4
- Dropped redundant commented out lines in spec
- Updated description
- Dropped defattr since it is set by default in recent RPM
- http://ftp.gnome.org/pub/GNOME/sources/gnome-tweak-tool/3.0/gnome-tweak-tool-3.0.4.news
  * Enables support for system wide themes
  * Supports management of shell extensions 

* Wed May  4 2011 Michel Salim <salimma@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3

* Mon Apr  4 2011 Michel Salim <salimma@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.93-2
- Enable icon theme selection

* Fri Mar 25 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.92-3
- Include license information

* Tue Mar 22 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.92-2
- Use %%configure macro
- Validate desktop file

* Mon Mar 21 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.92-1
- Initial package
