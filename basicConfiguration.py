import math
import numpy as np
from numpy import linalg as LA
from copy import deepcopy
from UpdatedEventList import UpdatedEventList
from NewEvent import NewEvent
def basicConfiguration(requestLocations, completedLocations, times, vehiclesAtStation, capacityOfStation, stationLocations, c_baseTimeBicycleDF, c_trafficTimeCar, c_distanceCar, c_distanceBicycle):

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
    # DESCRIPTION
    #
    # usage: [fullEventList, availabilityTime, lostDemand] = basicConfiguration(requestLocations, completedLocations,
    #                                                                             times, vehiclesAtStation,
    #                                                                             capacityAtStation, stationLocations,
    #                                                                             c_baseTimeBicycle, c_trafficTimeCar)

    # The    demand    for a vehicle and parking spot are generated randomly in the
    # city(without    any    information    on    urban and rural    areas and the    dynamics
    # of    the    city).

    # The    REQUEST    event is generated, which    triggers        PICKUP
    # event(This    event    assigns    the    request    to    the    closest    station    having
    # available    vehicles    at    the    moment.If    there    are    no    available    vehicles
    # within    the    300    m    circle    of    the    requestLocation, the    customer    opts    out.).
    # The    user is assumed    to    walk    from the requestLocation    to    pickUpLocation.
    # If    there    are    no    vehicles    available    at    the    station    when    the    customer
    # arrives, s / he    opts    out.

    # In    the    case    of    available    vehicle, the    user    starts    the    journey.This
    # triggers    the    event    DROPOFF.The    availability    of    a    parking    spot is not
    # checked in advance.When    the    user    arrives    to    the    closest    station, and
    # cannot    find    a    parking    spot, s / he    goes    to    the    next    closest    station.This
    # triggers    another    DROPOFF    event and a    DROPOFF - REDIRECTED    event    for the

    # DROPOFF        that        could        not be        executed.
    # Since        the        user        has        to        park        the
    # vehicle, s / he    looks    for a place until s / he finds.There is no opt-out
    # option    at    this    point.

    # When    the    user    finds    a    parking    spot, s / he    parks    the    vehicle and walks    to
    # the    completedLocation    which is handled    by    the    last    event    type    COMPLETED.
    #
    # ----------------------------------------------------------------------------
    # PARAMETERS
    #
    # requestLocations    set    of(x, y)    coordinates    of    generation    of    order
    # completedLocations    set    of    times    at    which    the    order is placed
    # times
    # vehiclesAtStation
    # capacityAtStation    matrix    indicating    the    number    of    drones    at    each    open    hub
    # stationLocations    locations    of    all    possible    hubs
    #
    # ---------------------------------------------------------------------------
    # RETURN    VALUES
    #
    # fullEventList         array    of    hubs    assigned    to    each    order
    # availabilityTime      event    list    of    all    events
    # lostDemand
    # nbCustomersTime1
    #
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==

    stationLocations = np.fliplr(stationLocations)
    parkingSpotsAtStation = capacityOfStation - vehiclesAtStation

    c_baseTimeBicycle = c_baseTimeBicycleDF.values
    c_baseTimeBicycle = c_baseTimeBicycle[:, 1:] ##here, ask why?
    EventList = []
    fullEventList = []
    availabilityTime = []

    nbCustomersTime = []
    nbCustomersInTheSystem = 0


    lostDemandTime = []
    lostDemand = 0

    walkingSpeed = 5 # km / h
    cyclingSpeed = 20 # km / h
    drivingSpeed = 55 # km / h

    vehicleSpeed = drivingSpeed

    for i in range(len(times)):
        # REQUEST event
        event = NewEvent(times[i][0], 1, 0, math.inf, 0, requestLocations[i], times[i][0], completedLocations[i], math.inf)
        EventList = UpdatedEventList(EventList, event)
        fullEventList = UpdatedEventList(fullEventList, event)
    #endfor

    cust = {
        'time': 0,
        'number': nbCustomersInTheSystem
    }


    nbCustomersTime.append(cust)
    nbCustomersTime

    while len(EventList)>0:
        currentEvent = EventList[0]
        EventList.pop(0)

        vehiclesAtStationCp = deepcopy(vehiclesAtStation)

        av = {
            'time': currentEvent['time'],
            'avail': vehiclesAtStationCp
        }

        availabilityTime.append(av)

        if currentEvent['typeEvent'] == 1:      #REQUEST event
            nbCustomersInTheSystem = nbCustomersInTheSystem +1

            cust = {
                'time': currentEvent['time'],
                'number' : nbCustomersInTheSystem
            }

            nbCustomersTime.append(cust)

            proximityHubs = []

            for j in range(len(stationLocations)):
                proximityHubs.append(LA.norm(stationLocations[j,:]-currentEvent['requestLocation']))

            distAssignedStation = 0
            pickUpStation = 0

            while 1:
                distAssignedStation = min(p for p in proximityHubs if p>distAssignedStation)
                idxAssignedStation = proximityHubs.index(distAssignedStation)

                if distAssignedStation > 0.8:
                    lostDemand = lostDemand + 1
                    nbCustomersInTheSystem = nbCustomersInTheSystem - 1

                    cust = {
                        'time' : currentEvent['time'],
                        'number' : nbCustomersInTheSystem
                    }

                    nbCustomersTime.append(cust)
                    break
                else:
                    if vehiclesAtStation[0,idxAssignedStation] > 0:
                        pickUpStation = idxAssignedStation
                        break
                    else:
                        print("Assign to another pick up station\n")
            #endwhile

            if pickUpStation > 0:
                # Trigger PICKUP event
                nextEventTime = (LA.norm(stationLocations[pickUpStation]-currentEvent['requestLocation'])*100)/walkingSpeed + currentEvent['time']

                pickUpEvent = NewEvent(nextEventTime, 2, pickUpStation, math.inf, 0, currentEvent['requestLocation'], currentEvent['requestTime'], currentEvent['completedLocation'], math.inf)
                fullEventList = UpdatedEventList(fullEventList, pickUpEvent)
                EventList = UpdatedEventList(EventList, pickUpEvent)
            #endif
        # endif for REQUEST

        if currentEvent['typeEvent'] == 2:      #PICKUP event
            if vehiclesAtStation[0,currentEvent['pickUpStation']] >0:

                proximityHubs = []

                for j in range(len(stationLocations)):
                    proximityHubs.append(LA.norm(stationLocations[j, :] - currentEvent['completedLocation']))
                
                dropOffStation = proximityHubs.index(min(proximityHubs))
                #print(np.shape(c_baseTimeBicycle))
                #print(currentEvent['pickUpStation'])
                #print(dropOffStation)
                
                nextEventTime = (c_baseTimeBicycle[currentEvent['pickUpStation'], dropOffStation]/60)/60 + currentEvent['time']

                dropOffEvent = NewEvent(nextEventTime, 3, currentEvent['pickUpStation'], math.inf, dropOffStation, currentEvent['requestLocation'], currentEvent['requestTime'], currentEvent['completedLocation'], math.inf)
                fullEventList = UpdatedEventList(fullEventList, dropOffEvent)
                EventList = UpdatedEventList(EventList, dropOffEvent)

                vehiclesAtStation[0,currentEvent['pickUpStation']] = vehiclesAtStation[0,currentEvent['pickUpStation']] -1
                parkingSpotsAtStation = capacityOfStation - vehiclesAtStation

            else:
                lostDemand = lostDemand + 1
                nbCustomersInTheSystem = nbCustomersInTheSystem -1

                cust = {
                    'time' : currentEvent['time'],
                    'number' : nbCustomersInTheSystem
                }

                nbCustomersTime.append(cust)
                print("The user has arrived to the station but at the time no vehicle is left.\n")
            #endif
        # endif for PICKUP

        if currentEvent['typeEvent'] == 3:  # DROPOFF event
            if parkingSpotsAtStation[0,currentEvent['dropOffStation']] > 0:
                nextEventTime = (LA.norm(stationLocations[currentEvent['dropOffStation']]-currentEvent['completedLocation'])*100)/walkingSpeed + currentEvent['time']
                completedEvent = NewEvent(nextEventTime, 4, currentEvent['pickUpStation'], math.inf, currentEvent['dropOffStation'], currentEvent['requestLocation'], currentEvent['requestTime'], currentEvent['completedLocation'], nextEventTime)
                fullEventList = UpdatedEventList(fullEventList, completedEvent)
                EventList = UpdatedEventList(EventList, completedEvent)

                vehiclesAtStation[0,currentEvent['dropOffStation']] = vehiclesAtStation[0,currentEvent['dropOffStation']] + 1
                parkingSpotsAtStation = capacityOfStation - vehiclesAtStation

                nbCustomersInTheSystem = nbCustomersInTheSystem - 1

                cust = {
                    'time' : currentEvent['time'],
                    'number' : nbCustomersInTheSystem
                }

                nbCustomersTime.append(cust)

            else:   # If no parking spots available when the user arrives, s/he chooses the next closest station to leave the vehicle. It is not possible to opt-out since s/he has to deliver the vehicle.
                print("The user has arrived to the station but at the time no parking spot is left.\n")
                for j in range(len(stationLocations)):
                    proximityHubs.append(LA.norm(stationLocations[j, :] - currentEvent['completedLocation']))

                distAssignedStation = proximityHubs[currentEvent['dropOffStation']]
                dropOffStation = 0

                while 1:
                    distAssignedStation = min(p for p in proximityHubs if p > distAssignedStation)
                    idxAssignedStation = proximityHubs.index(distAssignedStation)

                    if parkingSpotsAtStation[idxAssignedStation] > 0:
                        dropOffStation = idxAssignedStation
                        break
                    else:
                        print("Assign to another drop off station.\n")
                # endwhile

                if dropOffStation > 0:
                    # Trigger PICKUP event
                    nextEventTime = (c_baseTimeBicycle[dropOffStation, currentEvent['dropOffStation']]/60)/60 + currentEvent['time']

                    dropOffEvent = NewEvent(nextEventTime, 3, currentEvent['pickUpStation'], currentEvent['dropOffStation'], dropOffStation,
                                           currentEvent['requestLocation'], currentEvent['requestTime'],
                                           currentEvent['completedLocation'], math.inf)
                    fullEventList = UpdatedEventList(fullEventList, dropOffEvent)
                    EventList = UpdatedEventList(EventList, dropOffEvent)
                    currentEvent['prevDrop'] = currentEvent['dropOffStation']
                    currentEvent['dropOffStation'] = 0

                    fullEventList = UpdatedEventList(fullEventList, currentEvent)
                    print("The user tries the next dropoff station.\n")
                # endif

        # endif for DROPOFF

        if currentEvent['typeEvent'] == 4:  # COMPLETED event
            a=1
            # Do nothing
        # endif for COMPLETED
    #endwhile
    return fullEventList, availabilityTime, lostDemand, nbCustomersTime