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
 * Creates a new guac_socket which will use the CZMQ C binding of ZeroMQ
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

#endif
