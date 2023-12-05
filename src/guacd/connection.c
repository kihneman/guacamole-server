/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include "config.h"

#include "connection.h"
#include "log.h"
#include "proc.h"
#include "proc-map.h"

#include <guacamole/client.h>
#include <guacamole/error.h>
#include <guacamole/id.h>
#include <guacamole/parser.h>
#include <guacamole/plugin.h>
#include <guacamole/protocol.h>
#include <guacamole/socket.h>
#include <guacamole/user.h>

#ifdef ENABLE_SSL
#include <openssl/ssl.h>
#include <guacamole/socket-ssl.h>
#endif

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

#ifdef CYGWIN_BUILD

#include <io.h>
#include <sddl.h>
#include <windows.h>

#include <guacamole/handle-helpers.h>
#include <guacamole/socket-handle.h>

#include "move-pipe.h"

#else

#include "move-fd.h"
#include <sys/socket.h>

#endif

#ifdef CYGWIN_BUILD

/**
 * Behaves exactly as write(), but writes as much as possible, returning
 * successfully only if the entire buffer was written. If the write fails for
 * any reason, a negative value is returned.
 *
 * @param handle
 *     The file handle to write to.
 *
 * @param buffer
 *     The buffer containing the data to be written.
 *
 * @param length
 *     The number of bytes in the buffer to write.
 *
 * @return
 *     The number of bytes written, or -1 if an error occurs. As this function
 *     is guaranteed to write ALL bytes, this will always be the number of
 *     bytes specified by length unless an error occurs.
 */
static int __write_all(HANDLE handle, char* buffer, int length) {

    /* Repeatedly write to the handle until all data is written */
    while (length > 0) {
        
        DWORD written;
        if (guac_write_to_handle(handle, buffer, length, &written))
            return -1;

        length -= written;
        buffer += written;

    }

    return length;

}

#else

/**
 * Behaves exactly as write(), but writes as much as possible, returning
 * successfully only if the entire buffer was written. If the write fails for
 * any reason, a negative value is returned.
 *
 * @param fd
 *     The file descriptor to write to.
 *
 * @param buffer
 *     The buffer containing the data to be written.
 *
 * @param length
 *     The number of bytes in the buffer to write.
 *
 * @return
 *     The number of bytes written, or -1 if an error occurs. As this function
 *     is guaranteed to write ALL bytes, this will always be the number of
 *     bytes specified by length unless an error occurs.
 */
static int __write_all(int fd, char* buffer, int length) {

    /* Repeatedly write() until all data is written */
    int remaining_length = length;
    while (remaining_length > 0) {

        int written = write(fd, buffer, remaining_length);
        if (written < 0)
            return -1;

        remaining_length -= written;
        buffer += written;

    }

    return length;

}

#endif

/**
 * Continuously reads from a guac_socket, writing all data read to a file
 * descriptor or handle. Any data already buffered from that guac_socket by a
 * given guac_parser is read first, prior to reading further data from the
 * guac_socket. The provided guac_parser will be freed once its buffers have
 * been emptied, but the guac_socket will not.
 *
 * This thread ultimately terminates when no further data can be read from the
 * guac_socket.
 *
 * @param data
 *     A pointer to a guacd_connection_io_thread_params structure containing
 *     the guac_socket to read from, the file descriptor to write the read data
 *     to, and the guac_parser associated with the guac_socket which may have
 *     unhandled data in its parsing buffers.
 *
 * @return
 *     Always NULL.
 */
static void* guacd_connection_write_thread(void* data) {

    guacd_connection_io_thread_params* params = (guacd_connection_io_thread_params*) data;
    char buffer[8192];

    int length;

    /* Read all buffered data from parser first */
    while ((length = guac_parser_shift(params->parser, buffer, sizeof(buffer))) > 0) {

#ifdef CYGWIN_BUILD
        if (__write_all(params->handle, buffer, length) < 0)
#else
        if (__write_all(params->fd, buffer, length) < 0)
#endif

            break;
    }

    /* Parser is no longer needed */
    guac_parser_free(params->parser);

    /* Transfer data from file descriptor to socket */
    while ((length = guac_socket_read(params->socket, buffer, sizeof(buffer))) > 0) {

#ifdef CYGWIN_BUILD
        if (__write_all(params->handle, buffer, length) < 0)
#else
        if (__write_all(params->fd, buffer, length) < 0)
#endif

            break;
    }

    return NULL;

}

