#!/bin/bash
#set -e

cd guacamole-server

export PKG_CONFIG_PATH="/quasi-msys2/root/mingw64/lib/pkgconfig/"
export LDFLAGS="-L/quasi-msys2/root/mingw64/bin/ -lws2_32"
export CFLAGS="-I/quasi-msys2/root/mingw64/include/ \
               -I/usr/x86_64-w64-mingw32/include \
               -I/quasi-msys2/root/mingw64/include/pango-1.0 \
               -I/quasi-msys2/root/mingw64/include/glib-2.0/ \
               -I/quasi-msys2/root/mingw64/lib/glib-2.0/include/ \
               -I/quasi-msys2/root/mingw64/include/harfbuzz/ \
               -I/quasi-msys2/root/mingw64/include/cairo/ \
	       -D_WIN32_WINNT=0x0600 -DWINVER=0x0600"

autoreconf -fi
./configure --host=x86_64-w64-mingw32 --with-cygwin --with-telnet=no --with-rdp=no --disable-kubernetes --disable-guacenc --disable-guacd --disable-guaclog || cat config.log

make
make install
