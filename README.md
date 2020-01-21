# Projet ENAC: Analysis of the value of demand forecasting within vehicle sharing systems

The repository contains all the codes used for the project *Analysis of the value of demand forecasting within vehicle sharing systems*. In addition, the final report and presentation are also included.

## Report and presentation
* Report: Final_Report.pdf
* Presentation: Final_Presentation.pdf

## Python files:
Important note: this project uses the Python API of CPLEX.
* Bridge.py: main file to run.
 
### Rebalancing operations
* BSS_model_X_Y.py: rebalancing models (X: MTZ or DL, Y: vi or nothing).
* Classes.py, vi_subsets.py: additional files to store auxiliary classes and functions.

### Simulation
* randomScenarioX.mat: random simulation scenarios
* DistanceMatrix.xlsx: distance matrix of the network
* basicConfiguration.py, eventsPlotterV2.py, NewEvent.py, UpdatedEventList.py: files to run the simulation
