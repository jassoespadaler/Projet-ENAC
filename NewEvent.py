def NewEvent(time, typeEvent, pickUpStation, prevDrop, dropOffStation, requestLocation, requestTime, completedLocation, completedTime):
    event = {
        'time' : time,
        'typeEvent' : typeEvent,
        'pickUpStation' : pickUpStation,
        'prevDrop' : prevDrop,
        'dropOffStation' : dropOffStation,
        'requestLocation' : requestLocation,
        'requestTime' : requestTime,
        'completedLocation' : completedLocation,
        'completedTime' : completedTime
    }
    return event