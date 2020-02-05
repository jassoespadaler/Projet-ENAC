## Inputs
import sys
import time
import copy
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from random import randrange

from Classes import RebalancingOperations, Simulation

#Choices:
#demand_is = 'Unknown'                     # 'Unknown' or 'Known'
NumberOfStations = 35                      # keep it to 35 for the moment
NumberOfTrucks = 4                         # Number of repositioning trucks
TruckCapacity = 23                         # Capacity of each repositioning truck
UseMTZ = True                              # MTZ constraints or DL
ValidInequalities = True                   # Use of a model with valid inequalities
InitialNoOfBikesPerStation = 5             # Number of bikes at the beginning in each station
NumberOfDays =  5                          # Number of days to repeat the simulation (max9)
TimeLimit = 1e75                              # Maximum seconds to solve the rebalancing model

#Initialise the Rebalancing Operations and simulation classes:
t1 = time.time()
Rebalancing = RebalancingOperations(mtz = UseMTZ, vi = ValidInequalities)
Simulation = Simulation(nSt = NumberOfStations, FirstBikesPerStation = InitialNoOfBikesPerStation )

#Initialise the results lists
UnknownCost = []
UnknownLostDemandList = []
UnknownConfigIniList = []
UnknownConfigFinList = []
UnknownSimTime = []
UnknownRebTime = []
KnownCost = []
KnownLostDemandList = []
KnownConfigIniList = []
KnownConfigFinList = []
KnownSimTime = []
KnownRebTime = []

#Main loop (two cases: unknown or known demand)

demands = ['Unknown', 'Known']

j = randrange(10)
for i in range(NumberOfDays):

    for demand_is in demands:

        #Choose a random scenario of the 10 possible

        if demand_is == 'Unknown':

            ConfigIni = [InitialNoOfBikesPerStation]*NumberOfStations

            #Simulation
            t1_sim = time.time()
            ConfigFin, LostDemand =  Simulation.Simulate(InitialConfiguration = ConfigIni, scenario = j)
            t2_sim = time.time()
            
            UnknownSimTime.append(round(t2_sim-t1_sim,2))
            UnknownConfigIniList.append(ConfigIni)
            UnknownConfigFinList.append(ConfigFin)
            UnknownLostDemandList.append(LostDemand)

            #Rebalancing operations
            data_dict = Rebalancing.getInputData(nSt = NumberOfStations, nTr = NumberOfTrucks,
                                                 CapTr = TruckCapacity, desiredConfig = ConfigIni, currentConfig = ConfigFin)
            t1_reb = time.time()
            UnknownCost.append(Rebalancing.Solve(data_dict, TimeLimit))
            t2_reb = time.time()
            UnknownRebTime.append(round(t2_reb-t1_reb,2))            

        elif demand_is == 'Known':

            #Estimate Configuration of the day based on the popularity of the stations forecasted
            ConfigIni = Simulation.EstimateConfigIni(j)

            #Simulation
            t1_sim = time.time()
            ConfigFin, LostDemand = Simulation.Simulate(InitialConfiguration = ConfigIni, scenario = j)
            t2_sim = time.time()

            KnownSimTime.append(round(t2_sim-t1_sim,2))
            KnownConfigIniList.append(ConfigIni) 
            KnownConfigFinList.append(ConfigFin)
            KnownLostDemandList.append(LostDemand) 

            #Rebalancing operations
            j = randrange(10)
            ConfigNextDay = Simulation.EstimateConfigIni(jj)
            data_dict = Rebalancing.getInputData(nSt = NumberOfStations, nTr = NumberOfTrucks,
                                                 CapTr = TruckCapacity, desiredConfig = ConfigNextDay, currentConfig = ConfigFin)
            t1_reb = time.time()
            KnownCost.append(Rebalancing.Solve(data_dict, TimeLimit))  
            t2_reb = time.time()
            KnownRebTime.append(round(t2_reb-t1_reb,2))                  

t2 = time.time()
#Print the results
print('Unknown demand: Cost of rebalancing operations: \n', UnknownCost)
print('Known demand: Cost of rebalancing operations: \n', KnownCost)
print('Unknown demand: Lost demand during the day: \n', UnknownLostDemandList)
print('Known demand: Lost demand during the day: \n', KnownLostDemandList)

