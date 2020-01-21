# General
import sys
import time
import copy
import warnings
import numpy as np

# CPLEX
import cplex
from cplex.exceptions import CplexSolverError

# Models

# Data
#Import all the variables
#from data_20 import *
#from Converter_txt_2_py import *

#Create a dictionary with all the imported variables
'''
data_file = {}
data_file['N'] = N      #stations
data_file['m'] = m      #number of trucks
data_file['Q'] = Q      #capacity of trucks
data_file['c'] = c      #cost matrix (VxV)
data_file['q'] = q      #demands (1xV)
data_file['V'] = N+1    #stations+depot
'''      

def getModel(f, data):
    ''' Construct a CPLEX model
        Returns:
            model          CPLEX model
    '''

    t_in = time.time()
    # Initialize the model
    model = cplex.Cplex()


    ##########################################
    ##### ----- OBJECTIVE FUNCTION ----- #####
    ##########################################

    # Set the objective function sense
    model.objective.set_sense(model.objective.sense.minimize)


    ##########################################
    ##### ----- DECISION VARIABLES ----- #####
    ##########################################

    # BATCH OF BINARY VARIABLE ON ARC USAGE
    objVar = []
    typeVar = []
    nameVar = []

    # Binary variables on arc usage x(ij)
    for i in range(data['N']+1):
        for j in range(data['N']+1):
            objVar.append(data['c'][i][j])
            typeVar.append(model.variables.type.binary)
            nameVar.append('x[' + str(i) + ']' + '[' + str(j) + ']')

    model.variables.add(obj = [objVar[i] for i in range(len(objVar))],
                        types = [typeVar[i] for i in range(len(typeVar))],
                        names = [nameVar[i] for i in range(len(nameVar))])


    # BATCH OF MTZ AUXILIARY VARIABLES
    typeVar = []
    nameVar = []
    lbVar = []
    ubVar = []

    # Auxiliary variables MTZ (order in the tour)
    for i in range(1,data['N']+1):
        typeVar.append(model.variables.type.continuous)
        nameVar.append('u[' + str(i) +']')
        lbVar.append(1.0)
        ubVar.append(data['N'])

    model.variables.add(types = [typeVar[i] for i in range(len(typeVar))],
                        lb = [lbVar[i] for i in range(len(typeVar))],
                        ub = [ubVar[i] for i in range(len(typeVar))],
                        names = [nameVar[i] for i in range(len(nameVar))])


    # BATCH OF THETA AUXILIARY VARIABLES
    typeVar = []
    nameVar = []
    lbVar = []
    ubVar = []
    
    #Theta or the load of the vehicle after visiting every node
    for i in range(data['N']+1):
        typeVar.append(model.variables.type.continuous)
        nameVar.append('o[' + str(i) +']')
        lbVar.append(max(0,data['q'][i]))
        ubVar.append(min(data['Q'],data['Q']+data['q'][i]))
        
    model.variables.add(types = [typeVar[i] for i in range(len(typeVar))],
                        lb = [lbVar[i] for i in range(len(typeVar))],
                        ub = [ubVar[i] for i in range(len(typeVar))],
                        names = [nameVar[i] for i in range(len(nameVar))])
        
    

    print('CPLEX model: all decision variables added. N variables: %r. Time: %r'\
          %(model.variables.get_num(), round(time.time()-t_in,2)))

    # Creating a dictionary that maps variable names to indices, to speed up constraints creation
    # https://www.ibm.com/developerworks/community/forums/html/topic?id=2349f613-26b1-4c29-aa4d-b52c9505bf96
    nameToIndex = { n : j for j, n in enumerate(model.variables.get_names()) }



    #########################################
    ##### -------- CONSTRAINTS -------- #####
    #########################################

    ###################################################
    ### --- Routing constraints --- ###
    ###################################################

    indicesConstr = []
    coefsConstr = []
    sensesConstr = []
    rhsConstr = []
    
    #Each node must be visited once, arrival at the node
    for j in range(1,data['N']+1):
        ind = []
        co = []
        for i in range(data['N']+1):
            ind.append(nameToIndex['x[' + str(i) + ']' + '[' + str(j) + ']'])
            co.append(1.0)
        indicesConstr.append(ind)
        coefsConstr.append(co)
        sensesConstr.append('E')
        rhsConstr.append(1.0)

    #Each node must be visited once, departure of the node
    for j in range(1,data['N']+1):
        ind = []
        co = []
        for i in range(data['N']+1):
            ind.append(nameToIndex['x[' + str(j) + ']' + '[' + str(i) + ']'])
            co.append(1.0)
        indicesConstr.append(ind)
        coefsConstr.append(co)
        sensesConstr.append('E')
        rhsConstr.append(1.0)   
        
    #xii must be 0 to avoid all possible subtours
    for i in range(data['N']+1):
        indicesConstr.append([nameToIndex['x[' + str(i) + ']' + '[' + str(i) + ']']])
        coefsConstr.append([1.0])
        sensesConstr.append('E')
        rhsConstr.append(0.0)      
        
    #theta 0 must be 0 
    #indicesConstr.append([nameToIndex['o[' + str(1) +']']])
    #coefsConstr.append([1.0])
    #sensesConstr.append('E')
    #rhsConstr.append(0.0)            
        
    #A maximum of m trucks can leave the depot  
    ind = []
    co = []
    for j in range(data['N']+1):
        ind.append(nameToIndex['x[' + str(0) + ']' + '[' + str(j) + ']'])
        co.append(1.0)
    indicesConstr.append(ind)
    coefsConstr.append(co)
    sensesConstr.append('L')
    rhsConstr.append(data['m'])
    
    #All trucks must return to the depot
    ind = []
    co = []
    for j in range(1,data['N']+1):
        ind.append(nameToIndex['x[' + str(0) + ']' + '[' + str(j) + ']'])
        ind.append(nameToIndex['x[' + str(j) + ']' + '[' + str(0) + ']'])
        co.append(1.0)
        co.append(-1.0)
    indicesConstr.append(ind)
    coefsConstr.append(co)
    sensesConstr.append('E')
    rhsConstr.append(0.0)

    model.linear_constraints.add(lin_expr = [[indicesConstr[i], coefsConstr[i]] for i in range(len(indicesConstr))],
                                 senses = [sensesConstr[i] for i in range(len(sensesConstr))],
                                 rhs = [rhsConstr[i] for i in range(len(rhsConstr))])


    #####################################################
    ##### ----- Subtour elimination constraints ---- ####
    #####################################################

    indicesConstr = []
    coefsConstr = []
    sensesConstr = []
    rhsConstr = []

    # MTZ constraints
    for i in range(1,data['N']+1):
        for j in range(1,data['N']+1):
            if i != j:
                indicesConstr.append([nameToIndex['u[' + str(i) + ']'], nameToIndex['u[' + str(j) + ']'], 
                                      nameToIndex['x[' + str(i) + ']' + '[' + str(j) + ']'], 
                                      nameToIndex['x[' + str(j) + ']' + '[' + str(i) + ']']])
                coefsConstr.append([1.0, -1.0, data['N'], data['N']-2])
                sensesConstr.append('L')
                rhsConstr.append(data['N']-1)

    model.linear_constraints.add(lin_expr = [[indicesConstr[i], coefsConstr[i]] for i in range(len(indicesConstr))],
                                 senses = [sensesConstr[i] for i in range(len(sensesConstr))],
                                 rhs = [rhsConstr[i] for i in range(len(rhsConstr))])                
                

    #####################################################
    ##### ----- Demand satisfaction constraints ---- ####
    #####################################################
            
    indicesConstr = []
    coefsConstr = []
    sensesConstr = []
    rhsConstr = []
    
    # Big M method
    for i in range(data['N']+1):
        for j in range(1,data['N']+1):
            if i != j:
                M = min(data['Q'],data['Q']+data['q'][j])
                indicesConstr.append([nameToIndex['o[' + str(j) + ']'], nameToIndex['o[' + str(i) + ']'],
                                  nameToIndex['x[' + str(i) + ']' + '[' + str(j) + ']']])
                coefsConstr.append([1.0, -1.0, -M])
                sensesConstr.append('G')
                rhsConstr.append(data['q'][j] - M)
        
    for i in range(1,data['N']+1):
        for j in range(data['N']+1):
            if i != j:
                M = min(data['Q'],data['Q']-data['q'][j])
                indicesConstr.append([nameToIndex['o[' + str(i) + ']'], nameToIndex['o[' + str(j) + ']'],
                                      nameToIndex['x[' + str(i) + ']' + '[' + str(j) + ']']])
                coefsConstr.append([1.0, -1.0, -M])
                sensesConstr.append('G')
                rhsConstr.append(-data['q'][j] - M)
           
    model.linear_constraints.add(lin_expr = [[indicesConstr[i], coefsConstr[i]] for i in range(len(indicesConstr))],
                                 senses = [sensesConstr[i] for i in range(len(sensesConstr))],
                                 rhs = [rhsConstr[i] for i in range(len(rhsConstr))])                    
           

    #######################################
    #### ---- Print and warm start ---- ###
    #######################################

    print('CPLEX model: all constraints added. N constraints: %r. Time: %r\n'\
          %(model.linear_constraints.get_num(), round(time.time()-t_in,2)))


    return model




