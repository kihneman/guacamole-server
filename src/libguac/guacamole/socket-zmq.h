//
// Created by KevinKihneman on 1/3/2024.
//

#ifndef GUAC_SOCKET_ZMQ_H
#define GUAC_SOCKET_ZMQ_H

/**
 * Provides an implementation of guac_socket specific to the CZMQ C binding for ZeroMQ.
 * This header will only be available if libguac was built with ZeroMQ support.
 *
 * @file socket-zmq.h
 */

#include "socket-types.h"

#include <czmq.h>

/**
 * Opens a new guac_socket which will use the CZMQ C binding of ZeroMQ
 * for all communication. Freeing this guac_socket will
 * automatically close the associated ZeroMQ socket handle.
 *
 * @param zsock
 *     The ZeroMQ socket of type zsock_t to use for the connection underlying the created
 *     guac_socket.
 *
 * @return
 *     A newly-allocated guac_socket which will transparently use the CZMQ C binding of ZeroMQ
 *     for all communication.
 */
guac_socket* guac_socket_open_zmq(zsock_t zsock);

/**
 * Creates a new guac_socket which will use the CZMQ C binding of ZeroMQ
 * for all communication. Freeing this guac_socket will
 * automatically close the associated ZeroMQ socket handle.
 *
 * @param type
 *     The ZeroMQ socket type integer based on the socket type as follows:
 *         ZMQ_PAIR 0
 *         ZMQ_PUB 1
 *         ZMQ_SUB 2
 *         ZMQ_REQ 3
 *         ZMQ_REP 4
 *         ZMQ_DEALER 5
 *         ZMQ_ROUTER 6
 *         ZMQ_PULL 7
 *         ZMQ_PUSH 8
 *         ZMQ_XPUB 9
 *         ZMQ_XSUB 10
 *         ZMQ_STREAM 11
 *
 * @param endpoints
 *     The endpoints pointer is NULL, or points to string starting with
 *     '@' (bind) or '>' (connect). Multiple endpoints are allowed, separated by
 *     commas. If the endpoint does not start with '@' or '>', the serverish argument defines
 *     whether it is used to bind (serverish = true) or connect (serverish = false).
 *
 * @param serverish
 *     The serverish argument defines whether it is used to bind (serverish = true) or connect (serverish = false).
 *
 * @return
 *     A newly-allocated guac_socket which will transparently use the CZMQ C binding of ZeroMQ
 *     for all communication.
 */
guac_socket* guac_socket_create_zmq(int type, const char *endpoints, bool serverish);

#endif
