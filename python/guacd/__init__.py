import ctypes
import sys

import ctypes_wrapper
from ctypes_wrapper import guac_client_log_level, String
from .constants import GuacClientLogLevel


def guacd_log(log_level: GuacClientLogLevel, msg: str):
    ctypes_wrapper.guacd_log(
        guac_client_log_level(log_level),
        String(msg.encode())
    )


def guacd_main():
    argc = ctypes.c_int(len(sys.argv))
    argv_values = [ctypes.c_char_p(s.encode()) for s in sys.argv]
    argv = (ctypes.c_char_p * len(sys.argv))(*argv_values)
    return ctypes_wrapper.main(argc, argv)
