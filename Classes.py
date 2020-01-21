import numpy as np
import math
import scipy.io as sio
import pandas as pd
import matplotlib.pyplot as plt
from NewEvent import NewEvent
from UpdatedEventList import UpdatedEventList
from basicConfiguration import basicConfiguration
from eventsPlotterV2 import eventsPlotterV2
from numpy import linalg as LA
from copy import deepcopy
from random import randrange
import time

class RebalancingOperations():
    def __init__(self, mtz: bool, vi: bool):
        self.mtz = mtz
        self.vi = vi
        self.data_dict = {}
        
    def getInputData(self, nSt: int, nTr: int, CapTr: int, desiredConfig: list, currentConfig: list):
        self.data_dict['N'] = nSt
        self.data_dict['m'] = nTr
        self.data_dict['Q'] = CapTr
        self.data_dict['V'] = nSt + 1
        l = currentConfig - desiredConfig
        self.data_dict['q'] = [int(x) for x in l]
        self.data_dict['q'].insert(0,0)
        if nSt == 35:
            from data_35_new import c
            self.data_dict['c'] = c
        elif nSt == 20:
            from data_20 import c
            self.data_dict['c'] = c
            
        #print(self.data_dict)
        return self.data_dict
    
    def Solve(self, input_dict: dict, TimeLimit: int):
        data = input_dict
        with open("output.txt", "w") as f:
            t_0 = time.time()
            t_1 = time.time()
            # Import the corresponding model
            if self.mtz == True and self.vi == True:
                from BSS_model_mtz_vi import getModel, solveModel
            elif self.mtz == True and self.vi == False:
                from BSS_model_mtz import getModel, solveModel
            elif self.mtz == False and self.vi == True:
                from BSS_model_dl_vi import getModel, solveModel                
            elif self.mtz == False and self.vi == False:
                from BSS_model_dl import getModel, solveModel
            
            #SOLVE MODEL
            model = getModel(f, data)
            model.parameters.timelimit.set(TimeLimit)
            results = solveModel(f, data, model)

            t_2 = time.time()

            print('\n -- TIMING -- ')
            print('Get data + Preprocess: %r sec' %(t_1 - t_0))
            print('Run the model: %r sec' %(t_2 - t_1))
            print('\n ------------ ')
                
        return results['Routing cost']
    
    
    
    
    
