class PollingMonitorStore:
    def __init__(self, conf, clock):
        self.clock = clock
        self.min_inhibitor_s = conf['sleep_after_idle_duration_s']
        self.max_inhibitor_s = conf['max_keepalive_duration_s']
        self.reset()

    def reset(self):
        self.sleep_at_time_s = self.clock.time() + self.min_inhibitor_s

    def tick(self):
        return self.sleep_at_time_s
