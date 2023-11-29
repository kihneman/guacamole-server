import ctypes
import sys
from typing import Optional

from . import ctypes_wrapper
from .ctypes_wrapper import guac_client_log_level, guacd_config, guacd_conf_load, guacd_conf_parse_args, String
from .constants import GuacClientLogLevel


def guacd_log(log_level: GuacClientLogLevel, msg: str):
    ctypes_wrapper.guacd_log(
        guac_client_log_level(log_level),
        String(msg.encode())
    )


def get_argc_argv() -> (ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)):
    argc = ctypes.c_int(len(sys.argv))
    argv_values = [ctypes.c_char_p(s.encode()) for s in sys.argv]
    argv = (ctypes.c_char_p * len(sys.argv))(*argv_values)
    return argc, argv


def guacd_main():
    argc, argv = get_argc_argv()
    argv_double_ptr = ctypes.cast(argv, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    result: ctypes.c_int = ctypes_wrapper.main(argc, argv_double_ptr)
    return result


def get_config() -> (Optional[int], Optional[guacd_config]):
    config_ptr: ctypes.POINTER(guacd_config) = guacd_conf_load()
    if config_ptr:
        argc, argv = get_argc_argv()
        argv_double_ptr = ctypes.cast(argv, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        result = guacd_conf_parse_args(config_ptr, argc, argv_double_ptr)
        config: guacd_config = config_ptr.contents
        return result, config
    else:
        return None, None
