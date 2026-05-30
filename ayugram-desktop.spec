# Avoid possible building crash on aarch64
%ifarch aarch64
    %global _lto_cflags %nil
%endif

# AyuGram Desktop's constants...
%global appname AyuGramDesktop

# Reducing debuginfo verbosity to avoid possible building crash on low-memory devices
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

Name: ayugram-desktop
Version: 6.7.8
Release: 2%{?dist}

# Application and 3rd-party modules licensing:
# * AyuGram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * tg_owt - BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain -- static dependency;
# * rlottie - LGPL-2.1-or-later AND FTL AND BSD-3-Clause -- static dependency;
# * cld3  - Apache-2.0 -- static dependency;
# * open-sans-fonts  - Apache-2.0 -- bundled font;
# * vazirmatn-fonts - OFL-1.1 -- bundled font.
# * lib_icu - Unicode-3.0 -- static dependency;
# * kcoreaddons - MPL-1.1 AND CC0-1.0 AND Artistic-1.0-Perl AND QPL-1.0 -- static dependency;
# * expected-lite - BSL-1.0 -- only header lib
# * minizip - Zlib -- static dependency;
License: GPL-3.0-or-later AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain AND LGPL-2.1-or-later AND FTL AND MPL-1.1 AND OFL-1.1 AND Unicode-3.0 AND BSL-1.0 AND CC0-1.0 AND Zlib AND Artistic-1.0-Perl AND QPL-1.0
URL: https://github.com/AyuGram/%{appname}
Summary: Desktop Telegram client with good customization and Ghost mode

# Upstream doesn't provide full source tarball. AyuGram splited to many git submodules.
# Also it bundles some 3rd-party libraries. In most generating script does
# git clone --recursive --branch "v${VERSION}" ...

# create-ayugram-tarball-full.sh 6.3.10.
Source0: AyuGramDesktop-%{version}-full.tar.gz
Source1: create-ayugram-tarball-full.sh

# Fix searching protobuf cmake module
Patch0: findprotobuf_fix.patch
# Fix compilation with gcc16
Patch1: gcc16.patch
# Fix saving hide premium statuses to config file
Patch2: fix-hide-premium-statuses.patch
# AyuGram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64 aarch64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6GuiPrivate)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6WidgetsPrivate)
BuildRequires: cmake(fmt)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: cmake(ada)

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.68) >= 2.76.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(webkitgtk-6.0)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libdispatch-devel
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: pkgconfig(openh264)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(tde2e)

Requires: hicolor-icon-theme
Requires: qt6-qtimageformats%{?_isa}
Requires: webkitgtk6.0%{?_isa}

# Short alias for the main package...
Provides: ayugram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: ayugram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Virtual provides for bundled libraries...
# https://github.com/google/cld3.git
Provides: bundled(cld3) = 3.0.13~gitb48dc46
 # https://github.com/desktop-app/cmake_helpers.git
Provides: bundled(cmake_helpers) = 0~gitba366ad
# https://github.com/AyuGram/codegen.git
Provides: bundled(codegen) = 0~git1c91960
# https://gitlab.com/mnauw/cppgir.git
Provides: bundled(cppgir) = 2.0~git2a7d9ce
# https://github.com/KDE/kcoreaddons.git
Provides: bundled(kf5-kcoreaddons) = 5.102.0~gitfd84da5
# https://github.com/desktop-app/lib_base.git
Provides: bundled(lib_base) = 0~git444ab33
# https://github.com/desktop-app/lib_crl.git
Provides: bundled(lib_crl) = 0~gita41edfc
# https://github.com/AyuGram/lib_icu.git
Provides: bundled(lib_icu) = 0~gitfd92c31
# https://github.com/desktop-app/lib_lottie.git
Provides: bundled(lib_lottie) = 0~git99d8cc4
# https://github.com/desktop-app/libprisma.git
Provides: bundled(libprisma) = 0~git23b0d70
# https://github.com/desktop-app/lib_qr.git
Provides: bundled(lib_qr) = 0~git6fdf604
# https://github.com/desktop-app/lib_rpl.git
Provides: bundled(lib_rpl) = 0~gitc57cccf
# https://github.com/desktop-app/lib_spellcheck
Provides: bundled(lib_spellcheck) = 0~git476bb43
# https://github.com/desktop-app/lib_storage.git
Provides: bundled(lib_storage) = 0~gitccdc725
# https://github.com/AyuGram/lib_tl.git
Provides: bundled(lib_tl) = 0~git6a1bf6b
# https://github.com/AyuGram/lib_ui.git
Provides: bundled(lib_ui) = 0~gitb1710a6
# https://github.com/desktop-app/lib_webrtc.git
Provides: bundled(lib_webrtc) = 0~git553102f
# https://github.com/desktop-app/lib_webview.git
Provides: bundled(lib_webview) = 0~git55ea117
# https://github.com/desktop-app/rlottie.git
Provides: bundled(rlottie) = 0~git8c69fc2
# https://github.com/TelegramMessenger/tgcalls.git
Provides: bundled(tgcalls) = ios_release_11.13~git24876eb
# https://github.com/flatpak/xdg-desktop-portal.git
Provides: bundled(xdg-desktop-portal) = 1.20.1~git23a76c3
Provides: bundled(vazirmatn-fonts) = 27.2.2
Provides: bundled(minizip) = 1.2.13

%description
AyuGram is a Telegram client with a very pleasant features.

Telegram is a messaging app with a focus on speed and security, it's
super-fast, simple and free. You can use Telegram on all your devices at the
same time - your messages sync seamlessly across any number of your phones,
tablets or computers.

AyuGram pretends to be an official application to Telegram.
If you look at the list of sessions, you'll see yourself using a regular
Telegram rather than AyuGram. Generally, developer ToS apply only to
developers, by restricting their application keys. But since we're using
official ones, Telegram can't block our client. And since it's applied only to
developers, they can't ban you, except if you're doing bad things that violate
user ToS.

We are not responsible for the possible blocking of your account. Use the
client at your own risk.

%prep
# Unpacking AyuGram Desktop source archive...
%autosetup -n %{appname}-%{version}-full -p1

# Unbundling libraries... except minizip
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx5-qt,hime,hunspell,kimageformats,lz4,nimf,range-v3,xxHash}

%build
# Building AyuGram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_ID=2040 \
    -DTDESKTOP_API_HASH=b18441a1ff607e10a989891a5462e627 \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_QT_PLUGINS:BOOL=ON
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.ayugram.desktop.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/com.ayugram.desktop.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/AyuGram
%{_datadir}/applications/com.ayugram.desktop.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/dbus-1/services/com.ayugram.desktop.service
%{_metainfodir}/com.ayugram.desktop.metainfo.xml

%changelog
* Wed May 06 2026 Ivan Romanov <drizt72@zoho.eu> - 6.7.8-2
- Add patch fix-hide-premium-statuses.patch

* Mon Apr 27 2026 Ivan Romanov <drizt72@zoho.eu> - 6.7.8-1
- Bump to 6.7.8

* Fri Mar 20 2026 Nicolas Chauvet <kwizart@gmail.com> - 6.3.10-2
- Rebuilt for libvpx-1.16.0

* Mon Feb 02 2026 Ivan Romanov <drizt72@zoho.eu> - 6.3.10-1
- Initial version based on RPM Fusion tdesktop package
