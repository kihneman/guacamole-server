import ctypes
import os
import sys
from os.path import exists, join


GUACD_DLL = join(os.sep, 'opt', 'guacamole', 'lib', 'libguacd.so')


def main():
    if exists(GUACD_DLL):
        guacd_lib = ctypes.CDLL('/opt/guacamole/lib/libguacd.so')
        guacd_lib.main.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
        guacd_lib.main.restype = ctypes.c_int
        argc = ctypes.c_int(len(sys.argv))
        argv_values = [ctypes.c_char_p(s.encode()) for s in sys.argv]
        argv = (ctypes.c_char_p * len(sys.argv))(*argv_values)
        return guacd_lib.main(argc, argv)
    else:
        print(f'The Guacamole Server library {GUACD_DLL} does not exist.')
        return 'Missing DLL'
