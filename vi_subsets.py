#for the valid inequalities

def compute_S(i,j,N,Q,q):
    '''
    i,j are the nodes of the comparison
    N, number of stations
    Q, capacity of vehicules
    q, array with requests
    '''
    ls = []
    for h in range(1,N+1):
         if h!=i and h!=j and abs(q[i]+q[j]+q[h])>Q:
                ls.append(h)
    return ls      