#!/usr/bin/bash

GUACD_BASE="guacamole-server"
# GUACD_REPO="jmuehlner/$GUACD_BASE"
# GUACD_BRANCH="GUACAMOLE-1841-mingw-build"
GUACD_REPO="kihneman/$GUACD_BASE"
GUACD_BRANCH="GUACAMOLE-1841-mingw-build-with-python"
KCM_BASE="kcm"
KCM_REPO="Keeper-Security/$KCM_BASE"
KCM_BRANCH="windows-build-test-no-cygwin"
FIX_LINKS="$KCM_BASE/windows-scripts/fix-links.sh"

cd ~ || { echo "Couldn't cd to home directory"; exit 1; }
mkdir -p src
cd src || { echo "Couldn't make and cd to 'src' directory"; exit 1; }

# Clone kcm repo
if [ ! -d "$KCM_BASE" ]; then
  gh repo clone $KCM_REPO || { echo "Couldn't clone repo '$KCM_REPO'"; exit 1; }
fi

# Pull latest commits of branch for building Windows
git -C $KCM_BASE checkout $KCM_BRANCH || { echo "Couldn't checkout branch '$KCM_BRANCH'"; exit 1; }
# git -C $KCM_BASE pull || { echo "Couldn't pull latest commits for branch '$KCM_BRANCH'"; exit 1; }

# Fix links
if [ ! -f "$FIX_LINKS" ]; then
  echo "Script $FIX_LINKS doesn't exist"
  exit 1
fi
bash "$FIX_LINKS" || { echo "Couldn't fix links for Windows"; exit 1; }

# Clone guacd repo
if [ ! -d "$GUACD_BASE" ]; then
  gh repo clone $GUACD_REPO || { echo "Couldn't clone repo '$GUACD_REPO'"; exit 1; }
fi
cd $GUACD_BASE || { echo "Couldn't cd to repo '$GUACD_BASE'"; exit 1; }
git checkout $GUACD_BRANCH || { echo "Couldn't checkout branch '$GUACD_BRANCH'"; exit 1; }
git pull || { echo "Couldn't pull latest commits for branch '$GUACD_BRANCH'"; exit 1; }
git log -n 1

make clean

# Configure
export PKG_CONFIG_PATH="/mingw64/lib/pkgconfig:/usr/lib/pkgconfig"
export PATH="$PATH:/mingw64/bin:/usr/bin"
autoreconf -fi
export LDFLAGS="-L/mingw64/bin/ -L/usr/bin/ -L/mingw64/lib -lws2_32"
export CFLAGS="-isystem/mingw64/include/ \
            -I/mingw64/include/pango-1.0 \
            -I/mingw64/include/glib-2.0/ \
            -I/mingw64/lib/glib-2.0/include/ \
            -I/mingw64/include/harfbuzz/ \
            -I/mingw64/include/cairo/ \
            -I/mingw64/include/freerdp2 \
            -I/mingw64/include/winpr2 \
            -Wno-error=expansion-to-defined -Wno-error=attributes"
./configure --prefix=/mingw64 --with-windows --disable-guacenc --disable-guacd --disable-guaclog || cat config.log

# Build and install
make
make install
ln -sf /mingw64/bin/msys-guac-21.dll /usr/bin/libguac.dll
ln -sf /mingw64/bin/msys-guac-terminal-0.dll /usr/bin/libguac-terminal.dll
