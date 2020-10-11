class ControlLoop:
    def __init__(self, monitors, switch, clock):
        self.monitors = monitors
        self.switch = switch
        self.clock = clock
        self.isAsleep = False

    def tick(self):
        self.reset_monitors_after_wakeup()
        if self.is_idle():
            self.switch.sleep()
            self.isAsleep = True

    def is_idle(self):
        sleep_at_time_s = self.monitors.current_sleep_time()
        return self.clock.time() > sleep_at_time_s

    def reset_monitors_after_wakeup(self):
        if self.isAsleep:
            self.monitors.reset()
            self.isAsleep = False
