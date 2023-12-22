from glob import glob
from itertools import zip_longest
from os import chdir, environ
from os.path import exists, expanduser, join
from subprocess import check_call, check_output


MSYS_PKGS = [
    'autoconf-wrapper',
    'automake-wrapper',
    'diffutils',
    'git',
    'libedit-devel',
    'libtool',
    'make',
    'mingw-w64-x86_64-cairo',
    'mingw-w64-x86_64-dlfcn',
    'mingw-w64-x86_64-freerdp',
    'mingw-w64-x86_64-freetds',
    'mingw-w64-x86_64-gcc',
    'mingw-w64-x86_64-gdb',
    'mingw-w64-x86_64-github-cli',
    'mingw-w64-x86_64-libgcrypt',
    'mingw-w64-x86_64-libgxps',
    'mingw-w64-x86_64-libjpeg-turbo',
    'mingw-w64-x86_64-libmariadbclient',
    'mingw-w64-x86_64-libpng',
    'mingw-w64-x86_64-libssh2',
    'mingw-w64-x86_64-libtool',
    'mingw-w64-x86_64-libvncserver',
    'mingw-w64-x86_64-libvorbis',
    'mingw-w64-x86_64-libwebp',
    'mingw-w64-x86_64-libwebsockets',
    'mingw-w64-x86_64-openssl',
    'mingw-w64-x86_64-pkg-config',
    'mingw-w64-x86_64-postgresql',
    'mingw-w64-x86_64-pulseaudio',
    'mingw-w64-x86_64-python',
    'mingw-w64-x86_64-zlib',
    'msys2-runtime-devel',
    'vim',
    'wget',
]
USR_BIN = join('\\', 'msys64', 'usr', 'bin')
BASH = join(USR_BIN, 'bash.exe')
PACMAN = join(USR_BIN, 'pacman.exe')
PACMAN_KEY = join(USR_BIN, 'pacman-key')


# Add msys2 /usr/bin to PATH
env = environ.copy()
env['PATH'] = f'{USR_BIN};{env["PATH"]}'

if not exists(join('\\', 'msys64')):
    # Install msys2 with the following: msys2-base-x86_64-*.sfx.exe -y -oC:\
    sfx = glob(join(expanduser('~'), 'Downloads', 'msys2-base-x86_64-*.sfx.exe'))[0]
    check_call([sfx, '-y', '-oC:\\'])

    # Init pacman
    # C:\msys64\usr\bin\bash.exe C:\msys64\usr\bin\pacman-key --init
    check_call([BASH, PACMAN_KEY, '--init'], env=env)
    check_call([BASH, PACMAN_KEY, '--populate', 'msys2'], env=env)
else:
    print('Msys2 is already installed')

# Check msys2 packages
cmd = [PACMAN, '-Q']
found_it = iter(check_output(cmd, env=env, encoding='utf8').split())
found_pkgs = {k: v for k, v in zip_longest(found_it, found_it)}
missing_pkgs = [pkg for pkg in MSYS_PKGS if pkg not in found_pkgs]

if len(missing_pkgs) > 0:
    # Install packages with the following: C:\msys64\usr\bin\pacman.exe -Sy --noconfirm
    cmd = [PACMAN, '-Sy', '--noconfirm'] + missing_pkgs
    check_call(cmd, env=env)
else:
    print('Msys2 build packages are already installed')

# Build libguac
cmd = [BASH, '-c', 'pwd']
check_call(cmd, env=env)
cmd = [BASH, './build-win-libguac.sh']
check_call(cmd, env=env)
