/*
 * Copyright (c) 2024 Keeper Security, Inc. All rights reserved.
 *
 * Unless otherwise agreed in writing, this software and any associated
 * documentation files (the "Software") may be used and distributed solely
 * in accordance with the Keeper Connection Manager EULA:
 *
 *     https://www.keepersecurity.com/termsofuse.html?t=k
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

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
 *     A NULL pointer is returned and guac_error set if unsuccessful in attaching to provided endpoints.
 */
guac_socket* guac_socket_create_zmq(int type, const char *endpoints, bool serverish);

#endif
