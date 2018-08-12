import plex
import nzb
import json
import time
import logging.handlers
from helpers import stream_throttle_helpers as stream_helper

#Initialize Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create a file handler
# Max Log Size - 10 MB
# Max Log Count - 1
fh = logging.handlers.RotatingFileHandler('./nzbthrottle.log',maxBytes=10 * 1024 * 1024 , backupCount=1)
fh.setLevel(logging.INFO)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s-%(module)-6s: %(levelname)-8s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S ')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

p = plex.PlexServer()
n = nzb.NZB()
currThrottled = False
while(1):
    logger.info("Requesting active stream count...")
    active_streams = p.get_active_streams()
    if(active_streams != None):
        logger.info("Current stream count: %d",active_streams)
        if(active_streams > 0):
            logger.info("There are currently active streams. Proceeding to throttle NZB")

    logger.info("Sleeping for %d seconds before checking again",p.get_interval())
    time.sleep(p.get_interval())


