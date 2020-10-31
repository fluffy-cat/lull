from collections import namedtuple
from unittest.mock import Mock

import pytest

from lull.tcp_monitor import TCPMonitor

Conn = namedtuple('Connection', ['laddr', 'status'])
Addr = namedtuple('Address', ['ip', 'port'])


@pytest.fixture
def psutil():
    return Mock()


def test_shouldNotReturnKeepAlive_whenThereAreNoConnections(psutil):
    monitor = TCPMonitor([22], psutil)
    assert_keepalive_given_connections([], 0, monitor, psutil)


def test_shouldReturnKeepAlive_whenThereIsAnActiveConnection(psutil):
    monitor = TCPMonitor([22], psutil)
    assert_keepalive_given_connections([Conn(Addr('192.168.245.130', 22), 'ESTABLISHED')], 1, monitor, psutil)


def test_shouldNotReturnKeepAlive_whenConnectionIsInactive(psutil):
    monitor = TCPMonitor([22], psutil)
    assert_keepalive_given_connections(
        [Conn(Addr('192.168.245.130', 22), 'CLOSE'), Conn(Addr('192.168.245.130', 22), 'CLOSE_WAIT')], 0, monitor,
        psutil)


def test_shouldNotReturnKeepAlive_whenConnectionIsFromAnotherPort(psutil):
    monitor = TCPMonitor([22], psutil)

    assert_keepalive_given_connections(
        [Conn(Addr('192.168.245.130', 80), 'ESTABLISHED'), Conn(Addr('192.168.245.130', 443), 'ESTABLISHED')], 0,
        monitor, psutil)


def test_shouldReturnKeepAlive_whenMultiplePortsAreMonitored(psutil):
    monitor = TCPMonitor([22, 23], psutil)
    assert_keepalive_given_connections([Conn(Addr('192.168.245.130', 22), 'ESTABLISHED')], 1, monitor, psutil)
    assert_keepalive_given_connections([Conn(Addr('192.168.245.130', 23), 'ESTABLISHED')], 1, monitor, psutil)
    assert_keepalive_given_connections([Conn(Addr('192.168.245.130', 24), 'ESTABLISHED')], 0, monitor, psutil)


def assert_keepalive_given_connections(connections, keepalive, monitor, psutil):
    psutil.net_connections.return_value = connections
    assert monitor.current_keepalive_request_s() == keepalive
