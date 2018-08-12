import logging

logger = logging.getLogger()

def find_nearest(speeds,currStreamCount):
    sortedSpeedIntervals = sorted([int(i) for i in speeds.keys()])

    # Check if there is an exact match for currentCount
    if(currStreamCount in sortedSpeedIntervals):
        logger.debug("No need to iterate through defined speeds, exact stream count speed defined!")
        return speeds[str(currStreamCount)]
    # Check if currentCount is less then the smallest
    elif(currStreamCount < sortedSpeedIntervals[0]):
        logger.debug("Current stream count is smaller than the lowest speed increment defined")
        return speeds[str(sortedSpeedIntervals[0])]
    elif(currStreamCount > sortedSpeedIntervals[len(speeds)-1]):
        logger.debug("Current stream count is larger than the largest speed increment defined")
        return speeds[str(sortedSpeedIntervals[len(speeds)-1])]
    else:
        logger.debug("Iterating through speed increments to calculate best match")
        for i in range(0,len(sortedSpeedIntervals)):
            if(i != len(sortedSpeedIntervals)-1):
                if(currStreamCount < sortedSpeedIntervals[i+1]):
                    logger.debug("Stuck between two. I have %d on lower bound and %d on upper",sortedSpeedIntervals[i],sortedSpeedIntervals[i+1])
                    lowerDiff = abs(sortedSpeedIntervals[i] - currStreamCount)
                    upperDiff = abs(sortedSpeedIntervals[i+1] - currStreamCount)
                    if(lowerDiff < upperDiff):
                        return speeds[str(sortedSpeedIntervals[i])]
                    if(lowerDiff > upperDiff):
                        return speeds[str(sortedSpeedIntervals[i+1])]
                    else:
                        return speeds[str(sortedSpeedIntervals[i])]