void* guacd_connection_io_thread(void* data) {

    guacd_connection_io_thread_params* params = (guacd_connection_io_thread_params*) data;
    char buffer[8192];

    pthread_t write_thread;
    pthread_create(&write_thread, NULL, guacd_connection_write_thread, params);

#ifdef CYGWIN_BUILD

    /* Transfer data from file handle to socket */
    while (1) {
        
        DWORD bytes_read;
        if (guac_read_from_handle(params->handle, buffer, sizeof(buffer), &bytes_read))
            break;

        if (guac_socket_write(params->socket, buffer, bytes_read))
            break;

        guac_socket_flush(params->socket);

    }

#else

    /* Transfer data from file descriptor to socket */
    int length;
    while ((length = read(params->fd, buffer, sizeof(buffer))) > 0) {
        if (guac_socket_write(params->socket, buffer, length))
            break;
        guac_socket_flush(params->socket);
    }

#endif

    /* Wait for write thread to die */
    pthread_join(write_thread, NULL);

    /* Clean up */
    guac_socket_free(params->socket);

#ifdef CYGWIN_BUILD
    CloseHandle(params->handle);
#else
    close(params->fd);
#endif

    free(params);

    return NULL;

}

/**
 * Adds the given socket as a new user to the given process, automatically
 * reading/writing from the socket via read/write threads. The given socket,
 * parser, and any associated resources will be freed unless the user is not
 * added successfully.
 *
 * If adding the user fails for any reason, non-zero is returned. Zero is
 * returned upon success.
 *
 * @param proc
 *     The existing process to add the user to.
 *
 * @param parser
 *     The parser associated with the given guac_socket (used to handle the
 *     user's connection handshake thus far).
 *
 * @param socket
 *     The socket associated with the user to be added to the existing
 *     process.
 *
 * @return
 *     Zero if the user was added successfully, non-zero if an error occurred.
 */
