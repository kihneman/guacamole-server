from ctypes import cast, c_char_p, c_int

import zmq

from . import libguac_wrapper
from .constants import GuacClientLogLevel, GuacStatus, GUAC_CLIENT_ID_PREFIX, GUACD_USEC_TIMEOUT
from .libguac_wrapper import (
    String, guac_parser_alloc, guac_parser_expect, guac_parser_free, guac_socket_create_zmq, guac_socket_free
)
from .log import guacd_log, guacd_log_guac_error, guacd_log_handshake_failure
from .proc import guacd_create_proc


def parse_identifier(zmq_addr: str):

    parser_ptr = guac_parser_alloc()
    parser = parser_ptr.contents

    # Reset guac_error
    libguac_wrapper.__guac_error()[0] = c_int(GuacStatus.GUAC_STATUS_SUCCESS)
    libguac_wrapper.__guac_error_message()[0] = String(b'').raw

    # Get protocol from select instruction
    guac_sock = guac_socket_create_zmq(zmq.PAIR, zmq_addr, False)
    parser_result = guac_parser_expect(parser_ptr, guac_sock, c_int(GUACD_USEC_TIMEOUT), String(b'select'))
    guac_socket_free(guac_sock)

    if parser_result:
        # Log error
        guacd_log_handshake_failure()
        guacd_log_guac_error(GuacClientLogLevel.GUAC_LOG_ERROR, f'Error reading "select" ({parser_result})')
        return None

    # Validate args to select
    if parser.argc != 1:
        # Log error
        guacd_log_handshake_failure()
        guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Bad number of arguments to "select" ({parser.argc})')
        return None

    identifier = bytes(cast(parser.argv[0], c_char_p).value).decode()
    guac_parser_free(parser_ptr)
    return identifier


def guacd_route_connection(proc_map: dict, zmq_addr: str) -> int:
    """Route a Guacamole connection

    Routes the connection on the given socket according to the Guacamole
    protocol, adding new users and creating new client processes as needed. If a
    new process is created, this function blocks until that process terminates,
    automatically deregistering the process at that point.

    The socket provided will be automatically freed when the connection
    terminates unless routing fails, in which case non-zero is returned.

    @param proc_map
        The map of existing client processes.

    @param zmq_addr
        ZeroMQ address for use in creating a new guac_socket to the new connection that will be routed

    @return
        Zero if the connection was successfully routed, non-zero if routing has
        failed.
    """

    identifier = parse_identifier(zmq_addr)

    if identifier is None:
        guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Invalid connection identifier from parsing "select"')
        return 1

    # If connection ID, retrieve existing process
    if identifier[0] == GUAC_CLIENT_ID_PREFIX:
        proc = proc_map.get(identifier)

        if proc is None:
            guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, f'Connection "{identifier}" does not exist')
            return 1
        else:
            guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, f'Found existing connection "{identifier}"')

    # Otherwise, create new client
    else:
        guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, f'Creating new client for protocol "{identifier}"')

        # Create new process
        proc = guacd_create_proc(identifier)
        if proc is None:
            return 1

        # Add to proc_map
        client_ptr = proc.client_ptr
        client = client_ptr.contents
        proc_map[str(client.connection_id)] = proc

    proc.connect()
    guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, f'Connected to "{proc.zmq_socket_addr}"')
    proc.send_user_socket_addr(zmq_addr)
    proc.zmq_socket.close()

    return 0
