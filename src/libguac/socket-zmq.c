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

#include "guacamole/error.h"
#include "guacamole/socket.h"

#include <arpa/inet.h>
#include <errno.h>
#include <pthread.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <czmq.h>

/**
 * Data associated with an open socket which uses CZMQ C binding for ZeroMQ.
 */
typedef struct guac_socket_zmq_data {

    /**
     * The associated ZeroMQ CZMQ socket.
     */
    zsock_t *zsock;

    /**
     * The associated ZeroMQ socket handle.
     */
    void *zmq_handle;

    /**
     * ZeroMQ message (Kept between read_handler calls if not completely consumed)
     */
    zmq_msg_t zmq_msg;

    /**
    * Current position in ZeroMQ message data
    * Pointer is NULL unless ZeroMQ message exists
    */
    char *zmq_data_ptr;

    /**
    * Remaining size of ZeroMQ message data
    * This value is 0 unless ZeroMQ message exists
    */
    size_t zmq_data_size;

    /**
     * The number of bytes currently in the main write buffer.
     */
    int written;

    /**
     * The main write buffer. Bytes written go here before being flushed
     * to the open socket.
     */
    char out_buf[GUAC_SOCKET_OUTPUT_BUFFER_SIZE];

    /**
     * Lock which is acquired when an instruction is being written, and
     * released when the instruction is finished being written.
     */
    pthread_mutex_t socket_lock;

    /**
     * Lock which protects access to the internal buffer of this socket,
     * guaranteeing atomicity of writes and flushes.
     */
    pthread_mutex_t buffer_lock;

} guac_socket_zmq_data;

/**
 * Writes the entire contents of the given buffer to the ZeroMQ handle
 * associated with the given socket, retrying as necessary until the whole
 * buffer is written, and aborting if an error occurs.
 *
 * @param socket
 *     The guac_socket associated with the ZeroMQ socket to which the given
 *     buffer should be written.
 *
 * @param buf
 *     The buffer of data to write to the given guac_socket.
 *
 * @param count
 *     The number of bytes within the given buffer.
 *
 * @return
 *     The number of bytes written, which will be exactly the size of the given
 *     buffer, or a negative value if an error occurs.
 */
ssize_t guac_socket_zmq_write(guac_socket* socket,
        const void* buf, size_t count) {

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;
    const char* buffer = buf;

    /* Write until completely written */
    while (count > 0) {

        /* Send timestamp */
        struct timespec current;
        clock_gettime(CLOCK_MONOTONIC, &current);
        uint32_t tv_sec = htonl((uint32_t) current.tv_sec);
        uint32_t tv_nsec = htonl((uint32_t) current.tv_nsec);

        int retval = zmq_send(data->zmq_handle, (char*) &tv_sec, sizeof(uint32_t), ZMQ_SNDMORE);
        if (retval >= 0)
            retval = zmq_send(data->zmq_handle, (char*) &tv_nsec, sizeof(uint32_t), ZMQ_SNDMORE);

        /* Send data buffer */
        if (retval >= 0)
            retval = zmq_send(data->zmq_handle, buffer, count, 0);

        /* Record errors in guac_error */
        if (retval < 0) {
            guac_error = GUAC_STATUS_SEE_ERRNO;
            guac_error_message = "Error writing data to socket";
            return retval;
        }

        /* Advance buffer as data retval */
        buffer += retval;
        count  -= retval;

    }

    return 0;

}

/**
 * Attempts to read from the underlying ZeroMQ handle of the given guac_socket,
 * populating the given buffer.
 *
 * @param socket
 *     The guac_socket being read from.
 *
 * @param buf
 *     The arbitrary buffer which we must populate with data.
 *
 * @param count
 *     The maximum number of bytes to read into the buffer.
 *
 * @return
 *     The number of bytes read, or -1 if an error occurs.
 */
