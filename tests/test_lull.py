from unittest.mock import Mock


def test_shouldSleepOnlyAfterIdleTimeout_whenThereAreNoMonitors(controller, switch, clock):
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    assert_no_sleep_at_time(30.0, clock, controller, switch)
    assert_sleep_at_time(31.0, clock, controller, switch)


def test_shouldSleepAgainAfterIdleTimeout_whenSystemHasWokenUpFromTheFirstSleep(controller, switch, clock):
    assert_sleep_at_time(31.0, clock, controller, switch)
    assert_no_sleep_at_time(1000.0, clock, controller, switch)
    assert_no_sleep_at_time(1030.0, clock, controller, switch)
    assert_sleep_at_time(1031.0, clock, controller, switch)


def test_shouldSleepAfterIdleTimeout_whenMonitorMakeNoRequests(controller, switch, clock, monitors):
    monitor = Mock()
    monitor.current_keepalive_request_s.return_value = 0.0
    monitors.add(monitor)
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    assert_no_sleep_at_time(30.0, clock, controller, switch)
    assert_sleep_at_time(31.0, clock, controller, switch)


def test_shouldDeferSleep_whenMonitorMakesASingleKeepAliveRequest(controller, switch, clock, monitors):
    monitor = Mock()
    monitors.add(monitor)
    monitor.current_keepalive_request_s.return_value = 40.0
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(40.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_sleep_at_time(41.0, clock, controller, switch)


def test_shouldDeferSleep_whenMonitorMakesMultipleKeepAliveRequest(controller, switch, clock, monitors):
    monitor = Mock()
    monitors.add(monitor)
    monitor.current_keepalive_request_s.return_value = 50.0
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 50.0
    assert_no_sleep_at_time(30.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(80.0, clock, controller, switch)
    assert_sleep_at_time(81.0, clock, controller, switch)


def test_shouldStayAwakeForAMinimumDuration_whenMonitorMakesASmallKeepAliveRequest(controller, switch, clock, monitors):
    monitor = Mock()
    monitors.add(monitor)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 1.0
    assert_no_sleep_at_time(30.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(60.0, clock, controller, switch)
    assert_sleep_at_time(61.0, clock, controller, switch)


def test_shouldLimitKeepAliveTime_whenMonitorMakesALargeInitialRequestAndNoFurtherRequests(controller, switch, clock,
                                                                                           monitors):
    monitor = Mock()
    monitors.add(monitor)
    monitor.current_keepalive_request_s.return_value = 9000.0
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    monitor.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(120.0, clock, controller, switch)
    assert_sleep_at_time(121.0, clock, controller, switch)


def test_shouldDeferSleepToLatestRequest_whenMultipleMonitorsEachMakeARequest(controller, switch, clock, monitors):
    mon1 = Mock()
    monitors.add(mon1)
    mon1.current_keepalive_request_s.return_value = 40.0
    mon2 = Mock()
    monitors.add(mon2)
    mon2.current_keepalive_request_s.return_value = 50.0
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    mon1.current_keepalive_request_s.return_value = 0.0
    mon2.current_keepalive_request_s.return_value = 0.0
    assert_no_sleep_at_time(50.0, clock, controller, switch)
    assert_sleep_at_time(51.0, clock, controller, switch)


def assert_no_sleep_at_time(time, clock, controller, switch):
    clock.time.return_value = time
    controller.tick()
    switch.sleep.assert_not_called()
    switch.sleep.reset_mock()


def assert_sleep_at_time(time, clock, controller, switch):
    clock.time.return_value = time
    controller.tick()
    switch.sleep.assert_called_once()
    switch.sleep.reset_mock()
