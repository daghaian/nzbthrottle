import logging
import requests
import json
import sys

class NZB(object):

    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                self._logger.info("Loading NZB config.json")
                cfg = json.load(w)
                self._logger.info("NZB Config loaded successfully" + str(cfg))
                self._url = cfg['nzbget']['url']
                self._username = cfg['nzbget']['username']
                self._password = cfg['nzbget']['password']
                self._speedIncrements = cfg['nzbget']['speeds']
        except Exception as e:
            self._logger.exception("Problem encountered when creating NZB object")
            sys.exit(1)

