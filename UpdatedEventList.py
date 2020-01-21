import math
def UpdatedEventList(oldEventList, newEvent):
    pos = 0
    if oldEventList!=[]:
    # binary  search for position where to update
        lower = 0
        upper = len(oldEventList)

        while (lower < upper):
            pos = math.floor((lower + upper) / 2)
            curTime = oldEventList[pos]['time']
            if (newEvent['time'] < curTime):
                upper = pos
            else:
                lower = pos + 1
            #endif
        #endwhile

        pos = lower

        # insert new element at previously found position
    newEventList = oldEventList
    newEventList.insert(pos, newEvent)

    return newEventList