from ctypes import addressof, cast, c_char_p, c_int, POINTER, Structure
from threading import Thread
from typing import Optional

from . import ctypes_wrapper
from .constants import GuacClientLogLevel, GuacClientState, GuacProtocolVersion, GuacStatus, guac_status_to_string
from .ctypes_wrapper import (
    __guac_handshake_handler_map, __guac_instruction_handler_map, __guac_user_call_opcode_handler,
    guac_client, guac_client_add_user, guac_client_log, guac_client_log_level, guac_client_remove_user,
    guac_free_mimetypes, guac_mem_free_const,
    guac_parser, guac_parser_alloc, guac_parser_free, guac_parser_read,
    guac_protocol_send_args, guac_protocol_send_disconnect, guac_protocol_send_ready, guac_protocol_string_to_version,
    guac_socket, guac_socket_flush, guac_user, guac_user_abort, guac_user_log, guac_user_stop, String
)


# The client took too long to respond.
GUAC_PROTOCOL_STATUS_CLIENT_TIMEOUT = 0x308


# Parameters required by the user input thread.
# noinspection PyPep8Naming
class struct_guac_user_input_thread_params(Structure):
    pass


guac_user_input_thread_params = struct_guac_user_input_thread_params
struct_guac_user_input_thread_params.__slots__ = [
    'parser',
    'user',
    'usec_timeout',
]
struct_guac_user_input_thread_params._fields_ = [
    # The parser which will be used throughout the user's session.
    ('parser', POINTER(guac_parser)),
    # A reference to the connected user.
    ('user', POINTER(guac_user)),
    # The number of microseconds to wait for instructions from a connected
    # user before closing the connection with an error.
    ('usec_timeout', c_int),
]


def guac_user_log_guac_error(user: POINTER(guac_user), level: GuacClientLogLevel, message: str):
    """
    Prints an error message using the logging facilities of the given user,
    automatically including any information present in guac_error.

    @param user
        The guac_user associated with the error that occurred.

    @param level
        The level at which to log this message.

    @param message
        The message to log.
    """
    guac_error = ctypes_wrapper.__guac_error()[0]
    guac_error_message = cast(ctypes_wrapper.__guac_error_message()[0], c_char_p).value

    if guac_error != GuacStatus.GUAC_STATUS_SUCCESS:
        # If error message provided, include in log
        if guac_error_message:
            guac_user_log(user, level, f'{message}: {guac_error_message.decode()}')

        # Otherwise just log with standard status string
        else:
            status_string = guac_status_to_string.get(guac_error, guac_status_to_string[None])
            guac_user_log(user, level, f'{message}: {status_string}')

    # Just log message if no status code
    else:
        guac_user_log(user, level, message)


def guac_user_log_handshake_failure(user: POINTER(guac_user)):
    """
    Logs a reasonable explanatory message regarding handshake failure based on
    the current value of guac_error.

    @param user
        The guac_user associated with the failed Guacamole protocol handshake.
    """
    guac_error = ctypes_wrapper.__guac_error()[0]
    guac_error_message = cast(ctypes_wrapper.__guac_error_message()[0], c_char_p).value

    if guac_error == GuacStatus.GUAC_STATUS_CLOSED:
        guac_user_log(user, GuacClientLogLevel.GUAC_LOG_DEBUG, 'Guacamole connection closed during handshake')

    elif guac_error == GuacStatus.GUAC_STATUS_PROTOCOL_ERROR:
        guac_user_log(
            user, GuacClientLogLevel.GUAC_LOG_ERROR,
            'Guacamole protocol violation. Perhaps the version of '
            'guacamole-client is incompatible with this version of libguac?'
        )

    else:
        status_string = guac_status_to_string.get(guac_error, guac_status_to_string[None])
        guac_user_log(user, GuacClientLogLevel.GUAC_LOG_WARNING, f'Guacamole handshake failed: {status_string}')