static int guacd_add_user(guacd_proc* proc, guac_parser* parser, guac_socket* socket) {

#ifdef CYGWIN_BUILD

    SECURITY_ATTRIBUTES attributes = { 0 };
    attributes.nLength = sizeof(SECURITY_ATTRIBUTES);

    /*
     * Attempt to create a Windows security descriptor that grants access only
     * to the owner of this process.
     */
    if (!ConvertStringSecurityDescriptorToSecurityDescriptor(

            /* 
             * An SDDL string that uses DACL to grant the General Access (GA)
             * permission, only to the owner (OW). For more, see
             * https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-string-format.
             */
            "D:P(A;;GA;;;OW)",
            SDDL_REVISION_1,

            /* The populated security descriptor output */
            &(attributes.lpSecurityDescriptor),

            /* There's no need to capture the descriptor size */
            NULL

    )) {
        guacd_log(GUAC_LOG_ERROR, "Unable to initialize named pipe security descriptor.");
        return 1;
    }

    char pipe_name[GUAC_PIPE_NAME_LENGTH];

    /* Required pipe name prefix */
    memcpy(pipe_name, PIPE_NAME_PREFIX, strlen(PIPE_NAME_PREFIX));

    /* UUID to ensure the pipe name is unique */
    char* uuid = guac_generate_id('G');
    if (uuid == NULL) {
        guacd_log(GUAC_LOG_ERROR, "Unable to generate UUID for pipe name.");
        return 1;
    }

    memcpy(pipe_name + strlen(PIPE_NAME_PREFIX), uuid, GUAC_UUID_LEN);

    /* Null terminator */
    pipe_name[GUAC_PIPE_NAME_LENGTH - 1] = '\0';

    /* 
     * Set up a named pipe for communication with the user. For more, see
     * https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea
     */
    HANDLE pipe_handle = CreateNamedPipe(
        pipe_name, 

        /*
         * Read/write and "overlapped" (async) modes. PIPE_WAIT ensures
         * that completion actions do not occur until data is actually
         * ready, i.e. it's actually possible to wait for data.
         */
        PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED,

        /* Allow only one instance of this named pipe to be opened. 
         * PIPE_WAIT ensures that completion actions do not occur until data
         * is actually ready, i.e. it's actually possible to wait for data.
         * Also, allow only connections from the local machine.
         */
        PIPE_TYPE_BYTE | PIPE_WAIT | PIPE_REJECT_REMOTE_CLIENTS,

        /* Only this one instance of this named pipe is needed */
        1,

        /* Output and input buffer sizes */
        8192, 8192,

        /* Use the default timeout for the unused function WaitNamedPipe() */
        0,

        /* Set our custom security descriptor to allow only owner usage */
        &attributes

    );

    LocalFree(attributes.lpSecurityDescriptor);

    if (pipe_handle == INVALID_HANDLE_VALUE) {
        guacd_log(GUAC_LOG_ERROR, "Unable to create named pipe for IPC.");
        return 1;
    }
    
    /* If pipe creation failed, the error will already have been logged */
    if (pipe_handle == NULL)
        return 1;

    /* Send pipe name to process so it can connect to the pipe */
    if (!guacd_send_pipe(proc->fd_socket, pipe_name)) {
        CloseHandle(pipe_handle);
        guacd_log(GUAC_LOG_ERROR, "Unable to add user.");
        return 1;
    }

    /* Create an event to monitor for pipe connection */
    HANDLE event = CreateEvent(NULL, FALSE, FALSE, NULL);
    if (event == NULL) {
        guacd_log(GUAC_LOG_ERROR, "Event creation failed.");
        return 1;
    }

    /* Wait for the other end of the pipe to connect before attempting IO */
    OVERLAPPED overlapped = { 0 };
    overlapped.hEvent = event;
    ConnectNamedPipe(pipe_handle, &overlapped);
        
    /* Wait for 1 second for the other end to be connected */
    DWORD result = WaitForSingleObject(event, 1000);
    if (result == WAIT_FAILED) {

        /* 
         * If the wait failed for any reason other than the pipe being
         * already connected 
         */
        if (GetLastError() != ERROR_PIPE_CONNECTED) {
            guacd_log(GUAC_LOG_ERROR, "Named pipe connection not established.");
            return 1;
        }
        
    }

#else

    int sockets[2];

    /* Set up socket pair */
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) < 0) {
        guacd_log(GUAC_LOG_ERROR, "Unable to allocate file descriptors for I/O transfer: %s", strerror(errno));
        return 1;
    }

    int user_fd = sockets[0];
    int proc_fd = sockets[1];

    /* Send user file descriptor to process */
    if (!guacd_send_fd(proc->fd_socket, proc_fd)) {
        guacd_log(GUAC_LOG_ERROR, "Unable to add user.");
        return 1;
    }

    /* Close our end of the process file descriptor */
    close(proc_fd);

#endif

    guacd_connection_io_thread_params* params = malloc(sizeof(guacd_connection_io_thread_params));
    params->parser = parser;
    params->socket = socket;

#ifdef CYGWIN_BUILD
    params->handle = pipe_handle;
#else
    params->fd = user_fd;
#endif

    /* Start I/O thread */
    pthread_t io_thread;
    pthread_create(&io_thread,  NULL, guacd_connection_io_thread,  params);
    pthread_detach(io_thread);

    return 0;

}

/**
 * Routes the connection on the given socket according to the Guacamole
 * protocol, adding new users and creating new client processes as needed. If a
 * new process is created, this function blocks until that process terminates,
 * automatically deregistering the process at that point.
 *
 * The socket provided will be automatically freed when the connection
 * terminates unless routing fails, in which case non-zero is returned.
 *
 * @param map
 *     The map of existing client processes.
 *
 * @param socket
 *     The socket associated with the new connection that must be routed to
 *     a new or existing process within the given map.
 *
 * @return
 *     Zero if the connection was successfully routed, non-zero if routing has
 *     failed.
 */
