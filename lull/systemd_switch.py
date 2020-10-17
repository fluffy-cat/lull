import os


class SystemDSwitch:
    def __init__(self, conf):
        self.user = conf['user']
        self.host = conf['host']
        self.key_path = conf['private_key_path']
        self.sleep_command = conf['command']

    def sleep(self):
        os.system(f'ssh -i {self.key_path} {self.user}@{self.host} \'{self.sleep_command}\'')