def guac_user_input_thread(data):
    """
    The thread which handles all user input, calling event handlers for received
        instructions.

    @param data
        A pointer to a guac_user_input_thread_params structure describing the
        user whose input is being handled and the guac_parser with which to
        handle it.

    @return
        Always NULL.
    """

    params = data
    usec_timeout = params.usec_timeout
    user_ptr = params.user
    user = user_ptr.contents
    parser_ptr = params.parser
    parser = parser_ptr.contents
    client_ptr = user.client
    client = client_ptr.contents
    socket_ptr = user.socket

    # Guacamole user input loop
    while client.state == GuacClientState.GUAC_CLIENT_RUNNING and user.active:
        # Read instruction, stop on error
        if guac_parser_read(parser_ptr, socket_ptr, usec_timeout):
            guac_error = ctypes_wrapper.__guac_error()[0]
            guac_error_message = cast(ctypes_wrapper.__guac_error_message()[0], c_char_p).value

            if guac_error == GuacStatus.GUAC_STATUS_TIMEOUT:
                guac_user_abort(user_ptr, GUAC_PROTOCOL_STATUS_CLIENT_TIMEOUT, "User is not responding.");

            elif guac_error != GuacStatus.GUAC_STATUS_CLOSED:
                guac_user_log_guac_error(
                    user_ptr, GuacClientLogLevel.GUAC_LOG_WARNING, 'Guacamole connection failure'
                )
                guac_user_stop(user_ptr)

            return None

        # Reset guac_error and guac_error_message (user/client handlers are not
        # guaranteed to set these)
        ctypes_wrapper.__guac_error()[0] = c_int(GuacStatus.GUAC_STATUS_SUCCESS)
        ctypes_wrapper.__guac_error_message()[0] = String(b'').raw

        # Call handler, stop on error
        if __guac_user_call_opcode_handler(
                __guac_instruction_handler_map, user_ptr, parser.opcode, parser.argc, parser.argv
        ):
            # Log error
            guac_user_log_guac_error(user_ptr, GuacClientLogLevel.GUAC_LOG_WARNING, 'User connection aborted')

            # Log handler details
            guac_user_log(
                user_ptr, GuacClientLogLevel.GUAC_LOG_DEBUG,
                f'Failing instruction handler in user was "{parser.opcode.data.decode()}"'
            )

            guac_user_stop(user_ptr)
            return None

    return None


def guac_user_start(parser_ptr: POINTER(guac_parser), user_ptr: POINTER(guac_user), usec_timeout):
    """
    Starts the input/output threads of a new user. This function will block
    until the user disconnects. If an error prevents the input/output threads
    from starting, guac_user_stop() will be invoked on the given user.

    @param parser_ptr
        The guac_parser to use to handle all input from the given user.

    @param user_ptr
        The user whose associated I/O transfer threads should be started.

    @param usec_timeout
        The number of microseconds to wait for instructions from the given
        user before closing the connection with an error.

    @return
        Zero if the I/O threads started successfully and user has disconnected,
        or non-zero if the I/O threads could not be started.
    """

    params = guac_user_input_thread_params(parser=parser_ptr, user=user_ptr, usec_timeout=usec_timeout)

    input_thread = Thread(target=guac_user_input_thread, args=[params])

    try:
        input_thread.start()
    except Exception as e:
        guac_user_log(user_ptr, GuacClientLogLevel.GUAC_LOG_ERROR, f'Unable to start input thread: {e}')
        guac_user_stop(user_ptr)
        return -1

    # Wait for I/O threads
    input_thread.join()

    # Explicitly signal disconnect
    user = user_ptr.contents
    guac_protocol_send_disconnect(user.socket)
    guac_socket_flush(user.socket)

    # Done
    return 0


def __guac_user_handshake(user_ptr: POINTER(guac_user), parser_ptr: POINTER(guac_parser), usec_timeout) -> int:
    """
    This function loops through the received instructions during the handshake
                                                                     * with the client attempting to join the connection, and runs the handlers
    for each of the opcodes, ending when the connect instruction is received.
    Returns zero if the handshake completes successfully with the connect opcode,
    or a non-zero value if an error occurs.

    @param user_ptr
        The guac_user attempting to join the connection.

    @param parser_ptr
        The parser used to examine the received data.

    @param usec_timeout
        The timeout, in microseconds, for reading the instructions.

    @return
        Zero if the handshake completes successfully with the connect opcode,
        or non-zero if an error occurs.

    """
    user = user_ptr.contents
    parser = parser_ptr.contents
    socket_ptr = user.socket

    # Handle each of the opcodes.
    while guac_parser_read(parser_ptr, socket_ptr, usec_timeout) == 0:
        # If we receive the connect opcode, we're done.
        if parser.opcode.data == b'connect':
            return 0

        # Extra debug info
        # user_addr = hex(addressof(user))
        # client = user.client.contents
        # client_addr = hex(addressof(client))
        # log_handler_addr = hex(addressof(client.log_handler.contents))
        # print(f'Addresses: user ({user_addr}), client ({client_addr}), log_handler ({log_handler_addr})')
        guac_user_log(
            user_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_DEBUG),
            String(f'Processing instruction: {parser.opcode.data.decode()}'.encode())
        )

        # Run instruction handler for opcode with arguments.
        if (__guac_user_call_opcode_handler(
                __guac_handshake_handler_map, user_ptr, parser.opcode, parser.argc, parser.argv
        )):
            guac_user_log_handshake_failure(user_ptr)
            guac_user_log_guac_error(
                user_ptr, GuacClientLogLevel.GUAC_LOG_DEBUG, 'Error handling instruction during handshake.'
            )
            guac_user_log(
                user_ptr, GuacClientLogLevel.GUAC_LOG_DEBUG, f'Failed opcode: {parser.opcode.data.decode()}'
            )

            guac_parser_free(parser_ptr)
            return 1

    # If we get here it's because we never got the connect instruction.
    guac_user_log(
        user_ptr, GuacClientLogLevel.GUAC_LOG_ERROR, 'Handshake failed, "connect" instruction was not received.'
    )
    return 1