print('Unknown demand: Initial configurations:')
for count, list in enumerate(UnknownConfigIniList):
    print('Day '+str(count)+':', list)

print('Unknown demand: Final configurations:') 
for count, list in enumerate([l.tolist() for l in UnknownConfigFinList]):
    print('Day '+str(count)+':', [int(x) for x in list])

print('Known demand: Initial configurations:')
for count, list in enumerate(KnownConfigIniList):
    print('Day '+str(count)+':', list)
    
print('Known demand: Final configurations:') 
for count, list in enumerate([l.tolist() for l in KnownConfigFinList]):
    print('Day '+str(count)+':', [int(x) for x in list])

    

days = [x for x in range(NumberOfDays)]
totaltime = round(t2-t1,2)

plt.fig, ax = plt.subplots(1,2)
ax[0].plot(days, UnknownCost, 'b-')
ax[0].plot(days, KnownCost,'b--')
ax[0].set_title('Rebalancing costs')
ax[0].set_ylabel('Distance')
ax[0].set_xlabel('Days')
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].legend(('Unknown demand', 'Known demand'),
           loc='upper right')
ax[1].plot(days, UnknownLostDemandList, 'b-')
ax[1].plot(days, KnownLostDemandList, 'b--')
ax[1].set_title('Lost demand')
ax[1].set_ylabel('Customers lost')
ax[1].set_xlabel('Days')
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].legend(('Unknown demand', 'Known demand'),
           loc='upper right')
plt.suptitle('Stations: ' + str(NumberOfStations) + ', Number of trucks: '+ str(NumberOfTrucks) + ', Capacity: ' + str(TruckCapacity) + ', Time: ' + str(totaltime))
plt.show()   



length = len(UnknownSimTime)
UnknownTotal = [UnknownSimTime[i] + UnknownRebTime[i] for i in range(length)]
KnownTotal = [KnownSimTime[i] + KnownRebTime[i] for i in range(length)]
prop_u_sim = [100*UnknownSimTime[i]/UnknownTotal[i] for i in range(length)]
prop_u_reb = [100*UnknownRebTime[i]/UnknownTotal[i] for i in range(length)]
prop_k_sim = [100*KnownSimTime[i]/KnownTotal[i] for i in range(length)]
prop_k_reb = [100*KnownRebTime[i]/KnownTotal[i] for i in range(length)]



plt.fig, ax = plt.subplots(1,3)
ax[0].plot(days, UnknownSimTime, 'b-')
ax[0].plot(days, KnownSimTime, 'b--')
ax[0].set_title('Simulation')
ax[0].set_ylabel('Time (sec)')
ax[0].set_xlabel('Days')
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].legend(('Unknown demand', 'Known demand'),
           loc='upper right')
ax[1].plot(days, UnknownRebTime, 'b-')
ax[1].plot(days, KnownRebTime, 'b--')
ax[1].set_title('Rebalancing operations')
ax[1].set_ylabel('Time (sec)')
ax[1].set_xlabel('Days')
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].legend(('Unknown demand', 'Known demand'),
           loc='upper right')

ax[2].plot(days, prop_u_sim, 'b-')
ax[2].plot(days, prop_k_sim, 'r-')
ax[2].plot(days, prop_u_reb, 'b--')
ax[2].plot(days, prop_k_reb, 'r--')
ax[2].set_title('Percentages of time')
ax[2].set_ylabel('Proportion')
ax[2].set_xlabel('Days')
ax[2].set_ylim(0,100)
ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[2].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[2].legend(('Unknown simulation', 'Known simulation','Unknown rebalancing', 'Known rebalancing'),
           loc='upper right')
plt.suptitle('Stations: ' + str(NumberOfStations) + ', Number of trucks: '+ str(NumberOfTrucks) + ', Capacity: ' + str(TruckCapacity) + ', Time: ' + str(totaltime))
plt.show()   


plt.scatter(UnknownCost, UnknownLostDemandList,marker = 'x')
plt.scatter(KnownCost, KnownLostDemandList,marker = 'o')
plt.ylabel('Lost demand')
plt.xlabel('Rebalancing cost')
plt.legend(('Unknown demand', 'Known demand'),
           loc='upper right')
plt.show()