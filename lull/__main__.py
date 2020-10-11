import sys

import hiyapyco


def main():
    confs = sys.argv[1:]
    conf = hiyapyco.load(confs, method=hiyapyco.METHOD_MERGE, mergelists=False, failonmissingfiles=False)
    try:
        print(conf)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
