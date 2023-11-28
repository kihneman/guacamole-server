import sys
from argparse import ArgumentParser

from . import get_config, guacd_config, guacd_main, guacd_log
from .constants import GuacClientLogLevel


# parser = ArgumentParser(add_help=False)
# parser.add_argument('-v', action='store_true')
# ns, argv = parser.parse_known_args(sys.argv)
# if ns.v:
#     result = guacd_main()
#     exit(result)

result, config = get_config()
msg = f'Running with args {sys.argv}, config result "{result}"'
guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
result = guacd_main()
if config.print_version:
    guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, 'Printing help:')
    exit(result)

# result = guacd_main()
msg = f'Finished with result "{result}"'
guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
