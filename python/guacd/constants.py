from enum import IntEnum


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
GUACD_LOG_NAME = 'guacd'

# The default host that guacd should bind to, if no other host is explicitly specified.
GUACD_DEFAULT_BIND_HOST = 'localhost'

# The default port that guacd should bind to, if no other port is explicitly specified.
GUACD_DEFAULT_BIND_PORT = '4822'

# The number of milliseconds to wait for messages in any phase before
# timing out and closing the connection with an error.
GUACD_TIMEOUT = 15000

# The number of microseconds to wait for messages in any phase before
# timing out and closing the conncetion with an error. This is always
# equal to GUACD_TIMEOUT * 1000.
GUACD_USEC_TIMEOUT = (GUACD_TIMEOUT*1000)


class GuacClientLogLevel(IntEnum):
    """The contents of a guacd configuration file."""
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
