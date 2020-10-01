import sys

import hiyapyco
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    confs = [sys.argv[1], sys.argv[2]]
    conf = hiyapyco.load(confs, method=hiyapyco.METHOD_MERGE, mergelists=False, failonmissingfiles=False)
    scheduler = BlockingScheduler()
    try:
        print(conf)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
