from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from lull.network_monitor import NetworkMonitor


@dataclass
class NetworkMetrics:
    bytes_sent: int = 0
    bytes_recv: int = 0


@pytest.fixture
def monitor(psutil, clock):
    return NetworkMonitor(8, psutil, clock)


@pytest.fixture
def psutil(iface):
    psutil = Mock()
    psutil.net_io_counters.return_value = iface
    return psutil


@pytest.fixture
def iface():
    return NetworkMetrics()


@pytest.fixture
def clock():
    clock = Mock()
    clock.time.return_value = 0.0
    return clock


def test_shouldNotReturnKeepAlive_whenTrafficIsBelowThreshold(monitor, clock, iface):
    clock.time.return_value = 5.0
    iface.bytes_sent = 123
    monitor.current_keepalive_request_s()
    clock.time.return_value = 35.0
    iface.bytes_sent = 123 + 1024 * 1024 * 30 - 1

    assert monitor.current_keepalive_request_s() == 0


def test_shouldNotReturnKeepAlive_whenTrafficIsAtThreshold(monitor, clock, iface):
    clock.time.return_value = 5.0
    iface.bytes_sent = 123
    monitor.current_keepalive_request_s()
    clock.time.return_value = 35.0
    iface.bytes_sent = 123 + 1024 * 1024 * 30

    assert monitor.current_keepalive_request_s() == 0


def test_shouldReturnKeepAlive_whenTransmitTrafficIsAboveThreshold(monitor, clock, iface):
    clock.time.return_value = 5.0
    iface.bytes_sent = 123
    monitor.current_keepalive_request_s()
    clock.time.return_value = 35.0
    iface.bytes_sent = 123 + 1024 * 1024 * 30 + 1

    assert monitor.current_keepalive_request_s() == 1


def test_shouldReturnKeepAlive_whenReceiveTrafficIsAboveThreshold(monitor, clock, iface):
    clock.time.return_value = 6.0
    monitor.current_keepalive_request_s()
    clock.time.return_value = 36.0
    iface.bytes_recv = 1024 * 1024 * 30 + 1

    assert monitor.current_keepalive_request_s() == 1


def test_shouldNotReturnKeepAlive_whenMonitorIsPolledForTheFirstTime(monitor, iface):
    iface.bytes_sent = 1024 * 1024 + 1

    assert monitor.current_keepalive_request_s() == 0
