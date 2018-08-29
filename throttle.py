import plex
import nzb
import json
import time
import argparse
import logging.handlers
from helpers import stream_throttle_helpers as stream_helper


def start_monitor():
    try:
        lastThrottleState = False
        last_active_streams = p.get_active_streams()
        while (1):
            logger.info("Requesting active stream count...")
            active_streams = p.get_active_streams()

            if(n.get_current_throttle_status() == False and lastThrottleState == True):
                logger.debug("Previous state of throttle flag was True but currently not throttled, changing to False!")
                lastThrottleState = False

            if (active_streams != None):
                logger.info("Current stream count: %d", active_streams)
                if (lastThrottleState):
                    if (active_streams == 0):
                        logger.info("Streams are 0 and we are currently throttled. Lifting the limit")
                        if(n.throttle_streams(active_streams) == True):
                            lastThrottleState = False
                            last_active_streams = active_streams
                            logger.info("Throttle lifted successfully")
                    elif(active_streams != last_active_streams):
                        logger.info("Already throttled, but stream count has changed, adjusting speed")
                        if (n.throttle_streams(active_streams) == True):
                            last_active_streams = active_streams
                            logger.info("Speed throttling adjusted successfully")
                    else:
                        logger.info("Already throttled with no change. Continuing to monitor.")
                else:
                    if (active_streams > 0):
                        logger.info("There are currently active streams. Proceeding to throttle NZB")
                        if (n.throttle_streams(active_streams) == True):
                            logger.info("NZB throttled successfully")
                            lastThrottleState = True
                            last_active_streams = active_streams
                        else:
                            logger.error("Something went wrong when attemping to throttle NZB")
            logger.info("Sleeping for %d seconds before checking again", p.get_interval())
            time.sleep(p.get_interval())
    except Exception as e:
        logger.error("Start monitor encountered exception. Trying again in 60 seconds")
        time.sleep(60)

#=======================================================#
#                       INIT                            #
#=======================================================#

#Grab command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--log-level',type=str,default='INFO',choices=['INFO','DEBUG','WARN'],help="Level of Logging Desired (Default: INFO)")

#Initialize Logging
logger = logging.getLogger()
logger.setLevel(parser.parse_args().log_level)

# create a file handler
# Max Log Size - 10 MB
# Max Log Count - 1
fh = logging.handlers.RotatingFileHandler('./nzbthrottle.log',maxBytes=10 * 1024 * 1024 , backupCount=1)

# create console handler
ch = logging.StreamHandler()

# create a logging format
formatter = logging.Formatter('%(asctime)s-%(module)-6s: %(levelname)-8s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S ')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

p = plex.PlexServer()
n = nzb.NZB()

while(1):
    start_monitor()