static ssize_t guac_socket_zmq_read_handler(guac_socket* socket,
        void* buf, size_t count) {

    if (count == 0)
        return 0;

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Reading socket isn't necessary if remaining ZeroMQ message data is at least size "count" */
    if (data->zmq_data_size >= count) {
        memcpy(buf, data->zmq_data_ptr, count);

        /* Either close ZeroMQ message if consumed or update pointer to ZeroMQ message data */
        if (data->zmq_data_size == count) {
            zmq_msg_close(&(data->zmq_msg));
            data->zmq_data_ptr = NULL;
            data->zmq_data_size = 0;
        }
        else {
            data->zmq_data_ptr += count;
            data->zmq_data_size -= count;
        }

        fprintf(stderr, "Returning size %i data", (int) count);
        return count;
    }

    /* zmq_recvmsg() flags are 0 by default which waits for data to read (blocking mode) */
    int zmq_recvmsg_flags = 0;

    /* First copy any old ZeroMQ message data to return buffer and remember size */
    size_t old_msg_size = 0;
    if (data->zmq_data_ptr) {
        old_msg_size = data->zmq_data_size;
        memcpy(buf, data->zmq_data_ptr, old_msg_size);

        /* Update input and return parameters */
        buf = (char*) buf + old_msg_size;
        count -= old_msg_size;

        /* Close old ZeroMQ message */
        zmq_msg_close(&(data->zmq_msg));
        data->zmq_data_ptr = NULL;
        data->zmq_data_size = 0;

        /* Set flags to read from socket without waiting (non-blocking mode) since data is already available */
        zmq_recvmsg_flags = ZMQ_DONTWAIT;
    }

    /* Get timestamp before read */
    struct timespec current;
    clock_gettime(CLOCK_MONOTONIC, &current);
    uint32_t tv_before_sec = htonl((uint32_t) current.tv_sec);
    uint32_t tv_before_nsec = htonl((uint32_t) current.tv_nsec);

    /* Read from socket and return error if unsuccessful */
    zmq_msg_init(&(data->zmq_msg));
    if (zmq_recvmsg(data->zmq_handle, &(data->zmq_msg), zmq_recvmsg_flags) < 0) {
        if (errno == EAGAIN) {
            /* There is no socket data to read in non-blocking mode, so just return with what has already been copied */
            return old_msg_size;
        }
        guac_error = GUAC_STATUS_SEE_ERRNO;
        guac_error_message = "Error reading data from socket";
        return -1;
    }
    size_t new_msg_size = zmq_msg_size(&(data->zmq_msg));

    /* Send timestamp for debugging read latency */
    clock_gettime(CLOCK_MONOTONIC, &current);
    uint32_t tv_after_sec = htonl((uint32_t) current.tv_sec);
    uint32_t tv_after_nsec = htonl((uint32_t) current.tv_nsec);
    uint32_t new_msg_send_size = htonl((uint32_t) new_msg_size);

    int retval = zmq_send(data->zmq_handle, (char*) &tv_before_sec, sizeof(uint32_t), ZMQ_SNDMORE);
    if (retval >= 0)
        retval = zmq_send(data->zmq_handle, (char*) &tv_before_nsec, sizeof(uint32_t), ZMQ_SNDMORE);
    if (retval >= 0)
        retval = zmq_send(data->zmq_handle, (char*) &tv_after_sec, sizeof(uint32_t), ZMQ_SNDMORE);
    if (retval >= 0)
        retval = zmq_send(data->zmq_handle, (char*) &tv_after_nsec, sizeof(uint32_t), ZMQ_SNDMORE);
    if (retval >= 0)
        retval = zmq_send(data->zmq_handle, "ZMQ_DEBUG_LIBGUAC_READ_LATENCY", 30, ZMQ_SNDMORE);
    if (retval >= 0)
        retval = zmq_send(data->zmq_handle, (char*) &new_msg_send_size, sizeof(uint32_t), 0);

    /* Record errors in guac_error */
    if (retval < 0) {
        guac_error = GUAC_STATUS_SEE_ERRNO;
        guac_error_message = "Error writing data to socket";
        return retval;
    }

    /* Just copy socket message data if it doesn't exceed size "count" */
    if (new_msg_size <= count) {
        memcpy(buf, zmq_msg_data(&(data->zmq_msg)), new_msg_size);
        zmq_msg_close(&(data->zmq_msg));
        return old_msg_size + new_msg_size;
    }

    /* Otherwise copy only size "count" to return buffer and keep pointer to ZeroMQ message in data->zmq_msg */
    else {
        /* Set pointer to match new message and copy */
        data->zmq_data_ptr = (char*) zmq_msg_data(&(data->zmq_msg));
        memcpy(buf, data->zmq_data_ptr, count);

        /* Update ZeroMQ message data pointer and size for future reads */
        data->zmq_data_ptr += count;
        data->zmq_data_size = new_msg_size - count;

        return old_msg_size + count;
    }
}

/**
 * Flushes the contents of the output buffer of the given socket immediately,
 * without first locking access to the output buffer. This function must ONLY
 * be called if the buffer lock has already been acquired.
 *
 * @param socket
 *     The guac_socket to flush.
 *
 * @return
 *     Zero if the flush operation was successful, non-zero otherwise.
 */
