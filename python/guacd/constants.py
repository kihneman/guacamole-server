from enum import IntEnum


GUACD_LOG_NAME = 'guacd'


class GuacClientLogLevel(IntEnum):
    # Fatal errors.
    GUAC_LOG_ERROR = 3

    # Non-fatal conditions that indicate problems.
    GUAC_LOG_WARNING = 4

    # Informational messages of general interest to users or administrators.
    GUAC_LOG_INFO = 6

    # Informational messages which can be useful for debugging, but are
    # otherwise not useful to users or administrators. It is expected that
    # debug level messages, while verbose, will not negatively affect
    # performance.
    GUAC_LOG_DEBUG = 7

    # Informational messages which can be useful for debugging, like
    # GUAC_LOG_DEBUG, but which are so low-level that they may affect
    # performance.
    GUAC_LOG_TRACE = 8
