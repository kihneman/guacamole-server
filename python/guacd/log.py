from ctypes import c_int
from typing import Optional

from . import ctypes_wrapper
from .ctypes_wrapper import guac_error, guac_error_message, guac_client_log_level, String
from .constants import GuacClientLogLevel, GuacStatus, guac_status_to_string


def guacd_log(log_level: GuacClientLogLevel, msg: str):
    ctypes_wrapper.guacd_log(
        guac_client_log_level(log_level),
        String(msg.encode())
    )


def guacd_log_client(guac_client_ptr, log_level_cint: c_int, msg: String, log_args):
    guac_client = guac_client_ptr.contents
    log_level = GuacClientLogLevel(log_level_cint.value)
    ctypes_wrapper.guacd_log(guac_client_log_level(log_level), msg)


def guacd_log_guac_error(level: GuacClientLogLevel, message: str):
    if guac_error != GuacStatus.GUAC_STATUS_SUCCESS:
        # If error message provided, include in log
        if guac_error_message is not None:
            guacd_log(level, f'{message}: {guac_error_message}')

        # Otherwise just log with standard status string
        else:
            status_string = guac_status_to_string.get(guac_error, guac_status_to_string[None])
            guacd_log(level, f'{message}: {status_string}')

    # Just log message if no status code
    else:
        guacd_log(level, message)


def guacd_log_handshake_failure():
    if guac_error == GuacStatus.GUAC_STATUS_CLOSED:
        guacd_log(
            GuacClientLogLevel.GUAC_LOG_DEBUG,
            "Guacamole connection closed during handshake"
        )
    elif guac_error == GuacStatus.GUAC_STATUS_PROTOCOL_ERROR:
        guacd_log(
            GuacClientLogLevel.GUAC_LOG_ERROR,
            "Guacamole protocol violation. Perhaps the version of "
            "guacamole-client is incompatible with this version of "
            "guacd?"
        )
    else:
        status_string = guac_status_to_string.get(guac_error, guac_status_to_string[None])
        guacd_log(
            GuacClientLogLevel.GUAC_LOG_WARNING,
            f"Guacamole handshake failed: {status_string}"
        )
