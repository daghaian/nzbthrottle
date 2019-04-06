import plex
import nzb
import notification
import json
import time
import argparse
import logging.handlers
from helpers import stream_throttle_helpers as stream_helper


def start_monitor():
    try:
        lastThrottleState = False
        last_active_streams = 0
        #Initially set speed of nzbget to unthrottle or the user defined maxSpeed
        nzbServer.set_start_speed()
        while (1):
            logger.info("Requesting active stream count...")
            active_streams = plexServer.get_active_streams()
            state = nzbServer.get_current_throttle_status()
            if(state == False and lastThrottleState == True):
                    logger.debug("Previous state of throttle flag was True but currently not throttled, changing to False!")
                    lastThrottleState = False
            elif(state == True and lastThrottleState == False):
                    logger.debug("Previous state of throttle flag was False but currently we are throttled, changing to True!")
                    last_active_streams = plexServer.get_active_streams()
                    lastThrottleState = True
            if (active_streams != None):
                logger.info("Current stream count: %d", active_streams)
                if (lastThrottleState):
                    if (active_streams == 0):
                        logger.info("Streams are 0 and we are currently throttled. Lifting the limit")
                        throttleResponse = nzbServer.throttle_streams(active_streams)
                        if(throttleResponse != -1):
                            lastThrottleState = False
                            last_active_streams = active_streams
                            logger.info("Throttle lifted successfully")
                            try:
                                notifyClient.notify("Streams are 0 and we were throttled. Lifted the limit")
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                    elif(active_streams != last_active_streams):
                        logger.info("Already throttled, but stream count has changed, adjusting speed")
                        throttleResponse = nzbServer.throttle_streams(active_streams)
                        if (throttleResponse != -1):
                            last_active_streams = active_streams
                            logger.info("Speed throttling adjusted successfully")
                            try:
                                notifyClient.notify("Stream count has changed to {}, adjusted speed to: {} KB/s".format(active_streams,throttleResponse))
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                    else:
                        logger.info("Already throttled with no change. Continuing to monitor.")
                else:
                    if (active_streams > 0):
                        logger.info("There are currently active streams. Proceeding to throttle NZB")
                        throttleResponse = nzbServer.throttle_streams(active_streams)
                        if (throttleResponse != -1):
                            logger.info("NZB throttled successfully")
                            lastThrottleState = True
                            last_active_streams = active_streams
                            try:
                                notifyClient.notify("Currently {} active streams, throttled to: {} KB/s".format(active_streams,throttleResponse))
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                        else:
                            logger.error("Something went wrong when attempting to throttle NZB")
                    else:
                        logger.info("No active streams and not previously throttled. Ensuring correct unthrottle speed is set")
                        throttleResponse = nzbServer.throttle_streams(0)
                        if(throttleResponse != -1):
                            logger.info("Unthrottled speed set correctly")
            logger.info("Sleeping for %d seconds before checking again", plexServer.get_interval())
            time.sleep(plexServer.get_interval())
    except Exception as e:
        logger.exception("Start monitor encountered exception. Trying again in 60 seconds")

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

# initialize notification client
notifyClient = notification.NotificationClient()
# initialize plex server
plexServer = plex.PlexServer()
# initialize NZB server
nzbServer = nzb.NZB()

while(1):
    start_monitor()
