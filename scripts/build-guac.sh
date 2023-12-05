#!/bin/bash
#set -e

cd guacamole-server

# find / -name '*.dll' | xargs -d'\n' grep mingw_app_type
# exit 1

export PKG_CONFIG_PATH="/mingw64/lib/pkgconfig"

# mkdir "$PKG_CONFIG_PATH/potato"

# # cp -v $PKG_CONFIG_PATH/pango* "$PKG_CONFIG_PATH/potato"
# # cp -v $PKG_CONFIG_PATH/cairo* "$PKG_CONFIG_PATH/potato"

# # FILES=" \
# #     gobject-2.0.pc \
# #     glib-2.0.pc \
# #     libpcre2-8.pc \
# #     libswscale.pc \
# #     libffi.pc \
# #     harfbuzz.pc \
# #     freetype2.pc \
# #     zlib.pc \
# #     libpng.pc \
# #     libbrotlidec.pc \
# #     libbrotlicommon.pc \
# #     graphite2.pc \
# #     gio-2.0.pc \
# #     gmodule-no-export-2.0.pc \
# #     fribidi.pc \
# #     libthai.pc \
# #     datrie-0.2.pc \
# #     fontconfig.pc \
# #     expat.pc \
# #     pixman-1.pc \
# #     harfbuzz-gobject.pc"

# # for FILE in $FILES
# # do
# #     cp -v $PKG_CONFIG_PATH/$FILE "$PKG_CONFIG_PATH/potato"
# # done

# cp -v $PKG_CONFIG_PATH/*ssl* "$PKG_CONFIG_PATH/potato"
# cp -v $PKG_CONFIG_PATH/*rdp* "$PKG_CONFIG_PATH/potato"
# cp -v $PKG_CONFIG_PATH/*winpr* "$PKG_CONFIG_PATH/potato"
# cp -v $PKG_CONFIG_PATH/*crypto* "$PKG_CONFIG_PATH/potato"

# export PKG_CONFIG_PATH="$PKG_CONFIG_PATH/potato"

# rm $PKG_CONFIG_PATH/freerdp*
# rm $PKG_CONFIG_PATH/libav*

export LDFLAGS="-L/mingw64/bin/ -lws2_32 -lssl"
export CFLAGS="-isystem/mingw64/include/ \
               -isystem/usr/x86_64-w64-mingw32/include \
               -I/mingw64/include/pango-1.0 \
               -I/mingw64/include/glib-2.0/ \
               -I/mingw64/lib/glib-2.0/include/ \
               -I/mingw64/include/harfbuzz/ \
               -I/mingw64/include/cairo/ \
               -I/mingw64/include/freerdp2 \
               -I/mingw64/include/winpr2 \
	           -D_WIN32_WINNT=0x0600 -DWINVER=0x0600 \
               -Wno-error=expansion-to-defined -Wno-error=attributes"

autoreconf -fi
./configure --host=x86_64-w64-mingw32 --with-cygwin --disable-guacenc --disable-guacd --disable-guaclog --without-terminal || cat config.log

cat config.log

make V=1 || exit 0
make install # || exit 0
