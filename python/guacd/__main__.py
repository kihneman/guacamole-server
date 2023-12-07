import os
import socket
import sys
import syslog
from argparse import ArgumentParser
from socket import getaddrinfo, getnameinfo

from . import get_config, guacd_main
from .connection import guacd_route_connection
from .constants import (
    EXIT_SUCCESS, EXIT_FAILURE, GuacClientLogLevel, GUACD_DEFAULT_BIND_HOST, GUACD_DEFAULT_BIND_PORT, GUACD_LOG_NAME
)
from .ctypes_wrapper import (
    String, guac_protocol_send_name, guac_socket_flush, guac_socket_free, guac_socket_open
)
from .log import guacd_log


PROTOCOL = b'ssh'


def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--python', action='store_true')
    parser.add_argument('--test-sock', action='store_true')
    # Remove --python from argv to not affect libguacd parser
    ns, argv = parser.parse_known_args(sys.argv)

    use_python = ns.python or ns.test_sock
    if use_python:
        result, config = get_config(argv)
        if not config:
            exit(EXIT_FAILURE)

        # Init logging as early as possible
        guacd_log_level = config.max_log_level
        syslog.openlog(GUACD_LOG_NAME, logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)

        msg = f'Running with args {argv}, config result "{result}"'
        guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
        if config.print_version:
            guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, 'Version not available yet')
            exit(EXIT_SUCCESS)
        else:
            guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, 'Guacamole proxy daemon (guacd) started')

        try:
            addresses = getaddrinfo(
                GUACD_DEFAULT_BIND_HOST, GUACD_DEFAULT_BIND_PORT,
                family=socket.AF_UNSPEC, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
        except Exception as e:
            guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Error parsing given address or port: {e}')
            exit(EXIT_FAILURE)

        current_address = None
        for current_address in addresses:
            try:
                bound_result = getnameinfo(current_address[-1], socket.NI_NUMERICHOST | socket.NI_NUMERICSERV)
            except Exception as e:
                guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Unable to resolve host: {e}')
                continue
            else:
                bound_address, bound_port = bound_result

            guac_socket = None

            with socket.socket(current_address[0], socket.SOCK_STREAM) as s:
                try:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(current_address[-1])
                except Exception as e:
                    continue
                else:
                    guacd_log(
                        GuacClientLogLevel.GUAC_LOG_INFO,
                        f'Listening with PID "{os.getpid()}" on host "{bound_address}", port {bound_port}'
                    )

                try:
                    s.listen()
                except Exception as e:
                    guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Could not listen on socket: {e}')
                    exit(3)

                conn, addr = s.accept()
                with conn:
                    print(f'Connected by {addr}')
                    if ns.test_sock:
                        guac_socket = guac_socket_open(conn.fileno())
                        guac_protocol_send_name(guac_socket, String(b'simple-socket-test'))
                        guac_socket_flush(guac_socket)

                    else:
                        guac_socket = guac_socket_open(conn.fileno())
                        guacd_route_connection(guac_socket)

            if guac_socket:
                guac_socket_free(guac_socket)
            break
        else:
            address_host_port = [a[-1] for a in addresses]
            guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f"Couldn't bind to addresses: {address_host_port}")

    else:
        # parser.add_argument('-v', action='store_true')
        # ns, _ = parser.parse_known_args(argv)
        # if ns.v:
        #     result = guacd_main(argv)
        #     exit(result)

        result = guacd_main(argv)
        msg = f'Finished with result "{result}"'
        guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)

main()
