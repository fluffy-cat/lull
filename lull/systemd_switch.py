import requests


class SystemDSwitch:
    def __init__(self, conf):
        self.url = f"{conf['url']}/api/services/switch/turn_off"
        self.payload = {"entity_id": f"switch.{conf['switch_name']}"}
        self.headers = {"Authorization": f"Bearer {conf['token']}"}

    def sleep(self):
        requests.post(self.url, json=self.payload, headers=self.headers)
