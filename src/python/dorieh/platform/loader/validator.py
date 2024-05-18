
import sys

from dorieh.platform.loader import LoaderBase

if __name__ == '__main__':
    LoaderBase.get_domain(sys.argv[1])
