import logging as log
from datetime import datetime


class ControlLoop:
    def __init__(self, poll_interval_s, monitors, switch, clock):
        self.poll_interval_s = poll_interval_s
        self.monitors = monitors
        self.switch = switch
        self.clock = clock
        self.last_tick_s = clock.time()

    def start(self):
        log.info('Monitoring server for user activity')
        while True:
            self.tick()
            self.clock.sleep(self.poll_interval_s)

    def tick(self):
        self.reset_monitors_after_wakeup()
        self.last_tick_s = self.clock.time()
        if self.is_idle():
            log.info('System is now idle. Sending sleep command')
            self.switch.sleep()

    def is_idle(self):
        sleep_at_time_s = self.monitors.current_sleep_time()
        log.info(f'System scheduled to sleep at {datetime.fromtimestamp(sleep_at_time_s)}')
        return self.clock.time() > sleep_at_time_s

    def reset_monitors_after_wakeup(self):
        if self.isAsleep():
            log.info('System is now awake. Resetting monitors')
            self.monitors.reset()

    # Assume system was asleep if more than 4 poll intervals has elapsed and tick was not called
    def isAsleep(self):
        return self.clock.time() > self.last_tick_s + self.poll_interval_s * 4
