import logging
import logging.config
import sys
import time

import hiyapyco
import psutil

from lull.control_loop import ControlLoop
from lull.plex_monitor import PlexMonitor
from lull.polling_monitor_store import PollingMonitorStore
from lull.systemd_switch import SystemDSwitch
from lull.tcp_monitor import TCPMonitor


def main():
    logging.config.fileConfig('/config/logging.ini')
    confs = sys.argv[1:]
    conf = hiyapyco.load(confs, method=hiyapyco.METHOD_MERGE, mergelists=False, failonmissingfiles=False)
    switch = create_standby_switch(conf['home_assistant_switch'])
    monitors = create_monitors(conf['monitors'])
    clock = time
    monitor_store = create_monitor_storage(conf, clock, monitors)
    controller = create_control_loop(conf, monitor_store, switch, clock)
    try:
        controller.start()
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Control loop interrupted. Shutting down lull monitor')
        pass


def create_control_loop(conf, monitors, switch, clock):
    return ControlLoop(conf['monitor_poll_interval_s'], monitors, switch, clock)


def create_monitors(conf):
    monitors = []
    if conf['plex']:
        monitors.append(create_plex_monitor(conf['plex']))
    if conf['tcp']:
        monitors.append(create_tcp_monitor(conf['tcp']))
    return monitors


def create_monitor_storage(conf, clock, monitors):
    store = PollingMonitorStore(conf['sleep_after_idle_duration_s'], conf['max_keepalive_duration_s'], clock)
    for m in monitors:
        store.add(m)
    return store


def create_standby_switch(conf):
    return SystemDSwitch(conf['url'], conf['switch_name'], conf['token'])


def create_tcp_monitor(conf):
    return TCPMonitor(conf['ports'], psutil)


def create_plex_monitor(conf):
    return PlexMonitor(conf['url'], conf['token'])


if __name__ == '__main__':
    main()
