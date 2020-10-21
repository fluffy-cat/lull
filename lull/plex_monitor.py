import logging as log

from plexapi.server import PlexServer


class PlexMonitor:
    def __init__(self, conf):
        url = conf['url']
        token = conf['token']
        self.plex = PlexServer(url, token)

    def current_keepalive_request_s(self):
        if self.is_active():
            log.info(
                f'Plex is active with {len(self.plex.sessions())} sessions and {len(self.plex.activities)} activities')
            return 1
        else:
            return 0

    def is_active(self):
        return len(self.plex.activities) > 0 or len(self.plex.sessions()) > 0
