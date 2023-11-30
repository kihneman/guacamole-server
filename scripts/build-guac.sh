#!/bin/bash
#set -e

cd guacamole-server

# find / -name 'netdb.h'
# exit 1

# cat /quasi-msys2/root/mingw64/include/freerdp2/freerdp/version.h
# exit 1

export PKG_CONFIG_PATH="/quasi-msys2/root/mingw64/lib/pkgconfig/"
export LDFLAGS="-L/quasi-msys2/root/mingw64/bin/ -lws2_32"
export CFLAGS="-isystem/quasi-msys2/root/mingw64/include/ \
               -isystem/usr/x86_64-w64-mingw32/include \
               -I/quasi-msys2/root/mingw64/include/pango-1.0 \
               -I/quasi-msys2/root/mingw64/include/glib-2.0/ \
               -I/quasi-msys2/root/mingw64/lib/glib-2.0/include/ \
               -I/quasi-msys2/root/mingw64/include/harfbuzz/ \
               -I/quasi-msys2/root/mingw64/include/cairo/ \
               -I/quasi-msys2/root/mingw64/include/freerdp2 \
               -I/quasi-msys2/root/mingw64/include/winpr2 \
	           -D_WIN32_WINNT=0x0600 -DWINVER=0x0600 \
               -Wno-error=expansion-to-defined -Wno-error=attributes"

autoreconf -fi
./configure --host=x86_64-w64-mingw32 --with-cygwin --disable-guacenc --disable-guacd --disable-guaclog || cat config.log

make
make install
