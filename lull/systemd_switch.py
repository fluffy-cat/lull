class SystemDSwitch:
    def __init__(self, conf):
        self.sleep_command = conf['command']

    def sleep(self):
        self.sleep_command