def solveModel(f, data, model):
    ''' Solve the given model, return the solved model.
        Args:
            model          cplex model to solve
        Returns:
            model          cplex model solved
    '''
    try:
        #model.set_results_stream(None)
        #model.set_warning_stream(None)

        model.solve()

        ### PRINT OBJ FUNCTION
        print('Objective function value (profit): %r\n' %round(model.solution.get_objective_value(),3))
        print('Objective function value of optimizer profit : %r\n' %round(model.solution.get_objective_value(),3), file=f)

        ### INITIALIZE DICTIONARY OF RESULTS
        results = {}
        results['MTZaux'] = np.empty(data['N']+1)
        results['xij'] = np.empty([data['N']+1,data['N']+1])
        results['Loads'] = np.empty(data['N']+1)
        results['Routing cost'] = []

        ### SAVE RESULTS
        for i in range(data['N']+1):
            for j in range(data['N']+1):
                results['xij'][i][j] = model.solution.get_values('x[' + str(i) + ']' + '[' + str(j) + ']')
        for i in range(1,data['N']+1):
            results['MTZaux'][i] = model.solution.get_values('u[' + str(i) +']')
        results['MTZaux'][0] = 0.0    
        for i in range(data['N']+1)   :
            results['Loads'][i] = model.solution.get_values('o[' + str(i) +']')
        results['Routing cost'] = model.solution.get_objective_value()
        
        ### PRINT THE RESULTS NICELY
        #PRINT THE VARIABLES AS THEY ARE
        print('Order of nodes in the tours (MTZ auxiliary var): \n', results['MTZaux'])
        print('Binary variables x_ij: \n', results['xij'])
        print('Load of the vehicle after leaving the node: \n', results['Loads'])
        #PRINT THE TOURS THEMSELVES
        ini_pos = []
        a = len(results['xij'])
        for i in range(a):
            if round(results['xij'][0][i]) == 1:
                ini_pos.append(i) 
        d = []
        for i in range(a):
            for j in range(a):
                d.append(int(round(results['xij'][i][j])))
        x = np.reshape(d, (a, a)).tolist()
        tours = {}
        for i in ini_pos:
            j = i
            tours[i] = [0,j]
            while 1 in x[j] and j != 0 :
                j = x[j].index(1)
                tours[i].append(j)
            print('Tour starting at node ' + str(i) + ':', tours[i])
        
        return results
    
    except CplexSolverError as e:
        raise Exception('Exception raised')

    return results




if __name__ == '__main__':

    with open("output.txt", "w") as f:

        t_0 = time.time()
        
        #Read instance
        #data = data_file
        t_1 = time.time()

        #SOLVE MODEL
        model = getModel(f, data)
        results = solveModel(f, data, model)

        t_2 = time.time()
        
        print('\n -- TIMING -- ')
        print('Get data + Preprocess: %r sec' %(t_1 - t_0))
        print('Run the model: %r sec' %(t_2 - t_1))
        print('\n ------------ ')
