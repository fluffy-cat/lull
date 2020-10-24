import logging as log

import requests

REQUEST_TIMEOUT_S = 5


class SystemDSwitch:
    def __init__(self, url, switch_name, token):
        self.url = f"{url}/api/services/switch/turn_off"
        self.payload = {"entity_id": f"switch.{switch_name}"}
        self.headers = {"Authorization": f"Bearer {token}"}

    def sleep(self):
        try:
            requests.post(self.url, json=self.payload, headers=self.headers, timeout=REQUEST_TIMEOUT_S)
        except requests.exceptions.Timeout as e:
            log.info(f'Shutdown request timeout after {REQUEST_TIMEOUT_S}s: {e}')
