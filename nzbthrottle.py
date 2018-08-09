import plex
import logging
import logging.handlers

#Initialize Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create a file handler
# Max Log Size - 10 MB
# Max Log Count - 1
handler = logging.handlers.RotatingFileHandler(('./nzbthrottle.log'),maxBytes=10 * 1024 * 1024 , backupCount=1)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s-%(module)-6s: %(levelname)-8s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S ')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

p = plex.PlexServer()
p.monitor_active_streams()

