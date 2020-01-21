import numpy as np
import math
import scipy.io as sio
import pandas as pd
import matplotlib.pyplot as plt
from NewEvent import NewEvent
from UpdatedEventList import UpdatedEventList
from basicConfiguration import basicConfiguration
from eventsPlotterV2 import eventsPlotterV2

lambdasTime = (20,20,20,20,20)                                  #tuple
timePeriods = [[0,6],                                           #list
               [6,9],
               [9,16],
               [16,20],
               [20,24]]
timeLimit = 24                                                  #int

choose_rule = 0                                                 #int
choose_scenario = 2                                             #int

numScenarios = 1

if choose_scenario == 1:
    numStations = 35                                            #int
    vehiclesAtStation = 5*np.ones((1,numStations))              #ndarray
    capacityOfStation = 200*np.ones((1,numStations))            #ndarray
    initialStationConfig = vehiclesAtStation                    #ndarray
    matContents = sio.loadmat('PubliBikeStationLocations.mat')  #dict
    stationLocations = matContents['PubliBikeStationLocations'] #ndarray

    c_trafficTimeCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='trafficTimeCar')
    c_baseTimeBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='baseTimeBicycle')
    c_distanceCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceCar')
    c_distanceBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceBicycle')

if choose_scenario == 2:
    numStations = 20                                            # int
    vehiclesAtStation = 5 * np.ones((1, numStations))           # ndarray
    capacityOfStation = 200 * np.ones((1, numStations))         # ndarray
    initialStationConfig = vehiclesAtStation                    # ndarray
    matContents = sio.loadmat('PubliBikeStationLocations.mat')  # dict
    stationLocations = matContents['PubliBikeStationLocations'] # ndarray
    
    c_trafficTimeCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='trafficTimeCar')
    c_baseTimeBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='baseTimeBicycle')
    c_distanceCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceCar')
    c_distanceBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceBicycle')
    
    selection = [2,3,4,5,7,8,10,11,12,14,16,19,20,24,25,27,28,29,32,34]
    stationLocations = stationLocations[selection]
    c_trafficTimeCar = c_trafficTimeCar.iloc[selection,selection]
    c_baseTimeBicycle = c_baseTimeBicycle.iloc[selection,selection]
    c_distanceCar = c_distanceCar.iloc[selection,selection]
    c_distanceBicycle = c_distanceBicycle.iloc[selection,selection] 
    # Do the same thing but eliminate some of the stations.
    # [3:6, 8:9, 11:13, 15, 17, 20, 21, 25:26, 28:30, 33, 35] These indices should be in the final station list. Notice that this is from MATLAB. Therefore, the indices should be one less each time.

for scenario in range(0, numScenarios):
    print('scenario',scenario)
    matContentsFileName = 'randomScenario' + str(scenario+1) + '.mat'
    matContents = sio.loadmat(matContentsFileName)

    # a = matContents['availabilityTime1']
    # b = a[0,0][0][0][0]                             # availabilityTime1 : time information              #float64
    # c = a[0,0][1]                                   # availabilityTime1 : availability at each station  #ndarray
    # matContents['availabilityTime1']                # https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
    dropOffLocations = matContents['dropOffLocations']
    pickUpLocations = matContents['pickUpLocations']
    times = matContents['times']
    lostDemand1 = matContents['lostDemand1']
    finalStationConfig = matContents['finalStationConfig']
    print('HALLLLLLLOOOOOOO:')
    print(lostDemand1)
    print(finalStationConfig)
    # availabilirtyTime1
    # fullEventList1
    # nbCustomersTime1

    # Plot the order generation
    plt.scatter(pickUpLocations[:, 0], pickUpLocations[:, 1], color='orange', marker='x', label='pickUp')
    plt.scatter(dropOffLocations[:, 0], dropOffLocations[:, 1], color='blue', marker='o', label='dropOff')
    #plt.scatter(stationLocations[:, 1], stationLocations[:, 0], color='black', marker='s', label='stations')
    plt.legend()
    #plt.show()

    ## Simulate the system with basic configuration
    # The demand for a vehicle and parking spot are generated randomly in the
    # city (without any information on urban and rural areas and the dynamics
    # of the city). 

    # The REQUEST event is generated, which triggers a PICKUP event (This event assigns the request to the closest station having available vehicles at the moment. If there are no available vehicles within the 300m circle of the requestLocation,
    # the customer opts out.). The user is assumed to walk from the requestLocation to pickUpLocation. If there are no vehicles available at the station when the customer arrives, s/he opts out.

    # In the case of available vehicle, the user starts the journey. This triggers the event DROPOFF. The availability of a parking spot is not checked in advance. When the user arrives to the closest station, and cannot find a parking spot,
    # s/he goes to the next closest station. This triggers another DROPOFF event and a DROPOFF-REDIRECTED event for the DROPOFF that could not be executed. Since the user has to park the vehicle, s/he looks for a place until s/he finds.
    # There is no opt-out option at this point.

    # When the user finds a parking spot, s/he parks the vehicle and walks to the completedLocation which is handled by the last event type COMPLETED.

    # event1 = NewEvent(1, 1, 1, 1, 1, 1, 1, 1, 1)
    # event2 = NewEvent(2, 2, 2, 2, 2, 2, 2, 2, 2)
    # event3 = NewEvent(3, 3, 3, 3, 3, 3, 3, 3, 3)
    
    # EventList = [event1, event3]
    # EventList = UpdatedEventList(EventList, event2)

    print(vehiclesAtStation)
    fullEventList1, availabilityTime1, lostDemand1, nbCustomersTime1 = basicConfiguration(pickUpLocations, dropOffLocations, times, vehiclesAtStation, capacityOfStation, stationLocations, c_baseTimeBicycle, c_trafficTimeCar, c_distanceCar, c_distanceBicycle)

    #eventsPlotterV2(fullEventList1, stationLocations, availabilityTime1)
    print(vehiclesAtStation)
    print(availabilityTime1[-1]['avail'][0])
    print(lostDemand1)
