%global gsettings_desktop_schemas_version 3.21.2

%global major_version %%(cut -d "." -f 1-2 <<<%{version})

Name:           gnome-tweak-tool
Version:        3.22.0
Release:        2%{?dist}
Summary:        A tool to customize advanced GNOME 3 options

License:        GPLv3
URL:            https://wiki.gnome.org/Apps/GnomeTweakTool
Source0:        https://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{version}.tar.xz

Patch0: 0001-gshellwrapper-Add-missing-extension-state-and-type.patch
Patch1: 0002-gshellwrapper-Proxy-the-extension-status-changed-sig.patch
Patch2: 0003-shell_extensions-Add-remove-tweaks-as-extensions-are.patch
Patch3: 0004-shell_extensions-Add-a-sort-func-to-keep-the-list-or.patch
Patch4: 0005-ExtensionInstaller-load-extension-after-installing-i.patch
Patch5: 0006-shell_extensions-SESSION_MODE-extensions-can-t-be-en.patch
Patch6: 0007-GSettingsFontButtonTweak-filter-out-fonts-that-gtk-3.patch
Patch7: 0008-font-Remove-document-font-tweak-since-nothing-honors.patch
# https://gitlab.gnome.org/GNOME/gnome-tweaks/commit/34d6d451d7c25482c65c09220ef979aae8101d9d
Patch8: gnome-tweak-tool-remove-scaling-factor.patch

BuildArch:      noarch
BuildRequires:  intltool
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       gnome-shell
Requires:       gnome-shell-extension-user-theme
Requires:       gsettings-desktop-schemas >= %{gsettings_desktop_schemas_version}
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

autoreconf -i -f

%build
PYTHON=%{__python}
export PYTHON
%configure
make %{?_smp_mflags}


%install
PYTHON=%{__python}
export PYTHON
%make_install

sed -i '1s|^#!/usr/bin/env python|#!%{__python}|' $RPM_BUILD_ROOT%{_bindir}/%{name}

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/gnome-tweak-tool.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gnome-tweak-tool/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gnome-tweak-tool/b.png 

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
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/%{name}
%{_libexecdir}/gnome-tweak-tool-lid-inhibitor
%{python_sitelib}/gtweak/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/gnome-tweak-tool-symbolic.svg


%changelog
* Fri Apr 13 2018 Kalev Lember <klember@redhat.com> - 3.22.0-2
- Remove scaling factor setting, moved to control-center in RHEL 7.5
- Resolves: #1567040

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Tue Sep 06 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91
- Set minimum required gsettings-desktop-schemas version
- Update project URLs

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Wed Mar 23 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Aug 18 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Thu Apr 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.16.0-2
- Use better AppData screenshots

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING file

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

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
