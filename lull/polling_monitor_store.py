class PollingMonitorStore:
    def __init__(self, min_inhibitor_s, max_inhibitor_s, clock):
        self.sleep_at_time_s = 0.0
        self.clock = clock
        self.min_inhibitor_s = min_inhibitor_s
        self.max_inhibitor_s = max_inhibitor_s
        self.reset()
        self.monitors = []

    def reset(self):
        self.sleep_at_time_s = self.clock.time() + self.min_inhibitor_s

    def current_sleep_time(self):
        sleep_at_times = [self.calculate_sleep_time(m.current_keepalive_request_s()) for m in self.monitors if
                          m.current_keepalive_request_s() > 0]
        sleep_at_times.append(self.sleep_at_time_s)
        self.sleep_at_time_s = max(sleep_at_times)
        return self.sleep_at_time_s

    def add(self, monitor):
        self.monitors.append(monitor)

    def calculate_sleep_time(self, request):
        req = self.clamp_keepalive_request_to_limits(request)
        return req + self.clock.time()

    def clamp_keepalive_request_to_limits(self, keepalive_request_s):
        return min(max(keepalive_request_s, self.min_inhibitor_s), self.max_inhibitor_s)
