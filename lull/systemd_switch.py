import requests


class SystemDSwitch:
    def __init__(self, url, switch_name, token):
        self.url = f"{url}/api/services/switch/turn_off"
        self.payload = {"entity_id": f"switch.{switch_name}"}
        self.headers = {"Authorization": f"Bearer {token}"}

    def sleep(self):
        requests.post(self.url, json=self.payload, headers=self.headers)
