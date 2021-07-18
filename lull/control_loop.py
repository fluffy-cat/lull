import logging as log
from datetime import datetime


class ControlLoop:
    def __init__(self, poll_interval_s, monitors, switch, clock):
        self.poll_interval_s = poll_interval_s
        self.monitors = monitors
        self.switch = switch
        self.clock = clock
        self.is_asleep = False
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
            self.is_asleep = True

    def is_idle(self):
        sleep_at_time_s = self.monitors.current_sleep_time()
        log.info(f'System scheduled to sleep at {datetime.fromtimestamp(sleep_at_time_s)}')
        return self.clock.time() > sleep_at_time_s

    def reset_monitors_after_wakeup(self):
        if self.is_resumed_from_sleep():
            log.info('System is now awake. Resetting monitors')
            self.monitors.reset()
            self.is_asleep = False

    def is_resumed_from_sleep(self):
        """ Determine if system has just woken up from a sleep

        If lull application has put the system to sleep, then we can identify an awakened system by the is_asleep flag.
        Otherwise, we can assume the system was asleep if more than 4 poll intervals has elapsed and tick was not called
        """
        return self.is_asleep or self.clock.time() > self.last_tick_s + self.poll_interval_s * 4
