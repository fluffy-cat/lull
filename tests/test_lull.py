def test_shouldSleepOnlyAfterIdleTimeout_whenThereAreNoMonitors(controller, switch, clock):
    assert_no_sleep_at_time(0.0, clock, controller, switch)
    assert_no_sleep_at_time(30.0, clock, controller, switch)
    assert_sleep_at_time(31.0, clock, controller, switch)


def test_shouldSleepAgainAfterIdleTimeout_whenSystemHasWokenUpFromTheFirstSleep(controller, switch, clock):
    assert_sleep_at_time(31.0, clock, controller, switch)
    assert_no_sleep_at_time(1000.0, clock, controller, switch)
    assert_no_sleep_at_time(1030.0, clock, controller, switch)
    assert_sleep_at_time(1031.0, clock, controller, switch)


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
