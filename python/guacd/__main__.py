import sys

from . import guacd_main, guacd_log
from .constants import GuacClientLogLevel


result = guacd_main()
msg = f'Running with args {sys.argv}, result "{result}"'
guacd_log(GuacClientLogLevel.GUAC_LOG_INFO, msg)
