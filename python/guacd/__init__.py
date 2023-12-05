import ctypes
from typing import Optional

from . import ctypes_wrapper
from .ctypes_wrapper import guacd_config, guacd_conf_load, guacd_conf_parse_args
from .constants import GuacClientLogLevel


def get_argc_argv(sys_argv) -> (ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)):
    argc = ctypes.c_int(len(sys_argv))
    argv_values = [ctypes.c_char_p(s.encode()) for s in sys_argv]
    argv = (ctypes.c_char_p * len(sys_argv))(*argv_values)
    return argc, argv


def guacd_main(sys_argv):
    argc, argv = get_argc_argv(sys_argv)
    argv_double_ptr = ctypes.cast(argv, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    result: ctypes.c_int = ctypes_wrapper.main(argc, argv_double_ptr)
    return result


def get_config(sys_argv) -> (Optional[int], Optional[guacd_config]):
    config_ptr: ctypes.POINTER(guacd_config) = guacd_conf_load()
    if config_ptr:
        argc, argv = get_argc_argv(sys_argv)
        argv_double_ptr = ctypes.cast(argv, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        result = guacd_conf_parse_args(config_ptr, argc, argv_double_ptr)
        config: guacd_config = config_ptr.contents
        return result, config
    else:
        return None, None
