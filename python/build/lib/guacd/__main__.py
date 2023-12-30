import sys

from . import main


result = main()
print(f'Running with args {sys.argv}, result "{result}"')
