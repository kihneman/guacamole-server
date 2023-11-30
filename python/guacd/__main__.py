import socket
import sys
import syslog
from argparse import ArgumentParser
from socket import getaddrinfo, getnameinfo

from . import get_config, guacd_config, guacd_main, guacd_log
from .constants import (
    EXIT_SUCCESS, EXIT_FAILURE,
    GuacClientLogLevel, GUACD_DEFAULT_BIND_HOST, GUACD_DEFAULT_BIND_PORT, GUACD_LOG_NAME
)
from .ctypes_wrapper import guac_socket_open


def main():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('--python', action='store_true')
    # Remove --python from argv to not affect libguacd parser
    ns, argv = parser.parse_known_args(sys.argv)

    if ns.python:
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

        # for current_address in addresses:
        #     socket.getnameinfo(current_address[-1], socket.NI_NUMERICHOST | socket.NI_NUMERICSERV)
        current_address = addresses[-1]  # Default 127.0.0.1
        bound_result = getnameinfo(current_address[-1], socket.NI_NUMERICHOST | socket.NI_NUMERICSERV)
        bound_address, bound_port = bound_result

        with socket.socket(current_address[0], socket.SOCK_STREAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(current_address[-1])
            except Exception as e:
                guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Socket error binding to {bound_result}: {e}')
                exit(EXIT_FAILURE)
            else:
                guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, f'Listening on host {bound_address}, port {bound_port}')

            try:
                s.listen()
            except Exception as e:
                guacd_log(GuacClientLogLevel.GUAC_LOG_ERROR, f'Could not listen on socket: {e}')
                exit(3)

            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                breakpoint()
                guac_socket_ptr = guac_socket_open(s.fileno())
                guac_socket = guac_socket_ptr.contents

    else:
        # parser.add_argument('-v', action='store_true')
        # ns, _ = parser.parse_known_args(argv)
        # if ns.v:
        #     result = guacd_main(argv)
        #     exit(result)

        result = guacd_main(argv)
        msg = f'Finished with result "{result}"'
        guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
