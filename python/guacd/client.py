from ctypes import POINTER

from . import ctypes_wrapper
from .ctypes_wrapper import (
    String, guac_client_alloc, guac_client_free, guac_client_load_plugin, guac_client_log_handler, guac_client_stop,
    guac_socket, guac_socket_require_keep_alive, guac_user_alloc, guac_user_free, guac_user_handle_connection
)
from .constants import GuacClientLogLevel, GuacStatus, GUACD_USEC_TIMEOUT
from .log import guacd_client_log, guacd_log, guacd_log_guac_error


def cleanup_client(client):
    # Request client to stop/disconnect
    guac_client_stop(client)

    # Attempt to free client cleanly
    guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, 'Requesting termination of client...')

    # Attempt to free client (this may never return if the client is malfunctioning)
    guac_client_free(client)
    guacd_log(GuacClientLogLevel.GUAC_LOG_DEBUG, 'Client terminated successfully.')

    # TODO: Forcibly terminate if timeout occurs during client free
    # result = guacd_timed_client_free(client, GUACD_CLIENT_FREE_TIMEOUT);
    # If client was unable to be freed, warn and forcibly kill
    # if (result) {
    # guacd_log(GUAC_LOG_WARNING, "Client did not terminate in a timely "
    # "manner. Forcibly terminating client and any child "
    # "processes.");
    # guacd_kill_current_proc_group();
    # }


def guacd_create_client(socket: POINTER(guac_socket), protocol: bytes):
    # Similar to guacd_create_proc(protocol) but without creating process
    # Open UNIX socket pair
    # try:
    #     parent_socket, child_socket = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
    # except Exception as e:
    #     guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Error opening socket pair: {e}')
    #     return  None

    # Associate new client
    client_ptr = guac_client_alloc()
    client = client_ptr.contents

    # Init logging
    client.log_handler = guac_client_log_handler(guacd_client_log)

    # Init client for selected protocol
    if guac_client_load_plugin(client_ptr, String(protocol)):
        # Log error
        guac_error = ctypes_wrapper.__guac_error()[0]
        if guac_error == GuacStatus.GUAC_STATUS_NOT_FOUND:
            guacd_log(
                GuacClientLogLevel.GUAC_LOG_WARNING, f'Support for protocol "{protocol.decode()}" is not installed'
            )
        else:
            guacd_log_guac_error(GuacClientLogLevel.GUAC_LOG_ERROR, 'Unable to load client plugin')

        cleanup_client(client_ptr)

    # The first file descriptor is the owner
    owner = 1

    # Enable keep alive on the broadcast socket
    guac_socket_require_keep_alive(client.socket)

    # Add each received file descriptor as a new user
    # while received_fd := guacd_recv_fd(fd_socket) != -1:
    #     guacd_proc_add_user(proc, received_fd, owner)

    #     # Future file descriptors are not owners
    #     owner = 0

    # Create skeleton user (guacd_user_thread())
    user_ptr = guac_user_alloc()
    user = user_ptr.contents
    user.socket = socket
    user.client = client_ptr
    user.owner  = 1

    # Handle user connection from handshake until disconnect/completion
    guac_user_handle_connection(user_ptr, GUACD_USEC_TIMEOUT)

    # Stop client and prevent future users if all users are disconnected
    if client.connected_users == 0:
        guacd_log(
            GuacClientLogLevel.GUAC_LOG_INFO, f'Last user of connection "{client.connection_id}" disconnected'
        )

    # Clean up
    guac_user_free(user_ptr)
    cleanup_client(client_ptr)
