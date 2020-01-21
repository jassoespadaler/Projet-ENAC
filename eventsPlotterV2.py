import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
from copy import deepcopy
def eventsPlotterV2(fullEventList, stationLocations, availabilityTime):
    stationLocations = np.fliplr(stationLocations)

    pauseOn = 1
    pauseTime = 0.000001

    fig = plt.figure()
    grid = plt.GridSpec(4,1, hspace=0.2, wspace=0.2)


    availability = deepcopy(availabilityTime)

    main_plt = fig.add_subplot( grid[0:3, 0] )

    plt.xlim(6.45, 6.7)
    plt.ylim(46.49, 46.56)


    avail_plot = fig.add_subplot(grid[-1,0], xticks = np.arange(len(stationLocations)+1), yticklabels = [], xlabel = "Station ID")

    # plt.gca().set_aspect('equal')

    main_plt.plot(stationLocations[:,0], stationLocations[:,1], 'r^')

    for i in range(len(stationLocations)):
        main_plt.text(stationLocations[i, 0], stationLocations[i, 1], ' St ' + str(i))


    main_plt.title.set_text('TIME = 0.0')
    avail_plot.title.set_text('CURRENT AVAILABILITY')
    if pauseOn:
        plt.pause(pauseTime)

    for i in range(len(fullEventList)):
        event = fullEventList[i]
        avail_plot.cla()
        currAv = availability[i]['avail'][0]
        currAvPlot = availability[i]['avail']

        c = avail_plot.pcolor(currAvPlot, vmin = 0, vmax = 30)
        for k in range(len(currAv)):
            avail_plot.text(k+0.25, 0.5, str(currAv[k]))

        if event['typeEvent'] == 1:     # REQUEST event
            main_plt.title.set_text("TIME = " + str(event['time']))

            main_plt.plot(event['requestLocation'][0], event['requestLocation'][1], color = 'red', marker = ".")
            main_plt.plot(event['completedLocation'][0], event['completedLocation'][1], color = 'green', marker = ".")

            if pauseOn:
                plt.pause(pauseTime)

        tempConnect = []
        if event['typeEvent'] == 2:     # PICKUP event
            tempConnect = stationLocations[event['pickUpStation']]

            x_ax = [tempConnect[0], event['requestLocation'][0]]
            y_ax = [tempConnect[1], event['requestLocation'][1]]

            main_plt.title.set_text("TIME = " + str(event['time']))
            main_plt.plot(x_ax, y_ax, color = 'cyan', linewidth = 0.5, linestyle = "-")

        if event['typeEvent'] == 3:  # DROPOFF event
            if event['prevDrop'] == math.inf and event['dropOffStation'] > 0:
                tempConnect = stationLocations[event['pickUpStation']]

                x_ax = [tempConnect[0], stationLocations[event['dropOffStation']][0]]
                y_ax = [tempConnect[1], stationLocations[event['dropOffStation']][1]]

                main_plt.title.set_text("TIME = " + str(event['time']))
                main_plt.plot(x_ax, y_ax, color = 'magenta', linewidth = 0.5, linestyle = ":")
                if pauseOn:
                    plt.pause(pauseTime)

            if event['prevDrop']!=math.inf and event['dropOffStation'] > 0:
                tempConnect = stationLocations[event['dropOffStation']]

                x_ax = [tempConnect[0], stationLocations[event['prevDrop']][0]]
                y_ax = [tempConnect[1], stationLocations[event['prevDrop']][1]]

                main_plt.title.set_text("TIME = " + str(event['time']))
                main_plt.plot(x_ax, y_ax, color = 'black', linewidth = 0.5, linestyle = "--")
                if pauseOn:
                    plt.pause(pauseTime)

        if event['typeEvent'] == 4:  # COMPLETED event
            tempConnect = event['completedLocation']

            x_ax = [tempConnect[0], stationLocations[event['dropOffStation']][0]]
            y_ax = [tempConnect[1], stationLocations[event['dropOffStation']][1]]

            main_plt.title.set_text("TIME = " + str(event['time']))
            main_plt.plot(x_ax, y_ax, color = 'blue', linewidth = 0.5, linestyle = "-.")
            if pauseOn:
                plt.pause(pauseTime)