def guac_user_handle_connection(user_ptr: POINTER(guac_user), usec_timeout: int) -> int:
    user: guac_user = user_ptr.contents
    socket_ptr = user.socket
    client_ptr = user.client
    client: guac_client = client_ptr.contents

    user.info.audio_mimetypes = None
    user.info.image_mimetypes = None
    user.info.video_mimetypes = None
    user.info.name = String()
    user.info.timezone = String()

    # Count number of arguments.
    max_args = 10
    num_args: Optional[int] = None
    for num_args, ptr in enumerate(client.args[i] for i in range(max_args + 1)):
        if not ptr:
            break

    # Send args
    if guac_protocol_send_args(socket_ptr, client.args) or guac_socket_flush(socket_ptr):
        # Log error
        guac_user_log_handshake_failure(user_ptr)
        guac_user_log_guac_error(
            user_ptr, GuacClientLogLevel.GUAC_LOG_DEBUG, 'Error sending "args" to new user'
        )

        return 1

    parser_ptr = guac_parser_alloc()
    parser = parser_ptr.contents

    # Perform the handshake with the client.
    if __guac_user_handshake(user_ptr, parser_ptr, usec_timeout):
        guac_parser_free(parser_ptr)
        return 1

    # Acknowledge connection availability
    guac_protocol_send_ready(socket_ptr, client.connection_id)
    guac_socket_flush(socket_ptr)

    # Verify argument count.
    if parser.argc != num_args + 1:
        guac_client_log(
            client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_ERROR),
            String.from_param('Client did not return the expected number of arguments.')
        )
        return 1

    # Attempt to join user to connection.
    if guac_client_add_user(client_ptr, user_ptr, parser.argc - 1, parser.argv + 1):
        guac_client_log(
            client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_ERROR),
            String.from_param(f'User "{user.user_id}" could NOT join connection "{client.connection_id}"')
        )

    # Begin user connection if join successful
    else:
        guac_client_log(
            client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_INFO),
            f'User "{user.user_id}" joined connection "{client.connection_id}" ({client.connected_users}'
            ' users now present)'
        )

        argv0 = cast(parser.argv[0], c_char_p).value
        if argv0 != b'':
            guac_client_log(
                client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_DEBUG),
                f'Client is using protocol version "{argv0.decode()}"'
            )
            user.info.protocol_version = guac_protocol_string_to_version(String(argv0))
        else:
            guac_client_log(
                client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_DEBUG),
                'Client has not defined its protocol version.'
            )
            user.info.protocol_version = GuacProtocolVersion.GUAC_PROTOCOL_VERSION_1_0_0

        # Handle user I/O, wait for connection to terminate
        guac_user_start(parser_ptr, user_ptr, usec_timeout)

        # Remove/free user
        guac_client_remove_user(client_ptr, user_ptr)
        guac_client_log(
            client_ptr, guac_client_log_level(GuacClientLogLevel.GUAC_LOG_INFO),
            f'User "{user.user_id}" disconnected ({client.connected_users} users remain)'
        )

    # Free mimetype character arrays.
    guac_free_mimetypes(user.info.audio_mimetypes)
    guac_free_mimetypes(user.info.image_mimetypes)
    guac_free_mimetypes(user.info.video_mimetypes)

    # Free name and timezone info.
    guac_mem_free_const(user.info.name)
    guac_mem_free_const(user.info.timezone)

    guac_parser_free(parser)

    # Successful disconnect
    return 0
