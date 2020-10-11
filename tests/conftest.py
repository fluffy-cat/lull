from unittest.mock import Mock

import pytest

from lull.control_loop import ControlLoop
from lull.polling_monitor_store import PollingMonitorStore


@pytest.fixture
def switch():
    return Mock()


@pytest.fixture
def clock():
    clk = Mock()
    clk.time.return_value = 0.0
    return clk


@pytest.fixture
def controller(switch, clock):
    monitors = PollingMonitorStore({'sleep_after_idle_duration_s': 30, 'max_keepalive_duration_s': 120}, clock)
    return ControlLoop(monitors, switch, clock)
