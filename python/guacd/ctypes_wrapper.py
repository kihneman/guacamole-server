r"""Wrapper for ctypes_wrapper.h

Generated with:
/usr/bin/ctypesgen -llibguacd -L /opt/guacamole/lib -I /opt/guacamole/include -o ctypes_wrapper.py src/guacd/ctypes_wrapper.h src/libguac/guacamole/socket.h src/libguac/guacamole/protocol.h

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
    # Some builds of ctypes apparently do not have ctypes.c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
        c_ptrdiff_t = t
del t
del _int_types



class UserString:
    def __init__(self, seq):
        if isinstance(seq, bytes):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq).encode()

    def __bytes__(self):
        return self.data

    def __str__(self):
        return self.data.decode()

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data.decode())

    def __long__(self):
        return int(self.data.decode())

    def __float__(self):
        return float(self.data.decode())

    def __complex__(self):
        return complex(self.data.decode())

    def __hash__(self):
        return hash(self.data)

    def __le__(self, string):
        if isinstance(string, UserString):
            return self.data <= string.data
        else:
            return self.data <= string

    def __lt__(self, string):
        if isinstance(string, UserString):
            return self.data < string.data
        else:
            return self.data < string

    def __ge__(self, string):
        if isinstance(string, UserString):
            return self.data >= string.data
        else:
            return self.data >= string

    def __gt__(self, string):
        if isinstance(string, UserString):
            return self.data > string.data
        else:
            return self.data > string

    def __eq__(self, string):
        if isinstance(string, UserString):
            return self.data == string.data
        else:
            return self.data == string

    def __ne__(self, string):
        if isinstance(string, UserString):
            return self.data != string.data
        else:
            return self.data != string

    def __contains__(self, char):
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.__class__(self.data[index])

    def __getslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other).encode())

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other).encode() + self.data)

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self):
        return self.__class__(self.data.capitalize())

    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))

    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)

    def decode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())

    def encode(self, encoding=None, errors=None):  # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))

    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return self.data.join(seq)

    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))

    def lower(self):
        return self.__class__(self.data.lower())

    def lstrip(self, chars=None):
        return self.__class__(self.data.lstrip(chars))

    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))

    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))

    def rpartition(self, sep):
        return self.data.rpartition(sep)

    def rstrip(self, chars=None):
        return self.__class__(self.data.rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def splitlines(self, keepends=0):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.__class__(self.data.strip(chars))

    def swapcase(self):
        return self.__class__(self.data.swapcase())

    def title(self):
        return self.__class__(self.data.title())

    def translate(self, *args):
        return self.__class__(self.data.translate(*args))

    def upper(self):
        return self.__class__(self.data.upper())

    def zfill(self, width):
        return self.__class__(self.data.zfill(width))


class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""

    def __init__(self, string=""):
        self.data = string

    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")

    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + sub + self.data[index + 1 :]

    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data):
            raise IndexError
        self.data = self.data[:index] + self.data[index + 1 :]

    def __setslice__(self, start, end, sub):
        start = max(start, 0)
        end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start] + sub.data + self.data[end:]
        elif isinstance(sub, bytes):
            self.data = self.data[:start] + sub + self.data[end:]
        else:
            self.data = self.data[:start] + str(sub).encode() + self.data[end:]

    def __delslice__(self, start, end):
        start = max(start, 0)
        end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]

    def immutable(self):
        return UserString(self.data)

    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, bytes):
            self.data += other
        else:
            self.data += str(other).encode()
        return self

    def __imul__(self, n):
        self.data *= n
        return self


class String(MutableString, ctypes.Union):

    _fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

    def __init__(self, obj=b""):
        if isinstance(obj, (bytes, UserString)):
            self.data = bytes(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(ctypes.POINTER(ctypes.c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from bytes
        elif isinstance(obj, bytes):
            return cls(obj)

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj.encode())

        # Convert from c_char_p
        elif isinstance(obj, ctypes.c_char_p):
            return obj

        # Convert from POINTER(ctypes.c_char)
        elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

        # Convert from ctypes.c_char array
        elif isinstance(obj, ctypes.c_char * len(obj)):
            return obj

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)

    from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
    if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
        return type
    else:
        return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self, func, restype, argtypes, errcheck):
        self.func = func
        self.func.restype = restype
        self.argtypes = argtypes
        if errcheck:
            self.func.errcheck = errcheck

    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func

    def __call__(self, *args):
        fixed_args = []
        i = 0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i += 1
        return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
    """
    Simple helper used for casts to simple builtin types:  if the argument is a
    string type, it will be converted to it's ordinal value.

    This function will raise an exception if the argument is string with more
    than one characters.
    """
    return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = ['/opt/guacamole/lib']

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
    """Split an environment variable into a path-like list elements"""
    if name in os.environ:
        return os.environ[name].split(":")
    return []


class LibraryLoader:
    """
    A base class For loading of libraries ;-)
    Subclasses load libraries for specific platforms.
    """

    # library names formatted specifically for platforms
    name_formats = ["%s"]

    class Lookup:
        """Looking up calling conventions for a platform"""

        mode = ctypes.DEFAULT_MODE

        def __init__(self, path):
            super(LibraryLoader.Lookup, self).__init__()
            self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

        def get(self, name, calling_convention="cdecl"):
            """Return the given name according to the selected calling convention"""
            if calling_convention not in self.access:
                raise LookupError(
                    "Unknown calling convention '{}' for function '{}'".format(
                        calling_convention, name
                    )
                )
            return getattr(self.access[calling_convention], name)

        def has(self, name, calling_convention="cdecl"):
            """Return True if this given calling convention finds the given 'name'"""
            if calling_convention not in self.access:
                return False
            return hasattr(self.access[calling_convention], name)

        def __getattr__(self, name):
            return getattr(self.access["cdecl"], name)

    def __init__(self):
        self.other_dirs = []

    def __call__(self, libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            # noinspection PyBroadException
            try:
                return self.Lookup(path)
            except Exception:  # pylint: disable=broad-except
                pass

        raise ImportError("Could not load %s." % libname)

    def getpaths(self, libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # search through a prioritized series of locations for the library

            # we first search any specific directories identified by user
            for dir_i in self.other_dirs:
                for fmt in self.name_formats:
                    # dir_i should be absolute already
                    yield os.path.join(dir_i, fmt % libname)

            # check if this code is even stored in a physical file
            try:
                this_file = __file__
            except NameError:
                this_file = None

            # then we search the directory where the generated python interface is stored
            if this_file is not None:
                for fmt in self.name_formats:
                    yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

            # now, use the ctypes tools to try to find the library
            for fmt in self.name_formats:
                path = ctypes.util.find_library(fmt % libname)
                if path:
                    yield path

            # then we search all paths identified as platform-specific lib paths
            for path in self.getplatformpaths(libname):
                yield path

            # Finally, we'll try the users current working directory
            for fmt in self.name_formats:
                yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

    def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
        """Return all the library paths available in this platform"""
        return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
    """Library loader for MacOS"""

    name_formats = [
        "lib%s.dylib",
        "lib%s.so",
        "lib%s.bundle",
        "%s.dylib",
        "%s.so",
        "%s.bundle",
        "%s",
    ]

    class Lookup(LibraryLoader.Lookup):
        """
        Looking up library files for this platform (Darwin aka MacOS)
        """

        # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
        # of the default RTLD_LOCAL.  Without this, you end up with
        # libraries not being loadable, resulting in "Symbol not found"
        # errors
        mode = ctypes.RTLD_GLOBAL

    def getplatformpaths(self, libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [fmt % libname for fmt in self.name_formats]

        for directory in self.getdirs(libname):
            for name in names:
                yield os.path.join(directory, name)

    @staticmethod
    def getdirs(libname):
        """Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        """

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [
                os.path.expanduser("~/lib"),
                "/usr/local/lib",
                "/usr/lib",
            ]

        dirs = []

        if "/" in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
            dirs.extend(_environ_path("LD_RUN_PATH"))

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
            dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

        dirs.extend(dyld_fallback_library_path)

        return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
    """Library loader for POSIX-like systems (including Linux)"""

    _ld_so_cache = None

    _include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

    name_formats = ["lib%s.so", "%s.so", "%s"]

    class _Directories(dict):
        """Deal with directories"""

        def __init__(self):
            dict.__init__(self)
            self.order = 0

        def add(self, directory):
            """Add a directory to our current set of directories"""
            if len(directory) > 1:
                directory = directory.rstrip(os.path.sep)
            # only adds and updates order if exists and not already in set
            if not os.path.exists(directory):
                return
            order = self.setdefault(directory, self.order)
            if order == self.order:
                self.order += 1

        def extend(self, directories):
            """Add a list of directories to our set"""
            for a_dir in directories:
                self.add(a_dir)

        def ordered(self):
            """Sort the list of directories"""
            return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

    def _get_ld_so_conf_dirs(self, conf, dirs):
        """
        Recursive function to help parse all ld.so.conf files, including proper
        handling of the `include` directive.
        """

        try:
            with open(conf) as fileobj:
                for dirname in fileobj:
                    dirname = dirname.strip()
                    if not dirname:
                        continue

                    match = self._include.match(dirname)
                    if not match:
                        dirs.add(dirname)
                    else:
                        for dir2 in glob.glob(match.group("pattern")):
                            self._get_ld_so_conf_dirs(dir2, dirs)
        except IOError:
            pass

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = self._Directories()
        for name in (
            "LD_LIBRARY_PATH",
            "SHLIB_PATH",  # HP-UX
            "LIBPATH",  # OS/2, AIX
            "LIBRARY_PATH",  # BE/OS
        ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))

        self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

        bitage = platform.architecture()[0]

        unix_lib_dirs_list = []
        if bitage.startswith("64"):
            # prefer 64 bit if that is our arch
            unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

        # must include standard libs, since those paths are also used by 64 bit
        # installs
        unix_lib_dirs_list += ["/lib", "/usr/lib"]
        if sys.platform.startswith("linux"):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            if bitage.startswith("32"):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
            elif bitage.startswith("64"):
                # Assume Intel/AMD x86 compatible
                unix_lib_dirs_list += [
                    "/lib/x86_64-linux-gnu",
                    "/usr/lib/x86_64-linux-gnu",
                ]
            else:
                # guess...
                unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r"lib(.*)\.s[ol]")
        # ext_re = re.compile(r"\.s[ol]$")
        for our_dir in directories.ordered():
            try:
                for path in glob.glob("%s/*.s[ol]*" % our_dir):
                    file = os.path.basename(path)

                    # Index by filename
                    cache_i = cache.setdefault(file, set())
                    cache_i.add(path)

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        cache_i = cache.setdefault(library, set())
                        cache_i.add(path)
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname, set())
        for i in result:
            # we iterate through all found paths for library, since we may have
            # actually found multiple architectures or other library types that
            # may not load
            yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
    """Library loader for Microsoft Windows"""

    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

    class Lookup(LibraryLoader.Lookup):
        """Lookup class for Windows libraries..."""

        def __init__(self, path):
            super(WindowsLibraryLoader.Lookup, self).__init__(path)
            self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin": DarwinLibraryLoader,
    "cygwin": WindowsLibraryLoader,
    "win32": WindowsLibraryLoader,
    "msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
    """
    Add libraries to search paths.
    If library paths are relative, convert them to absolute with respect to this
    file's directory
    """
    for path in other_dirs:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs(['/opt/guacamole/lib'])

# Begin libraries
_libs["libguacd"] = load_library("libguacd")

# 1 libraries
# End libraries

# No modules

# /opt/guacamole/include/guacamole/client-types.h: 35
class struct_guac_client(Structure):
    pass

guac_client = struct_guac_client# /opt/guacamole/include/guacamole/client-types.h: 35

enum_guac_client_log_level = c_int# /opt/guacamole/include/guacamole/client-types.h: 94

guac_client_log_level = enum_guac_client_log_level# /opt/guacamole/include/guacamole/client-types.h: 94

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 70
class struct_guacd_config(Structure):
    pass

struct_guacd_config.__slots__ = [
    'bind_host',
    'bind_port',
    'pidfile',
    'foreground',
    'print_version',
    'max_log_level',
]
struct_guacd_config._fields_ = [
    ('bind_host', String),
    ('bind_port', String),
    ('pidfile', String),
    ('foreground', c_int),
    ('print_version', c_int),
    ('max_log_level', guac_client_log_level),
]

guacd_config = struct_guacd_config# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 70

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 78
if _libs["libguacd"].has("guacd_conf_load", "cdecl"):
    guacd_conf_load = _libs["libguacd"].get("guacd_conf_load", "cdecl")
    guacd_conf_load.argtypes = []
    guacd_conf_load.restype = POINTER(guacd_config)

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 86
if _libs["libguacd"].has("guacd_conf_parse_args", "cdecl"):
    guacd_conf_parse_args = _libs["libguacd"].get("guacd_conf_parse_args", "cdecl")
    guacd_conf_parse_args.argtypes = [POINTER(guacd_config), c_int, POINTER(POINTER(c_char))]
    guacd_conf_parse_args.restype = c_int

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 99
if _libs["libguacd"].has("guacd_log", "cdecl"):
    _func = _libs["libguacd"].get("guacd_log", "cdecl")
    _restype = None
    _errcheck = None
    _argtypes = [guac_client_log_level, String]
    guacd_log = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 102
if _libs["libguacd"].has("main", "cdecl"):
    main = _libs["libguacd"].get("main", "cdecl")
    main.argtypes = [c_int, POINTER(POINTER(c_char))]
    main.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 39
class struct_guac_socket(Structure):
    pass

guac_socket = struct_guac_socket# /tmp/guacamole-server/src/libguac/guacamole/socket-types.h: 33

enum_guac_socket_state = c_int# /tmp/guacamole-server/src/libguac/guacamole/socket-types.h: 50

guac_socket_state = enum_guac_socket_state# /tmp/guacamole-server/src/libguac/guacamole/socket-types.h: 50

guac_socket_read_handler = CFUNCTYPE(UNCHECKED(c_ptrdiff_t), POINTER(guac_socket), POINTER(None), c_size_t)# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 43

guac_socket_write_handler = CFUNCTYPE(UNCHECKED(c_ptrdiff_t), POINTER(guac_socket), POINTER(None), c_size_t)# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 56

guac_socket_select_handler = CFUNCTYPE(UNCHECKED(c_int), POINTER(guac_socket), c_int)# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 70

guac_socket_flush_handler = CFUNCTYPE(UNCHECKED(c_ptrdiff_t), POINTER(guac_socket))# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 83

guac_socket_lock_handler = CFUNCTYPE(UNCHECKED(None), POINTER(guac_socket))# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 93

guac_socket_unlock_handler = CFUNCTYPE(UNCHECKED(None), POINTER(guac_socket))# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 103

guac_socket_free_handler = CFUNCTYPE(UNCHECKED(c_int), POINTER(guac_socket))# /tmp/guacamole-server/src/libguac/guacamole/socket-fntypes.h: 113

guac_timestamp = c_int64# /tmp/guacamole-server/src/libguac/guacamole/timestamp-types.h: 34

# /usr/include/bits/alltypes.h: 273
class struct___pthread(Structure):
    pass

pthread_t = POINTER(struct___pthread)# /usr/include/bits/alltypes.h: 273

struct_guac_socket.__slots__ = [
    'data',
    'read_handler',
    'write_handler',
    'flush_handler',
    'lock_handler',
    'unlock_handler',
    'select_handler',
    'free_handler',
    'state',
    'last_write_timestamp',
    '__ready',
    '__ready_buf',
    '__encoded_buf',
    '__keep_alive_enabled',
    '__keep_alive_thread',
]
struct_guac_socket._fields_ = [
    ('data', POINTER(None)),
    ('read_handler', POINTER(guac_socket_read_handler)),
    ('write_handler', POINTER(guac_socket_write_handler)),
    ('flush_handler', POINTER(guac_socket_flush_handler)),
    ('lock_handler', POINTER(guac_socket_lock_handler)),
    ('unlock_handler', POINTER(guac_socket_unlock_handler)),
    ('select_handler', POINTER(guac_socket_select_handler)),
    ('free_handler', POINTER(guac_socket_free_handler)),
    ('state', guac_socket_state),
    ('last_write_timestamp', guac_timestamp),
    ('__ready', c_int),
    ('__ready_buf', c_ubyte * int(768)),
    ('__encoded_buf', c_char * int(1024)),
    ('__keep_alive_enabled', c_int),
    ('__keep_alive_thread', pthread_t),
]

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 130
if _libs["libguacd"].has("guac_socket_alloc", "cdecl"):
    guac_socket_alloc = _libs["libguacd"].get("guac_socket_alloc", "cdecl")
    guac_socket_alloc.argtypes = []
    guac_socket_alloc.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 137
if _libs["libguacd"].has("guac_socket_free", "cdecl"):
    guac_socket_free = _libs["libguacd"].get("guac_socket_free", "cdecl")
    guac_socket_free.argtypes = [POINTER(guac_socket)]
    guac_socket_free.restype = None

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 147
if _libs["libguacd"].has("guac_socket_require_keep_alive", "cdecl"):
    guac_socket_require_keep_alive = _libs["libguacd"].get("guac_socket_require_keep_alive", "cdecl")
    guac_socket_require_keep_alive.argtypes = [POINTER(guac_socket)]
    guac_socket_require_keep_alive.restype = None

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 155
if _libs["libguacd"].has("guac_socket_instruction_begin", "cdecl"):
    guac_socket_instruction_begin = _libs["libguacd"].get("guac_socket_instruction_begin", "cdecl")
    guac_socket_instruction_begin.argtypes = [POINTER(guac_socket)]
    guac_socket_instruction_begin.restype = None

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 163
if _libs["libguacd"].has("guac_socket_instruction_end", "cdecl"):
    guac_socket_instruction_end = _libs["libguacd"].get("guac_socket_instruction_end", "cdecl")
    guac_socket_instruction_end.argtypes = [POINTER(guac_socket)]
    guac_socket_instruction_end.restype = None

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 178
if _libs["libguacd"].has("guac_socket_open", "cdecl"):
    guac_socket_open = _libs["libguacd"].get("guac_socket_open", "cdecl")
    guac_socket_open.argtypes = [c_int]
    guac_socket_open.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 202
if _libs["libguacd"].has("guac_socket_nest", "cdecl"):
    guac_socket_nest = _libs["libguacd"].get("guac_socket_nest", "cdecl")
    guac_socket_nest.argtypes = [POINTER(guac_socket), c_int]
    guac_socket_nest.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 234
if _libs["libguacd"].has("guac_socket_tee", "cdecl"):
    guac_socket_tee = _libs["libguacd"].get("guac_socket_tee", "cdecl")
    guac_socket_tee.argtypes = [POINTER(guac_socket), POINTER(guac_socket)]
    guac_socket_tee.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 260
if _libs["libguacd"].has("guac_socket_broadcast", "cdecl"):
    guac_socket_broadcast = _libs["libguacd"].get("guac_socket_broadcast", "cdecl")
    guac_socket_broadcast.argtypes = [POINTER(guac_client)]
    guac_socket_broadcast.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 286
if _libs["libguacd"].has("guac_socket_broadcast_pending", "cdecl"):
    guac_socket_broadcast_pending = _libs["libguacd"].get("guac_socket_broadcast_pending", "cdecl")
    guac_socket_broadcast_pending.argtypes = [POINTER(guac_client)]
    guac_socket_broadcast_pending.restype = POINTER(guac_socket)

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 300
if _libs["libguacd"].has("guac_socket_write_int", "cdecl"):
    guac_socket_write_int = _libs["libguacd"].get("guac_socket_write_int", "cdecl")
    guac_socket_write_int.argtypes = [POINTER(guac_socket), c_int64]
    guac_socket_write_int.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 314
if _libs["libguacd"].has("guac_socket_write_string", "cdecl"):
    guac_socket_write_string = _libs["libguacd"].get("guac_socket_write_string", "cdecl")
    guac_socket_write_string.argtypes = [POINTER(guac_socket), String]
    guac_socket_write_string.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 332
if _libs["libguacd"].has("guac_socket_write_base64", "cdecl"):
    guac_socket_write_base64 = _libs["libguacd"].get("guac_socket_write_base64", "cdecl")
    guac_socket_write_base64.argtypes = [POINTER(guac_socket), POINTER(None), c_size_t]
    guac_socket_write_base64.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 346
if _libs["libguacd"].has("guac_socket_write", "cdecl"):
    guac_socket_write = _libs["libguacd"].get("guac_socket_write", "cdecl")
    guac_socket_write.argtypes = [POINTER(guac_socket), POINTER(None), c_size_t]
    guac_socket_write.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 361
if _libs["libguacd"].has("guac_socket_read", "cdecl"):
    guac_socket_read = _libs["libguacd"].get("guac_socket_read", "cdecl")
    guac_socket_read.argtypes = [POINTER(guac_socket), POINTER(None), c_size_t]
    guac_socket_read.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 372
if _libs["libguacd"].has("guac_socket_flush_base64", "cdecl"):
    guac_socket_flush_base64 = _libs["libguacd"].get("guac_socket_flush_base64", "cdecl")
    guac_socket_flush_base64.argtypes = [POINTER(guac_socket)]
    guac_socket_flush_base64.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 383
if _libs["libguacd"].has("guac_socket_flush", "cdecl"):
    guac_socket_flush = _libs["libguacd"].get("guac_socket_flush", "cdecl")
    guac_socket_flush.argtypes = [POINTER(guac_socket)]
    guac_socket_flush.restype = c_ptrdiff_t

# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 401
if _libs["libguacd"].has("guac_socket_select", "cdecl"):
    guac_socket_select = _libs["libguacd"].get("guac_socket_select", "cdecl")
    guac_socket_select.argtypes = [POINTER(guac_socket), c_int]
    guac_socket_select.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/layer-types.h: 32
class struct_guac_layer(Structure):
    pass

guac_layer = struct_guac_layer# /tmp/guacamole-server/src/libguac/guacamole/layer-types.h: 32

# /tmp/guacamole-server/src/libguac/guacamole/object-types.h: 32
class struct_guac_object(Structure):
    pass

guac_object = struct_guac_object# /tmp/guacamole-server/src/libguac/guacamole/object-types.h: 32

enum_guac_protocol_status = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 164

guac_protocol_status = enum_guac_protocol_status# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 164

enum_guac_composite_mode = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 213

guac_composite_mode = enum_guac_composite_mode# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 213

enum_guac_transfer_function = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 259

guac_transfer_function = enum_guac_transfer_function# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 259

enum_guac_line_cap_style = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 268

guac_line_cap_style = enum_guac_line_cap_style# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 268

enum_guac_line_join_style = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 277

guac_line_join_style = enum_guac_line_join_style# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 277

enum_guac_protocol_version = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 318

guac_protocol_version = enum_guac_protocol_version# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 318

enum_guac_message_type = c_int# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 342

guac_message_type = enum_guac_message_type# /tmp/guacamole-server/src/libguac/guacamole/protocol-types.h: 342

# /tmp/guacamole-server/src/libguac/guacamole/stream-types.h: 32
class struct_guac_stream(Structure):
    pass

guac_stream = struct_guac_stream# /tmp/guacamole-server/src/libguac/guacamole/stream-types.h: 32

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 58
if _libs["libguacd"].has("guac_protocol_send_ack", "cdecl"):
    guac_protocol_send_ack = _libs["libguacd"].get("guac_protocol_send_ack", "cdecl")
    guac_protocol_send_ack.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String, guac_protocol_status]
    guac_protocol_send_ack.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 71
if _libs["libguacd"].has("guac_protocol_send_args", "cdecl"):
    guac_protocol_send_args = _libs["libguacd"].get("guac_protocol_send_args", "cdecl")
    guac_protocol_send_args.argtypes = [POINTER(guac_socket), POINTER(POINTER(c_char))]
    guac_protocol_send_args.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 83
if _libs["libguacd"].has("guac_protocol_send_connect", "cdecl"):
    guac_protocol_send_connect = _libs["libguacd"].get("guac_protocol_send_connect", "cdecl")
    guac_protocol_send_connect.argtypes = [POINTER(guac_socket), POINTER(POINTER(c_char))]
    guac_protocol_send_connect.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 94
if _libs["libguacd"].has("guac_protocol_send_disconnect", "cdecl"):
    guac_protocol_send_disconnect = _libs["libguacd"].get("guac_protocol_send_disconnect", "cdecl")
    guac_protocol_send_disconnect.argtypes = [POINTER(guac_socket)]
    guac_protocol_send_disconnect.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 107
if _libs["libguacd"].has("guac_protocol_send_error", "cdecl"):
    guac_protocol_send_error = _libs["libguacd"].get("guac_protocol_send_error", "cdecl")
    guac_protocol_send_error.argtypes = [POINTER(guac_socket), String, guac_protocol_status]
    guac_protocol_send_error.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 133
if _libs["libguacd"].has("guac_protocol_send_key", "cdecl"):
    guac_protocol_send_key = _libs["libguacd"].get("guac_protocol_send_key", "cdecl")
    guac_protocol_send_key.argtypes = [POINTER(guac_socket), c_int, c_int, guac_timestamp]
    guac_protocol_send_key.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 148
if _libs["libguacd"].has("guac_protocol_send_log", "cdecl"):
    _func = _libs["libguacd"].get("guac_protocol_send_log", "cdecl")
    _restype = c_int
    _errcheck = None
    _argtypes = [POINTER(guac_socket), String]
    guac_protocol_send_log = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 171
if _libs["libguacd"].has("vguac_protocol_send_log", "cdecl"):
    vguac_protocol_send_log = _libs["libguacd"].get("vguac_protocol_send_log", "cdecl")
    vguac_protocol_send_log.argtypes = [POINTER(guac_socket), String, c_void_p]
    vguac_protocol_send_log.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 192
if _libs["libguacd"].has("guac_protocol_send_msg", "cdecl"):
    guac_protocol_send_msg = _libs["libguacd"].get("guac_protocol_send_msg", "cdecl")
    guac_protocol_send_msg.argtypes = [POINTER(guac_socket), guac_message_type, POINTER(POINTER(c_char))]
    guac_protocol_send_msg.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 230
if _libs["libguacd"].has("guac_protocol_send_mouse", "cdecl"):
    guac_protocol_send_mouse = _libs["libguacd"].get("guac_protocol_send_mouse", "cdecl")
    guac_protocol_send_mouse.argtypes = [POINTER(guac_socket), c_int, c_int, c_int, guac_timestamp]
    guac_protocol_send_mouse.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 276
if _libs["libguacd"].has("guac_protocol_send_touch", "cdecl"):
    guac_protocol_send_touch = _libs["libguacd"].get("guac_protocol_send_touch", "cdecl")
    guac_protocol_send_touch.argtypes = [POINTER(guac_socket), c_int, c_int, c_int, c_int, c_int, c_double, c_double, guac_timestamp]
    guac_protocol_send_touch.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 300
if _libs["libguacd"].has("guac_protocol_send_nest", "cdecl"):
    guac_protocol_send_nest = _libs["libguacd"].get("guac_protocol_send_nest", "cdecl")
    guac_protocol_send_nest.argtypes = [POINTER(guac_socket), c_int, String]
    guac_protocol_send_nest.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 313
if _libs["libguacd"].has("guac_protocol_send_nop", "cdecl"):
    guac_protocol_send_nop = _libs["libguacd"].get("guac_protocol_send_nop", "cdecl")
    guac_protocol_send_nop.argtypes = [POINTER(guac_socket)]
    guac_protocol_send_nop.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 325
if _libs["libguacd"].has("guac_protocol_send_ready", "cdecl"):
    guac_protocol_send_ready = _libs["libguacd"].get("guac_protocol_send_ready", "cdecl")
    guac_protocol_send_ready.argtypes = [POINTER(guac_socket), String]
    guac_protocol_send_ready.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 339
if _libs["libguacd"].has("guac_protocol_send_set", "cdecl"):
    guac_protocol_send_set = _libs["libguacd"].get("guac_protocol_send_set", "cdecl")
    guac_protocol_send_set.argtypes = [POINTER(guac_socket), POINTER(guac_layer), String, String]
    guac_protocol_send_set.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 365
if _libs["libguacd"].has("guac_protocol_send_set_int", "cdecl"):
    guac_protocol_send_set_int = _libs["libguacd"].get("guac_protocol_send_set_int", "cdecl")
    guac_protocol_send_set_int.argtypes = [POINTER(guac_socket), POINTER(guac_layer), String, c_int]
    guac_protocol_send_set_int.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 378
if _libs["libguacd"].has("guac_protocol_send_select", "cdecl"):
    guac_protocol_send_select = _libs["libguacd"].get("guac_protocol_send_select", "cdecl")
    guac_protocol_send_select.argtypes = [POINTER(guac_socket), String]
    guac_protocol_send_select.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 401
if _libs["libguacd"].has("guac_protocol_send_sync", "cdecl"):
    guac_protocol_send_sync = _libs["libguacd"].get("guac_protocol_send_sync", "cdecl")
    guac_protocol_send_sync.argtypes = [POINTER(guac_socket), guac_timestamp, c_int]
    guac_protocol_send_sync.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 431
if _libs["libguacd"].has("guac_protocol_send_body", "cdecl"):
    guac_protocol_send_body = _libs["libguacd"].get("guac_protocol_send_body", "cdecl")
    guac_protocol_send_body.argtypes = [POINTER(guac_socket), POINTER(guac_object), POINTER(guac_stream), String, String]
    guac_protocol_send_body.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 452
if _libs["libguacd"].has("guac_protocol_send_filesystem", "cdecl"):
    guac_protocol_send_filesystem = _libs["libguacd"].get("guac_protocol_send_filesystem", "cdecl")
    guac_protocol_send_filesystem.argtypes = [POINTER(guac_socket), POINTER(guac_object), String]
    guac_protocol_send_filesystem.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 470
if _libs["libguacd"].has("guac_protocol_send_undefine", "cdecl"):
    guac_protocol_send_undefine = _libs["libguacd"].get("guac_protocol_send_undefine", "cdecl")
    guac_protocol_send_undefine.argtypes = [POINTER(guac_socket), POINTER(guac_object)]
    guac_protocol_send_undefine.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 493
if _libs["libguacd"].has("guac_protocol_send_audio", "cdecl"):
    guac_protocol_send_audio = _libs["libguacd"].get("guac_protocol_send_audio", "cdecl")
    guac_protocol_send_audio.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String]
    guac_protocol_send_audio.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 508
if _libs["libguacd"].has("guac_protocol_send_file", "cdecl"):
    guac_protocol_send_file = _libs["libguacd"].get("guac_protocol_send_file", "cdecl")
    guac_protocol_send_file.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String, String]
    guac_protocol_send_file.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 523
if _libs["libguacd"].has("guac_protocol_send_pipe", "cdecl"):
    guac_protocol_send_pipe = _libs["libguacd"].get("guac_protocol_send_pipe", "cdecl")
    guac_protocol_send_pipe.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String, String]
    guac_protocol_send_pipe.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 540
if _libs["libguacd"].has("guac_protocol_send_blob", "cdecl"):
    guac_protocol_send_blob = _libs["libguacd"].get("guac_protocol_send_blob", "cdecl")
    guac_protocol_send_blob.argtypes = [POINTER(guac_socket), POINTER(guac_stream), POINTER(None), c_int]
    guac_protocol_send_blob.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 571
if _libs["libguacd"].has("guac_protocol_send_blobs", "cdecl"):
    guac_protocol_send_blobs = _libs["libguacd"].get("guac_protocol_send_blobs", "cdecl")
    guac_protocol_send_blobs.argtypes = [POINTER(guac_socket), POINTER(guac_stream), POINTER(None), c_int]
    guac_protocol_send_blobs.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 584
if _libs["libguacd"].has("guac_protocol_send_end", "cdecl"):
    guac_protocol_send_end = _libs["libguacd"].get("guac_protocol_send_end", "cdecl")
    guac_protocol_send_end.argtypes = [POINTER(guac_socket), POINTER(guac_stream)]
    guac_protocol_send_end.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 607
if _libs["libguacd"].has("guac_protocol_send_video", "cdecl"):
    guac_protocol_send_video = _libs["libguacd"].get("guac_protocol_send_video", "cdecl")
    guac_protocol_send_video.argtypes = [POINTER(guac_socket), POINTER(guac_stream), POINTER(guac_layer), String]
    guac_protocol_send_video.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 629
if _libs["libguacd"].has("guac_protocol_send_arc", "cdecl"):
    guac_protocol_send_arc = _libs["libguacd"].get("guac_protocol_send_arc", "cdecl")
    guac_protocol_send_arc.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int, c_int, c_double, c_double, c_int]
    guac_protocol_send_arc.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 648
if _libs["libguacd"].has("guac_protocol_send_cfill", "cdecl"):
    guac_protocol_send_cfill = _libs["libguacd"].get("guac_protocol_send_cfill", "cdecl")
    guac_protocol_send_cfill.argtypes = [POINTER(guac_socket), guac_composite_mode, POINTER(guac_layer), c_int, c_int, c_int, c_int]
    guac_protocol_send_cfill.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 662
if _libs["libguacd"].has("guac_protocol_send_clip", "cdecl"):
    guac_protocol_send_clip = _libs["libguacd"].get("guac_protocol_send_clip", "cdecl")
    guac_protocol_send_clip.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_clip.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 674
if _libs["libguacd"].has("guac_protocol_send_close", "cdecl"):
    guac_protocol_send_close = _libs["libguacd"].get("guac_protocol_send_close", "cdecl")
    guac_protocol_send_close.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_close.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 696
if _libs["libguacd"].has("guac_protocol_send_copy", "cdecl"):
    guac_protocol_send_copy = _libs["libguacd"].get("guac_protocol_send_copy", "cdecl")
    guac_protocol_send_copy.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int, c_int, c_int, guac_composite_mode, POINTER(guac_layer), c_int, c_int]
    guac_protocol_send_copy.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 718
if _libs["libguacd"].has("guac_protocol_send_cstroke", "cdecl"):
    guac_protocol_send_cstroke = _libs["libguacd"].get("guac_protocol_send_cstroke", "cdecl")
    guac_protocol_send_cstroke.argtypes = [POINTER(guac_socket), guac_composite_mode, POINTER(guac_layer), guac_line_cap_style, guac_line_join_style, c_int, c_int, c_int, c_int, c_int]
    guac_protocol_send_cstroke.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 739
if _libs["libguacd"].has("guac_protocol_send_cursor", "cdecl"):
    guac_protocol_send_cursor = _libs["libguacd"].get("guac_protocol_send_cursor", "cdecl")
    guac_protocol_send_cursor.argtypes = [POINTER(guac_socket), c_int, c_int, POINTER(guac_layer), c_int, c_int, c_int, c_int]
    guac_protocol_send_cursor.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 758
if _libs["libguacd"].has("guac_protocol_send_curve", "cdecl"):
    guac_protocol_send_curve = _libs["libguacd"].get("guac_protocol_send_curve", "cdecl")
    guac_protocol_send_curve.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int, c_int, c_int, c_int, c_int]
    guac_protocol_send_curve.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 771
if _libs["libguacd"].has("guac_protocol_send_identity", "cdecl"):
    guac_protocol_send_identity = _libs["libguacd"].get("guac_protocol_send_identity", "cdecl")
    guac_protocol_send_identity.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_identity.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 785
if _libs["libguacd"].has("guac_protocol_send_lfill", "cdecl"):
    guac_protocol_send_lfill = _libs["libguacd"].get("guac_protocol_send_lfill", "cdecl")
    guac_protocol_send_lfill.argtypes = [POINTER(guac_socket), guac_composite_mode, POINTER(guac_layer), POINTER(guac_layer)]
    guac_protocol_send_lfill.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 801
if _libs["libguacd"].has("guac_protocol_send_line", "cdecl"):
    guac_protocol_send_line = _libs["libguacd"].get("guac_protocol_send_line", "cdecl")
    guac_protocol_send_line.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int]
    guac_protocol_send_line.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 819
if _libs["libguacd"].has("guac_protocol_send_lstroke", "cdecl"):
    guac_protocol_send_lstroke = _libs["libguacd"].get("guac_protocol_send_lstroke", "cdecl")
    guac_protocol_send_lstroke.argtypes = [POINTER(guac_socket), guac_composite_mode, POINTER(guac_layer), guac_line_cap_style, guac_line_join_style, c_int, POINTER(guac_layer)]
    guac_protocol_send_lstroke.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 857
if _libs["libguacd"].has("guac_protocol_send_img", "cdecl"):
    guac_protocol_send_img = _libs["libguacd"].get("guac_protocol_send_img", "cdecl")
    guac_protocol_send_img.argtypes = [POINTER(guac_socket), POINTER(guac_stream), guac_composite_mode, POINTER(guac_layer), String, c_int, c_int]
    guac_protocol_send_img.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 871
if _libs["libguacd"].has("guac_protocol_send_pop", "cdecl"):
    guac_protocol_send_pop = _libs["libguacd"].get("guac_protocol_send_pop", "cdecl")
    guac_protocol_send_pop.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_pop.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 883
if _libs["libguacd"].has("guac_protocol_send_push", "cdecl"):
    guac_protocol_send_push = _libs["libguacd"].get("guac_protocol_send_push", "cdecl")
    guac_protocol_send_push.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_push.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 899
if _libs["libguacd"].has("guac_protocol_send_rect", "cdecl"):
    guac_protocol_send_rect = _libs["libguacd"].get("guac_protocol_send_rect", "cdecl")
    guac_protocol_send_rect.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int, c_int, c_int]
    guac_protocol_send_rect.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 916
if _libs["libguacd"].has("guac_protocol_send_required", "cdecl"):
    guac_protocol_send_required = _libs["libguacd"].get("guac_protocol_send_required", "cdecl")
    guac_protocol_send_required.argtypes = [POINTER(guac_socket), POINTER(POINTER(c_char))]
    guac_protocol_send_required.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 928
if _libs["libguacd"].has("guac_protocol_send_reset", "cdecl"):
    guac_protocol_send_reset = _libs["libguacd"].get("guac_protocol_send_reset", "cdecl")
    guac_protocol_send_reset.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_reset.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 942
if _libs["libguacd"].has("guac_protocol_send_start", "cdecl"):
    guac_protocol_send_start = _libs["libguacd"].get("guac_protocol_send_start", "cdecl")
    guac_protocol_send_start.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int]
    guac_protocol_send_start.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 965
if _libs["libguacd"].has("guac_protocol_send_transfer", "cdecl"):
    guac_protocol_send_transfer = _libs["libguacd"].get("guac_protocol_send_transfer", "cdecl")
    guac_protocol_send_transfer.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int, c_int, c_int, guac_transfer_function, POINTER(guac_layer), c_int, c_int]
    guac_protocol_send_transfer.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 985
if _libs["libguacd"].has("guac_protocol_send_transform", "cdecl"):
    guac_protocol_send_transform = _libs["libguacd"].get("guac_protocol_send_transform", "cdecl")
    guac_protocol_send_transform.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_double, c_double, c_double, c_double, c_double, c_double]
    guac_protocol_send_transform.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1002
if _libs["libguacd"].has("guac_protocol_send_dispose", "cdecl"):
    guac_protocol_send_dispose = _libs["libguacd"].get("guac_protocol_send_dispose", "cdecl")
    guac_protocol_send_dispose.argtypes = [POINTER(guac_socket), POINTER(guac_layer)]
    guac_protocol_send_dispose.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1020
if _libs["libguacd"].has("guac_protocol_send_distort", "cdecl"):
    guac_protocol_send_distort = _libs["libguacd"].get("guac_protocol_send_distort", "cdecl")
    guac_protocol_send_distort.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_double, c_double, c_double, c_double, c_double, c_double]
    guac_protocol_send_distort.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1040
if _libs["libguacd"].has("guac_protocol_send_move", "cdecl"):
    guac_protocol_send_move = _libs["libguacd"].get("guac_protocol_send_move", "cdecl")
    guac_protocol_send_move.argtypes = [POINTER(guac_socket), POINTER(guac_layer), POINTER(guac_layer), c_int, c_int, c_int]
    guac_protocol_send_move.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1054
if _libs["libguacd"].has("guac_protocol_send_shade", "cdecl"):
    guac_protocol_send_shade = _libs["libguacd"].get("guac_protocol_send_shade", "cdecl")
    guac_protocol_send_shade.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int]
    guac_protocol_send_shade.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1069
if _libs["libguacd"].has("guac_protocol_send_size", "cdecl"):
    guac_protocol_send_size = _libs["libguacd"].get("guac_protocol_send_size", "cdecl")
    guac_protocol_send_size.argtypes = [POINTER(guac_socket), POINTER(guac_layer), c_int, c_int]
    guac_protocol_send_size.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1096
if _libs["libguacd"].has("guac_protocol_send_argv", "cdecl"):
    guac_protocol_send_argv = _libs["libguacd"].get("guac_protocol_send_argv", "cdecl")
    guac_protocol_send_argv.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String, String]
    guac_protocol_send_argv.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1110
if _libs["libguacd"].has("guac_protocol_send_clipboard", "cdecl"):
    guac_protocol_send_clipboard = _libs["libguacd"].get("guac_protocol_send_clipboard", "cdecl")
    guac_protocol_send_clipboard.argtypes = [POINTER(guac_socket), POINTER(guac_stream), String]
    guac_protocol_send_clipboard.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1120
if _libs["libguacd"].has("guac_protocol_send_name", "cdecl"):
    guac_protocol_send_name = _libs["libguacd"].get("guac_protocol_send_name", "cdecl")
    guac_protocol_send_name.argtypes = [POINTER(guac_socket), String]
    guac_protocol_send_name.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1129
if _libs["libguacd"].has("guac_protocol_decode_base64", "cdecl"):
    guac_protocol_decode_base64 = _libs["libguacd"].get("guac_protocol_decode_base64", "cdecl")
    guac_protocol_decode_base64.argtypes = [String]
    guac_protocol_decode_base64.restype = c_int

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1143
if _libs["libguacd"].has("guac_protocol_string_to_version", "cdecl"):
    guac_protocol_string_to_version = _libs["libguacd"].get("guac_protocol_string_to_version", "cdecl")
    guac_protocol_string_to_version.argtypes = [String]
    guac_protocol_string_to_version.restype = guac_protocol_version

# /tmp/guacamole-server/src/libguac/guacamole/protocol.h: 1156
if _libs["libguacd"].has("guac_protocol_version_to_string", "cdecl"):
    guac_protocol_version_to_string = _libs["libguacd"].get("guac_protocol_version_to_string", "cdecl")
    guac_protocol_version_to_string.argtypes = [guac_protocol_version]
    guac_protocol_version_to_string.restype = c_char_p

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 15
try:
    GUACD_DEFAULT_BIND_HOST = 'localhost'
except:
    pass

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 21
try:
    GUACD_DEFAULT_BIND_PORT = '4822'
except:
    pass

# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 93
try:
    GUACD_LOG_NAME = 'guacd'
except:
    pass

guacd_config = struct_guacd_config# /tmp/guacamole-server/src/guacd/ctypes_wrapper.h: 70

guac_socket = struct_guac_socket# /tmp/guacamole-server/src/libguac/guacamole/socket.h: 39

# No inserted files

# No prefix-stripping

