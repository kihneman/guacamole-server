import sys
import syslog
from argparse import ArgumentParser

from . import get_config, guacd_config, guacd_main, guacd_log
from .constants import GuacClientLogLevel, GUACD_LOG_NAME


parser = ArgumentParser(add_help=False)
parser.add_argument('--python', action='store_true')
# Remove --python from argv to not affect libguacd parser
ns, argv = parser.parse_known_args(sys.argv)

if ns.python:
    result, config = get_config(argv)

    # Init logging as early as possible
    guacd_log_level = config.max_log_level
    syslog.openlog(GUACD_LOG_NAME, logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)

    msg = f'Running with args {argv}, config result "{result}"'
    guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
    if config.print_version:
        guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, 'Printing help:')
        exit(result)

else:
    # parser.add_argument('-v', action='store_true')
    # ns, _ = parser.parse_known_args(argv)
    # if ns.v:
    #     result = guacd_main(argv)
    #     exit(result)

    result = guacd_main(argv)
    msg = f'Finished with result "{result}"'
    guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