static ssize_t guac_socket_zmq_flush(guac_socket* socket) {

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Flush remaining bytes in buffer */
    if (data->written > 0) {

        /* Write ALL bytes in buffer immediately */
        if (guac_socket_zmq_write(socket, data->out_buf, data->written))
            return 1;

        data->written = 0;
    }

    return 0;

}

/**
 * Flushes the internal buffer of the given guac_socket, writing all data
 * to the underlying ZeroMQ handle.
 *
 * @param socket
 *     The guac_socket to flush.
 *
 * @return
 *     Zero if the flush operation was successful, non-zero otherwise.
 */
static ssize_t guac_socket_zmq_flush_handler(guac_socket* socket) {

    int retval;
    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Acquire exclusive access to buffer */
    pthread_mutex_lock(&(data->buffer_lock));

    /* Flush contents of buffer */
    retval = guac_socket_zmq_flush(socket);

    /* Relinquish exclusive access to buffer */
    pthread_mutex_unlock(&(data->buffer_lock));

    return retval;

}

/**
 * Writes the contents of the buffer to the output buffer of the given socket,
 * flushing the output buffer as necessary, without first locking access to the
 * output buffer. This function must ONLY be called if the buffer lock has
 * already been acquired.
 *
 * @param socket
 *     The guac_socket to write the given buffer to.
 *
 * @param buf
 *     The buffer to write to the given socket.
 *
 * @param count
 *     The number of bytes in the given buffer.
 *
 * @return
 *     The number of bytes written, or a negative value if an error occurs
 *     during write.
 */
static ssize_t guac_socket_zmq_write_buffered(guac_socket* socket,
        const void* buf, size_t count) {

    size_t original_count = count;
    const char* current = buf;
    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Append to buffer, flush if necessary */
    while (count > 0) {

        int chunk_size;
        int remaining = sizeof(data->out_buf) - data->written;

        /* If no space left in buffer, flush and retry */
        if (remaining == 0) {

            /* Abort if error occurs during flush */
            if (guac_socket_zmq_flush(socket))
                return -1;

            /* Retry buffer append */
            continue;

        }

        /* Calculate size of chunk to be written to buffer */
        chunk_size = count;
        if (chunk_size > remaining)
            chunk_size = remaining;

        /* Update output buffer */
        memcpy(data->out_buf + data->written, current, chunk_size);
        data->written += chunk_size;

        /* Update provided buffer */
        current += chunk_size;
        count   -= chunk_size;

    }

    /* All bytes have been written, possibly some to the internal buffer */
    return original_count;

}

/**
 * Appends the provided data to the internal buffer for future writing. The
 * actual write attempt will occur only upon flush, or when the internal buffer
 * is full.
 *
 * @param socket
 *     The guac_socket being write to.
 *
 * @param buf
 *     The arbitrary buffer containing the data to be written.
 *
 * @param count
 *     The number of bytes contained within the buffer.
 *
 * @return
 *     The number of bytes written, or -1 if an error occurs.
 */
static ssize_t guac_socket_zmq_write_handler(guac_socket* socket,
        const void* buf, size_t count) {

    int retval;
    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Acquire exclusive access to buffer */
    pthread_mutex_lock(&(data->buffer_lock));

    /* Write provided data to buffer */
    retval = guac_socket_zmq_write_buffered(socket, buf, count);

    /* Relinquish exclusive access to buffer */
    pthread_mutex_unlock(&(data->buffer_lock));

    return retval;

}

/**
 * Waits for data on the underlying ZeroMQ socket to
 * become available such that the next read operation will not block.
 *
 * @param socket
 *     The guac_socket to wait for.
 *
 * @param usec_timeout
 *     The maximum amount of time to wait for data, in microseconds, or -1 to
 *     potentially wait forever.
 *
 * @return
 *     A positive value on success, zero if the timeout elapsed and no data is
 *     available, or a negative value if an error occurs.
 */
static int guac_socket_zmq_select_handler(guac_socket* socket,
        int usec_timeout) {

    fprintf(stderr, "Polling...");
    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    if (data->zmq_data_ptr) {
        /* There is ZeroMQ message data available from a previous read, so return success */
        return 1;
    }

    /* Initialize poll items with single underlying ZeroMQ socket handle */
    zmq_pollitem_t items [1];
    items[0].socket = data->zmq_handle;
    items[0].events = ZMQ_POLLIN;

    /* Wait for data on socket */
    /* Round timeout up to poll()'s granularity */
    int retval = zmq_poll(items, 1, (usec_timeout < 0) ? -1 : (usec_timeout + 999) / 1000);

    /* Properly set guac_error */
    if (retval <  0) {
        guac_error = GUAC_STATUS_SEE_ERRNO;
        guac_error_message = "Error while waiting for data on socket";
    }

    else if (retval == 0) {
        guac_error = GUAC_STATUS_TIMEOUT;
        guac_error_message = "Timeout while waiting for data on socket";
    }

    return retval;

}

