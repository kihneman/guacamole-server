#!/bin/bash

set -e
set -x

#bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

git clone https://github.com/holyblackcat/quasi-msys2
pushd quasi-msys2

# Use MSVCRT instead of UCRT
echo MINGW64 > msystem.txt

make install \
    mingw-w64-x86_64-cairo \
    mingw-w64-x86_64-gcc \
    mingw-w64-x86_64-gdb \
    mingw-w64-x86_64-libpng \
    mingw-w64-x86_64-libjpeg-turbo \
    mingw-w64-x86_64-freerdp \
    mingw-w64-x86_64-libvncserver \
    mingw-w64-x86_64-dlfcn \
    mingw-w64-x86_64-libgcrypt \
    mingw-w64-x86_64-libwebsockets \
    mingw-w64-x86_64-libwebp \
    mingw-w64-x86_64-openssl \
    mingw-w64-x86_64-libvorbis \
    mingw-w64-x86_64-pulseaudio

