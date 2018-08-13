import logging

logger = logging.getLogger()

def find_nearest(speeds,currStreamCount):
    return speeds[str(currStreamCount)] if str(currStreamCount) in speeds else speeds[min(sorted(speeds.keys(),key=lambda x: abs(int(x)-currStreamCount)))]
