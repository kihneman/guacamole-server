from ctypes import cast, c_char_p, c_int, c_void_p, POINTER
from typing import Optional

from . import ctypes_wrapper
from .ctypes_wrapper import String, guac_client_log_level, guac_user, guac_user_log as libguac_user_log
from .constants import GuacClientLogLevel, GuacStatus, guac_status_to_string


def guacd_client_log(guac_client_ptr, log_level: c_int, msg: String, log_args: c_void_p):
    """Compatible with ctypes_wrapper.guac_client_log_handler
    """
    guacd_log(GuacClientLogLevel(log_level.value), msg.data.decode())


def guacd_log(log_level: GuacClientLogLevel, msg: str):
    ctypes_wrapper.guacd_log(
        guac_client_log_level(log_level),
        String(msg.encode())
    )


def guac_user_log(user: POINTER(guac_user), level: GuacClientLogLevel, message: str):
    guacd_log(level, message)


def guacd_log_guac_error(level: GuacClientLogLevel, message: str):
    guac_error = ctypes_wrapper.__guac_error()[0]
    guac_error_message = cast(ctypes_wrapper.__guac_error_message()[0], c_char_p).value
    if guac_error != GuacStatus.GUAC_STATUS_SUCCESS:
        # If error message provided, include in log
        if guac_error_message:
            guacd_log(level, f'{message}: {guac_error_message.decode()}')

        # Otherwise just log with standard status string
        else:
            status_string = guac_status_to_string.get(guac_error, guac_status_to_string[None])
            guacd_log(level, f'{message}: {status_string}')

    # Just log message if no status code
    else:
        guacd_log(level, message)


def guacd_log_handshake_failure():
    guac_error = ctypes_wrapper.__guac_error()[0]
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
