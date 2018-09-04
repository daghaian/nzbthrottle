import logging
import requests
import json
import sys
from helpers import stream_throttle_helpers as stream_helper

class NZB(object):
    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                self._logger.debug("Loading NZB config.json")
                cfg = json.load(w)
                self._logger.debug("NZB Config loaded successfully" + str(cfg))
                self._url = cfg['nzbget']['url']
                self._username = cfg['nzbget']['username']
                self._password = cfg['nzbget']['password']
                self._speedIncrements = cfg['nzbget']['speeds']
                self._maxSpeed = cfg['nzbget']['max_speed']
        except Exception as e:
            self._logger.exception("Problem encountered when creating NZB object")
            sys.exit(1)
    def get_maxSpeed(self):
        return self._maxSpeed
    def set_start_speed(self):
        self._logger.info("Setting initial speed for NZB as %d",self._maxSpeed if self._maxSpeed else 0)
        self.throttle_streams(0)

    def get_speedIncrements(self):
        return self._speedIncrements

    def get_current_throttle_status(self):
        self._logger.debug("Grabbing current state of NZBGet")
        currStatus = json.loads(self.run_method("status"))
        if(currStatus != None):
            self._logger.debug("Current status of NZBGet is %s",currStatus)
            self._logger.debug("Current rate of NZBGet download is %d",currStatus['result']['DownloadLimit'])
            if(currStatus['result']['DownloadLimit'] == 0 or (self._maxSpeed and currStatus['result']['DownloadLimit'] >= (self._maxSpeed * 1000))):
                self._logger.debug("NZB is current NOT throttled, returning False")
                return False
            else:
                self._logger.debug("NZB is currently throttled with a speed of %d. Returning true",currStatus['result']['DownloadLimit'])
                return True
        else:
            self._logger.error("Something went wrong when requesting the current status of NZBGet")


    def throttle_streams(self,active_streams):
        currRate = 0 if not self._maxSpeed else self._maxSpeed
        if(active_streams != 0):
            currRate = stream_helper.find_nearest(self._speedIncrements,active_streams)
        throttleResponse = json.loads(self.run_method("rate",currRate))
        if ('result' in throttleResponse and throttleResponse["result"] == True):
            return True
        return False


    def run_method(self,method,params=None):
        try:
            self._logger.debug("Requesting method: " + str(method) + " with params: " + str(params))
            r = requests.post(self._url + '/{username}:{password}/jsonrpc'.format(username=self._username,password=self._password),headers={'Content-type':'application/json'},json={"method":method,"params": params if not None else []})
            if(r.status_code == 200):
                self._logger.debug("Response from NZBGet: " + str(r.text))
                return r.text
            else:
                self._logger.error("Did not get expected response from NZB API: %s",r.text)
                return None
        except Exception as e:
            self._logger.exception("Error encountered when requesting method: " + str(method) + " with params: " + str(params))
