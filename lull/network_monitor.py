import logging as log


class NetworkMonitor:
    def __init__(self, idle_threshold_mbps, psutil, clock):
        self.idle_threshold_mbps = idle_threshold_mbps
        self.psutil = psutil
        self.clock = clock
        self.last_time_s = 0.0
        self.last_traffic = 0
        self.is_reset = True

    def current_keepalive_request_s(self):
        traffic_mb = self.current_traffic_mb()
        elapsed_s = self.elapsed_time_s()
        if self.is_reset:
            self.is_reset = False
            return 0
        activity_mbps = traffic_mb / elapsed_s
        if activity_mbps > self.idle_threshold_mbps:
            log.info(f'Network is active ({activity_mbps:.3f} Mbps)')
            return 1
        else:
            return 0

    def current_traffic_mb(self):
        total_traffic = self.psutil.net_io_counters().bytes_sent + self.psutil.net_io_counters().bytes_recv
        traffic = total_traffic - self.last_traffic
        self.last_traffic = total_traffic
        return self.to_mb(traffic)

    def elapsed_time_s(self):
        elapsed_s = self.clock.time() - self.last_time_s
        self.last_time_s = self.clock.time()
        return elapsed_s

    @staticmethod
    def to_mb(traffic):
        return traffic / 1024. / 1024. * 8
