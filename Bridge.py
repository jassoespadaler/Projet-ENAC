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
NumberOfTrucks = 6                         # Number of repositioning trucks
TruckCapacity = 40                         # Capacity of each repositioning truck
UseMTZ = True                              # MTZ constraints or DL
ValidInequalities = True                   # Use of a model with valid inequalities
InitialNoOfBikesPerStation = 5             # Number of bikes at the beginning in each station
NumberOfDays = 3                            # Number of days to repeat the simulation (max9)
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
Trucks = []

#Main loop

demands = ['Unknown', 'Known']

for i in range(NumberOfDays):
    j = randrange(10)    #today's random scenario
    jj = randrange(10)   #tomorrow's random scenario
    
    for k in [2,4,NumberOfTrucks]:
        Trucks.append(k)

        for demand_is in demands:

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
                data_dict = Rebalancing.getInputData(nSt = NumberOfStations, nTr = k,
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
                ConfigNextDay = Simulation.EstimateConfigIni(jj)
                data_dict = Rebalancing.getInputData(nSt = NumberOfStations, nTr = k,
                                                     CapTr = TruckCapacity, desiredConfig = ConfigNextDay, currentConfig = ConfigFin)
                t1_reb = time.time()
                KnownCost.append(Rebalancing.Solve(data_dict, TimeLimit))  
                t2_reb = time.time()
                KnownRebTime.append(round(t2_reb-t1_reb,2))                  

t2 = time.time()
#Print the results

idx2 = [i for i, e in enumerate(Trucks) if e == 2]
idx4 = [i for i, e in enumerate(Trucks) if e == 4]
idx6 = [i for i, e in enumerate(Trucks) if e == 6]

UnknownCost2= [UnknownCost[i] for i in idx2]
UnknownCost4= [UnknownCost[i] for i in idx4]
UnknownCost6= [UnknownCost[i] for i in idx6]
KnownCost2= [KnownCost[i] for i in idx2]
KnownCost4= [KnownCost[i] for i in idx4]
KnownCost6= [KnownCost[i] for i in idx6]

print('Unknown demand: Cost of rebalancing operations with 2 trucks: \n', UnknownCost2)
print('Unknown demand: Cost of rebalancing operations with 4 trucks: \n', UnknownCost4)
print('Unknown demand: Cost of rebalancing operations with 6 trucks: \n', UnknownCost6)
print('Known demand: Cost of rebalancing operations with 2 trucks: \n', KnownCost2)
print('Known demand: Cost of rebalancing operations with 4 trucks: \n', KnownCost4)
print('Known demand: Cost of rebalancing operations with 6 trucks: \n', KnownCost6)

UnknownLostDem = [UnknownLostDemandList[i] for i in idx2]
KnownLostDem = [KnownLostDemandList[i] for i in idx2]

print('Unknown demand: Lost demand during the day: \n', UnknownLostDem)
print('Known demand: Lost demand during the day: \n', KnownLostDem)

UnknownIni = [UnknownConfigIniList[i] for i in idx2]
UnknownFin = [UnknownConfigFinList[i] for i in idx2]
KnownIni = [KnownConfigIniList[i] for i in idx2]
KnownFin = [KnownConfigFinList[i] for i in idx2]

print('Unknown demand: Initial configurations:')
for count, list in enumerate(UnknownIni):
    print('Day '+str(count)+':', list)

print('Unknown demand: Final configurations:') 
for count, list in enumerate([l.tolist() for l in UnknownFin]):
    print('Day '+str(count)+':', [int(x) for x in list])

print('Known demand: Initial configurations:')
for count, list in enumerate(KnownIni):
    print('Day '+str(count)+':', list)
    
print('Known demand: Final configurations:') 
for count, list in enumerate([l.tolist() for l in KnownFin]):
    print('Day '+str(count)+':', [int(x) for x in list])
    
print('Unknown demand: Simulation times: \n', UnknownSimTime)
print('Unknown demand: Rebalancing times: \n', UnknownRebTime)
print('Known demand: Simulation times: \n', KnownSimTime)
print('Known demand: Rebalancing times: \n', KnownRebTime)


    
days = [x for x in range(NumberOfDays)]
totaltime = round(t2-t1,2)


plt.plot(days, UnknownCost2, 'bx-')
plt.plot(days, KnownCost2, 'bx--')
plt.plot(days, UnknownCost4, 'bo-')
plt.plot(days, KnownCost4, 'bo--')
plt.plot(days, UnknownCost6, 'bd-')
plt.plot(days, KnownCost6, 'bd--')
yint = []
locs, labels = plt.yticks()
for each in locs:
    yint.append(int(each))
plt.yticks(yint)
xint = []
locs, labels = plt.xticks()
for each in locs:
    xint.append(int(each))
plt.xticks(xint)
plt.xlabel('Day')
plt.ylabel('Rebalancing cost')
plt.xlim(-1,NumberOfDays)
plt.legend(('2 trucks: unknown', '2 trucks: known','4 trucks: unknown', '4 trucks: known','6 trucks: unknown', '6 trucks: known' ),
           loc='center left', bbox_to_anchor=(1, 0.5))
plt.title('Rebalancing costs for different trucks')
plt.show()



plt.plot(days, UnknownLostDem, 'b-')
plt.plot(days, KnownLostDem, 'b--')
plt.xlabel('Day')
plt.ylabel('Lost demand')
yint = []
locs, labels = plt.yticks()
for each in locs:
    yint.append(int(each))
plt.yticks(yint)
xint = []
locs, labels = plt.xticks()
for each in locs:
    xint.append(int(each))
plt.xticks(xint)
plt.title('Lost demand')
plt.xlim(-1,NumberOfDays)
plt.legend(('Unknown demand','Known demand'),
           loc='upper right')
plt.show()



plt.fig, ax = plt.subplots(1,3, sharex=False, sharey = False)
ax[0].scatter(UnknownCost2[:-1], UnknownLostDem[1:], marker = 'x', color = 'b')
ax[0].scatter(KnownCost2[:-1], KnownLostDem[1:], marker = 'o', color = 'b')
ax[0].set_title('2 trucks')
ax[0].set_ylabel('Lost demand')
ax[0].set_xlabel('Rebalancing cost')
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].legend(('Unknown', 'Known'), loc='upper right')

