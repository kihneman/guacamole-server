//
// Created by KevinKihneman on 11/15/2023.
//

#ifndef PYTHON_WRAPPER_H
#define PYTHON_WRAPPER_H

#include <guacamole/client-types.h>

int main(int argc, char* argv[]);
void guacd_log(guac_client_log_level level, const char* format, ...);

#endif