class Simulation():
    def __init__(self, nSt: int, FirstBikesPerStation: int):
        self.nSt = nSt
        self.BikesPerStation = FirstBikesPerStation

        self.lambdasTime = (20,20,20,20,20)                                  #tuple
        self.timePeriods = [[0,6],                                           #list
                       [6,9],
                       [9,16],
                       [16,20],
                       [20,24]]
        self.timeLimit = 24                                                  #int
        self.choose_rule = 0                                                 #int
        #self.choose_scenario = 1                                             #int
        self.numScenarios = 2
        
        self.c_trafficTimeCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='trafficTimeCar')
        self.c_baseTimeBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='baseTimeBicycle')
        self.c_distanceCar = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceCar')
        self.c_distanceBicycle = pd.read_excel(r'DistanceMatrix.xlsx', sheet_name='distanceBicycle')
        
        matContents = sio.loadmat('PubliBikeStationLocations.mat')
        self.stationLocations = matContents['PubliBikeStationLocations'] #ndarray  
        self.capacityOfStation = 200*np.ones((1,self.nSt))            #ndarray  
                
        if self.nSt == 20:
            selection_rows = [3,4,5,7,8,10,11,12,13,14,16,19,20,24,25,27,28,29,32,34]
            selection_columns = [x+1 for x in selection_rows]
            selection_columns.insert(0,0)
            
            self.stationLocations = self.stationLocations[selection_rows]
            
            self.c_trafficTimeCar = self.c_trafficTimeCar.iloc[selection_rows,selection_columns]
            self.c_baseTimeBicycle = self.c_baseTimeBicycle.iloc[selection_rows,selection_columns]
            self.c_distanceCar = self.c_distanceCar.iloc[selection_rows,selection_columns]
            self.c_distanceBicycle = self.c_distanceBicycle.iloc[selection_rows,selection_columns]
            print(self.c_baseTimeBicycle)
        
  
    def Simulate(self, InitialConfiguration: list, scenario: int):
        vehiclesAtStation = np.array([InitialConfiguration])
        #print('scenario', scenario)
        matContentsFileName = 'randomScenario' + str(scenario+1) + '.mat'
        matContents = sio.loadmat(matContentsFileName)

        dropOffLocations = matContents['dropOffLocations']
        pickUpLocations = matContents['pickUpLocations']
        times = matContents['times']
        #lostDemand1 = matContents['lostDemand1']
        #finalStationConfig = matContents['finalStationConfig']
    
        ## Simulate the system with basic configuration
        # The demand for a vehicle and parking spot are generated randomly in the
        # city (without any information on urban and rural areas and the dynamics
        # of the city). 

        # The REQUEST event is generated, which triggers a PICKUP event (This event assigns the request to the closest station having available 
        # vehicles at the moment. If there are no available vehicles within the 300m circle of the requestLocation,
        # the customer opts out.). The user is assumed to walk from the requestLocation to pickUpLocation. If there are no vehicles available
        # at the station when the customer arrives, s/he opts out.

        # In the case of available vehicle, the user starts the journey. This triggers the event DROPOFF. The availability of a parking spot
        # is not checked in advance. When the user arrives to the closest station, and cannot find a parking spot,
        # s/he goes to the next closest station. This triggers another DROPOFF event and a DROPOFF-REDIRECTED event for the DROPOFF that could
        # not be executed. Since the user has to park the vehicle, s/he looks for a place until s/he finds.
        # There is no opt-out option at this point.

        # When the user finds a parking spot, s/he parks the vehicle and walks to the completedLocation which is handled by the last event
        # type COMPLETED.

        #print(vehiclesAtStation)   
        fullEventList1, availabilityTime1, lostDemand1, nbCustomersTime1 = basicConfiguration(pickUpLocations, dropOffLocations, times, 
                                                                                                  vehiclesAtStation, self.capacityOfStation, 
                                                                                                  self.stationLocations, self.c_baseTimeBicycle, 
                                                                                                  self.c_trafficTimeCar, self.c_distanceCar, 
                                                                                                  self.c_distanceBicycle)
        #print(availabilityTime1, lostDemand1,nbCustomersTime1)
        #print(vehiclesAtStation)
        #print(sum(availabilityTime1[-1]['avail'][0]))
        return availabilityTime1[-1]['avail'][0], lostDemand1
    
    def EstimateConfigIni(self, scenario: int):
        
        matContentsFileName = 'randomScenario' + str(scenario+1) + '.mat'
        matContents = sio.loadmat(matContentsFileName)

        dropOffLocations = matContents['dropOffLocations']
        pickUpLocations = matContents['pickUpLocations']
        times = matContents['times']
        #lostDemand1 = matContents['lostDemand1']
        #finalStationConfig = matContents['finalStationConfig']
        
        stationLocations1 = np.fliplr(self.stationLocations)
        IdxPickUps = []
        IdxDropOffs = []
        
        for i in range(len(pickUpLocations)):
            proxPickUps = []
            proxDropOffs = []
            
            for j in range(len(stationLocations1)):
                proxPickUps.append(LA.norm(stationLocations1[j,:]-pickUpLocations[i,:]))
                proxDropOffs.append(LA.norm(stationLocations1[j,:]-dropOffLocations[i,:]))
                
            mindist_pu = min(p for p in proxPickUps)
            mindist_do = min(p for p in proxDropOffs)
            idx_pu = proxPickUps.index(mindist_pu)
            idx_do = proxDropOffs.index(mindist_do)
            
            IdxPickUps.append(idx_pu)
            IdxDropOffs.append(idx_do)
            
        
        valuespu, countspu = np.unique(IdxPickUps, return_counts=True)
        valuesdo, countsdo = np.unique(IdxDropOffs, return_counts=True)
            
        pickups1 = {}                
        dropoffs1 = {}
        balance1 = {}  
        
        for k in range(self.nSt):
            if k in valuespu:
                pickups1[k] = countspu[valuespu == k][0]
            else: 
                pickups1[k] = 0
            if k in valuesdo:
                dropoffs1[k] = countsdo[valuesdo == k][0]
            else: 
                dropoffs1[k] = 0

        for j in range(self.nSt):
            balance1[j] = pickups1[j] - dropoffs1[j]
        balance = list(balance1.values())
        
        balance_pos = [x-min(balance) for x in balance]
        proportions = [x / sum(balance_pos) for x in balance_pos]
        TotalBikes = self.nSt*self.BikesPerStation
        
        EstimConfig1 = [x*TotalBikes for x in proportions]
        EstimConfig = [int(0.0) if i < 0 else int(np.round(i)) for i in EstimConfig1]

        while sum(EstimConfig) != self.nSt*self.BikesPerStation:
            aux = randrange(self.nSt)
            if sum(EstimConfig) > self.nSt*self.BikesPerStation:
                EstimConfig[aux] = EstimConfig[aux]-1
            else:
                EstimConfig[aux] = EstimConfig[aux]+1

        
        return EstimConfig
        
        
