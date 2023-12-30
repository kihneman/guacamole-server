import array
import socket


MSG = 'G'  # Arbitrary message sent along with file descriptor


# From https://docs.python.org/3/library/socket.html#socket.socket.sendmsg
def send_fds(sock, msg, fds):
    msglen = sock.sendmsg(
        [msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))]
    )
    return msglen


# From https://docs.python.org/3/library/socket.html#socket.socket.recvmsg
def recv_fds(sock, msglen, maxfds):
    fds = array.array("i")   # Array of ints
    msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            # Append data, ignoring any truncated integers at the end.
            fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
    return msg, list(fds)


def guacd_send_fd(sock, fd):
    # Send file descriptor
    return send_fds(sock, MSG, [fd]) == len(MSG)


def guacd_recv_fd(sock):
    # Receive file descriptor
    msg, fds = recv_fds(len(MSG), 1)

    # Validate payload
    if msg == MSG and len(fds) == 1:
        return fds[0]

    else:
        # Failed to receive file descriptor
        return -1