static int guacd_route_connection(guacd_proc_map* map, guac_socket* socket) {

    guac_parser* parser = guac_parser_alloc();

    /* Reset guac_error */
    guac_error = GUAC_STATUS_SUCCESS;
    guac_error_message = NULL;

    /* Get protocol from select instruction */
    if (guac_parser_expect(parser, socket, GUACD_USEC_TIMEOUT, "select")) {

        /* Log error */
        guacd_log_handshake_failure();
        guacd_log_guac_error(GUAC_LOG_DEBUG,
                "Error reading \"select\"");

        guac_parser_free(parser);
        return 1;
    }

    /* Validate args to select */
    if (parser->argc != 1) {

        /* Log error */
        guacd_log_handshake_failure();
        guacd_log(GUAC_LOG_ERROR, "Bad number of arguments to \"select\" (%i)",
                parser->argc);

        guac_parser_free(parser);
        return 1;
    }

    guacd_proc* proc;
    int new_process;

    const char* identifier = parser->argv[0];

    /* If connection ID, retrieve existing process */
    if (identifier[0] == GUAC_CLIENT_ID_PREFIX) {

        proc = guacd_proc_map_retrieve(map, identifier);
        new_process = 0;

        /* Warn and ward off client if requested connection does not exist */
        if (proc == NULL) {
            guacd_log(GUAC_LOG_INFO, "Connection \"%s\" does not exist", identifier);
            guac_protocol_send_error(socket, "No such connection.",
                    GUAC_PROTOCOL_STATUS_RESOURCE_NOT_FOUND);
        }

        else
            guacd_log(GUAC_LOG_INFO, "Joining existing connection \"%s\"",
                    identifier);

    }

    /* Otherwise, create new client */
    else {

        guacd_log(GUAC_LOG_INFO, "Creating new client for protocol \"%s\"",
                identifier);

        /* Create new process */
        proc = guacd_create_proc(identifier);
        new_process = 1;

    }

    /* Abort if no process exists for the requested connection */
    if (proc == NULL) {
        guacd_log_guac_error(GUAC_LOG_INFO, "Connection did not succeed");
        guac_parser_free(parser);
        return 1;
    }

    /* Add new user (in the case of a new process, this will be the owner */
    int add_user_failed = guacd_add_user(proc, parser, socket);

    /* If new process was created, manage that process */
    if (new_process) {

        /* The new process will only be active if the user was added */
        if (!add_user_failed) {

            /* Log connection ID */
            guacd_log(GUAC_LOG_INFO, "Connection ID is \"%s\"",
                    proc->client->connection_id);

            /* Store process, allowing other users to join */
            guacd_proc_map_add(map, proc);

            /* Wait for child to finish */
            waitpid(proc->pid, NULL, 0);

            /* Remove client */
            if (guacd_proc_map_remove(map, proc->client->connection_id) == NULL)
                guacd_log(GUAC_LOG_ERROR, "Internal failure removing "
                        "client \"%s\". Client record will never be freed.",
                        proc->client->connection_id);
            else
                guacd_log(GUAC_LOG_INFO, "Connection \"%s\" removed.",
                        proc->client->connection_id);

        }

        /* Parser must be manually freed if the process did not start */
        else
            guac_parser_free(parser);

        /* Force process to stop and clean up */
        guacd_proc_stop(proc);

        /* Free skeleton client */
        guac_client_free(proc->client);

        /* Clean up */
        close(proc->fd_socket);
        free(proc);

    }

    /* Routing succeeded only if the user was added to a process */
    return add_user_failed;

}

void* guacd_connection_thread(void* data) {

    guacd_connection_thread_params* params = (guacd_connection_thread_params*) data;

    guacd_proc_map* map = params->map;
    int connected_socket_fd = params->connected_socket_fd;

    guac_socket* socket;

#ifdef ENABLE_SSL

    SSL_CTX* ssl_context = params->ssl_context;

    /* If SSL chosen, use it */
    if (ssl_context != NULL) {
        socket = guac_socket_open_secure(ssl_context, connected_socket_fd);
        if (socket == NULL) {
            guacd_log_guac_error(GUAC_LOG_ERROR, "Unable to set up SSL/TLS");
            close(connected_socket_fd);
            free(params);
            return NULL;
        }
    }
    else
        socket = guac_socket_open(connected_socket_fd);

#else
    /* Open guac_socket */
    socket = guac_socket_open(connected_handle);
#endif

    /* Route connection according to Guacamole, creating a new process if needed */
    if (guacd_route_connection(map, socket))
        guac_socket_free(socket);

    free(params);
    return NULL;

}