ax[1].scatter(UnknownCost4[:-1], UnknownLostDem[1:], marker = 'x', color = 'b')
ax[1].scatter(KnownCost4[:-1], KnownLostDem[1:], marker = 'o', color = 'b')
#ax[1].scatter(KnownCost6, KnownLostDem, marker = 'd', color = 'b')
ax[1].set_title('4 trucks')
ax[1].set_ylabel('Lost demand')
ax[1].set_xlabel('Rebalancing cost')
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].legend(('Unknown', 'Known'), loc='upper right')
              
ax[2].scatter(UnknownCost6[:-1], UnknownLostDem[1:], marker = 'x', color = 'b')   
ax[2].scatter(KnownCost6[:-1], KnownLostDem[1:], marker = 'o', color = 'b')
ax[2].set_title('6 trucks')
ax[2].set_ylabel('Lost demand')
ax[2].set_xlabel('Rebalancing cost')
ax[2].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[2].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[2].legend(('Unknown', 'Known'), loc='upper right')              
              
#plt.suptitle('Stations: ' + str(NumberOfStations) + ', Capacity: ' + str(TruckCapacity) + ', Time: ' + str(totaltime))
plt.show() 


'''
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

markers = []
for kk in Trucks:
    if kk == 3:
        markers.append('x')
    elif kk == 4:
        markers.append('o')
    elif kk == 5:
        markers.append('s')
    elif kk == 6:
        markers.append('d')
        

plt.scatter(UnknownCost, UnknownLostDemandList,marker = markers,color = 'b')
plt.scatter(KnownCost, KnownLostDemandList,marker = markers, color = 'r')
plt.legend(('Unknown demand', 'Known demand'),
           loc='upper right')
plt.show()


plt.fig, ax = plt.subplots(1,2)
for i in range(len(Trucks)):
    ax[0].scatter(UnknownCost[i], UnknownLostDemandList[i], marker = markers[i])
    ax[1].scatter(KnownCost[i], KnownLostDemandList[i], marker = markers[i])
ax[0].set_title('Unknown demand')
ax[0].set_ylabel('Lost demand')
ax[0].set_xlabel('Rebalancing cost')
ax[0].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].set_title('Known demand')
ax[1].set_ylabel('Lost demand')
ax[1].set_xlabel('Rebalancing cost')
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
plt.suptitle('Stations: ' + str(NumberOfStations) + ', Capacity: ' + str(TruckCapacity) + ', Time: ' + str(totaltime))
plt.show() 
'''