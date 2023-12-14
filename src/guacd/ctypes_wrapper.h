//
// Created by KevinKihneman on 11/15/2023.
//

#ifndef PYTHON_WRAPPER_H
#define PYTHON_WRAPPER_H

#include <guacamole/client-types.h>

/** conf.h **/
/**
 * The default host that guacd should bind to, if no other host is explicitly
 * specified.
 */
#define GUACD_DEFAULT_BIND_HOST "localhost"

/**
 * The default port that guacd should bind to, if no other port is explicitly
 * specified.
 */
#define GUACD_DEFAULT_BIND_PORT "4822"

/**
 * The contents of a guacd configuration file.
 */
typedef struct guacd_config {

    /**
     * The host to bind on.
     */
    char* bind_host;

    /**
     * The port to bind on.
     */
    char* bind_port;

    /**
     * The file to write the PID in, if any.
     */
    char* pidfile;

    /**
     * Whether guacd should run in the foreground.
     */
    int foreground;

    /**
     * Whether guacd should simply print its version information and exit.
     */
    int print_version;

#ifdef ENABLE_SSL
    /**
     * SSL certificate file.
     */
    char* cert_file;

    /**
     * SSL private key file.
     */
    char* key_file;
#endif

    /**
     * The maximum log level to be logged by guacd.
     */
    guac_client_log_level max_log_level;

} guacd_config;


/** conf-file.h **/
/**
 * Loads the configuration from any of several default locations, if found. If
 * parsing fails, NULL is returned, and an error message is printed to stderr.
 */
guacd_config* guacd_conf_load();


/** conf-args.h **/
/**
 * Parses the given arguments into the given configuration. Zero is returned on
 * success, and non-zero is returned if arguments cannot be parsed.
 */
int guacd_conf_parse_args(guacd_config* config, int argc, char** argv);


int main(int argc, char* argv[]);

#endif
