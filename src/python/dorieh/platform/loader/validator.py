
import sys

from dorieh.platform.loader import LoaderBase


def main():
    LoaderBase.get_domain(sys.argv[1])


if __name__ == '__main__':
    main()