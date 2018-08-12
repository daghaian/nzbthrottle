
import requests
import json
import xml.etree.ElementTree as ET
import logging
import sys

class PlexServer(object):
    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                self._logger.info("Loading Plex config.json")
                cfg = json.load(w)
                self._logger.info("Plex Config loaded successfully" + str(cfg))
                self._url = cfg['plex']['url']
                self._token =  cfg['plex']['token']
                self._interval =  cfg['plex']['interval']
        except Exception as e:
            self._logger.exception("Problem encountered when creating PlexServer object")
            sys.exit(1)

    def get_interval(self):
        return self._interval

    def get_active_streams(self):
        try:
            r = requests.get(self._url + "/status/sessions",headers={'X-Plex-Token':self._token})
            if(r.status_code == 200):
                root = ET.fromstring(r.text)
                return int(root.attrib['size'])
            else:
                self._logger.error("Did not get expected response from Plex API: %s",r.text)
        except Exception as e:
            self._logger.exception("Failed to successfully request current active sessions from Plex")