/**
 * Frees all implementation-specific data associated with the given socket, but
 * not the socket object itself.
 *
 * @param socket
 *     The guac_socket whose associated data should be freed.
 *
 * @return
 *     Zero if the data was successfully freed, non-zero otherwise. This
 *     implementation always succeeds, and will always return zero.
 */
static int guac_socket_zmq_free_handler(guac_socket* socket) {

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Destroy locks */
    pthread_mutex_destroy(&(data->socket_lock));
    pthread_mutex_destroy(&(data->buffer_lock));

    /* Destroy socket */
    zsock_destroy(&(data->zsock));

    free(data);
    return 0;

}

/**
 * Acquires exclusive access to the given socket.
 *
 * @param socket
 *     The guac_socket to which exclusive access is required.
 */
static void guac_socket_zmq_lock_handler(guac_socket* socket) {

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Acquire exclusive access to socket */
    pthread_mutex_lock(&(data->socket_lock));

}

/**
 * Relinquishes exclusive access to the given socket.
 *
 * @param socket
 *     The guac_socket to which exclusive access is no longer required.
 */
static void guac_socket_zmq_unlock_handler(guac_socket* socket) {

    guac_socket_zmq_data* data = (guac_socket_zmq_data*) socket->data;

    /* Relinquish exclusive access to socket */
    pthread_mutex_unlock(&(data->socket_lock));

}

guac_socket* guac_socket_open_zmq(zsock_t *zsock) {

    pthread_mutexattr_t lock_attributes;

    /* Allocate socket and associated data */
    guac_socket* socket = guac_socket_alloc();
    guac_socket_zmq_data* data = malloc(sizeof(guac_socket_zmq_data));

    /* Store zsock as socket data */
    data->zsock = zsock;
    data->zmq_handle = zsock_resolve(zsock);
    data->zmq_data_ptr = NULL;
    data->zmq_data_size = 0;
    data->written = 0;
    socket->data = data;

    pthread_mutexattr_init(&lock_attributes);
    pthread_mutexattr_setpshared(&lock_attributes, PTHREAD_PROCESS_SHARED);

    /* Init locks */
    pthread_mutex_init(&(data->socket_lock), &lock_attributes);
    pthread_mutex_init(&(data->buffer_lock), &lock_attributes);

    /* Set read/write handlers */
    socket->read_handler   = guac_socket_zmq_read_handler;
    socket->write_handler  = guac_socket_zmq_write_handler;
    socket->select_handler = guac_socket_zmq_select_handler;
    socket->lock_handler   = guac_socket_zmq_lock_handler;
    socket->unlock_handler = guac_socket_zmq_unlock_handler;
    socket->flush_handler  = guac_socket_zmq_flush_handler;
    socket->free_handler   = guac_socket_zmq_free_handler;

    return socket;

}

/**
 * Creates a new CZMQ zsock and returns a corresponding opened guac_socket.
 * A NULL pointer is returned and guac_error set if unsuccessful in attaching to provided endpoints.
 * The zsock gets destroyed with the guac_socket in guac_socket_zmq_free_handler.
 *
 * @param type
 *     ZeroMQ socket type defined in zmq.h (https://github.com/zeromq/libzmq/blob/master/include/zmq.h#L258).
 *
 * @param endpoints
 *     If endpoints is not null, parses as list of ZeroMQ endpoints, separated by commas,
 *     and prefixed by '@' (to bind the socket) or '>' (to attach the socket). If the endpoint
 *     does not start with '@' or '>', the serverish argument defines whether it is used to
 *     bind (serverish = true) or connect (serverish = false).
 *
 * @param serverish
 *     The serverish argument defines whether it is used to bind (serverish = true) or connect (serverish = false).
 */
guac_socket* guac_socket_create_zmq(int type, const char *endpoints, bool serverish) {

    /* Create new zsock */
    zsock_t *zsock = zsock_new(type);

    /* Attach zsock to endpoints and set guac_error with NULL return value if unsuccessful */
    if (zsock_attach(zsock, endpoints, serverish)) {
        zsock_destroy(&zsock);
        guac_error = GUAC_STATUS_IO_ERROR;
        guac_error_message = "Error attaching socket to endpoint";
        return NULL;
    }

    return guac_socket_open_zmq(zsock);
}
