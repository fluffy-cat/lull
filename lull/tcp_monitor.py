class TCPMonitor:
    def __init__(self, ports, psutil):
        self.ports = ports
        self.psutil = psutil

    def current_keepalive_request_s(self):
        for c in self.psutil.net_connections(kind="tcp"):
            if self.is_active(c):
                return 1
        return 0

    def is_active(self, connection):
        return connection.laddr.port in self.ports and connection.status == "ESTABLISHED"
