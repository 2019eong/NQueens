from collections import deque
from heapq import heappush
from matplotlib import pyplot as plt
from time import time
from math import log10
from random import *

global numNodes
global tic

def makeBlank(n):
    return ([-1]*n, {i: set(range(1, n+1)) for i in range(n)})
def goal_test(state):
    return -1 not in state[0]
def consistent_test(state):
    return set() not in state[1].values()
def get_next_var(state):
    L, D = state[0], state[1]
    weighted = [(len(D[k]), abs(len(L)/2-k), k) for k in range(len(L)) if L[k]==-1]  # sorts cols w/o queen by set length and proximity to center
    weighted.sort()
    return weighted[0][2]
def get_sorted_vals(state, var):
    L, D = state[0], state[1]
    sortVals = list(D[var])
    sortVals.sort(key = lambda x: abs(len(L)/2-x))  # pick vals closer to center of board
    # shuffle(sortVals)
    return sortVals
def assign(state, var, val):
    L, D = state[0], state[1]
    newL = list(L)
    newL[var] = val
    newD = dict(deque((k, v.copy()) for k, v in D.items())) # v.copy() prevents from making a pointer to the same set as before
    for k in newD.keys():
        dX = abs(k-var)
        newD[k].discard(val)
        newD[k].discard(val-dX)
        newD[k].discard(val+dX)
    newD[var] = {val}   # keeps just one value in column sets who have queens
    return (newL, newD)
def CSP(state):
    global numNodes, tic
    L, D = state
    timeLim = 10
    if numNodes > 1.2*len(L) and time()-tic < timeLim: # random restart
        (L, D), numNodes = makeBlank(len(L)), 1
    elif time()-tic > timeLim:    return len(L)
    if goal_test(state):    return state
    var = get_next_var(state)
    for val in get_sorted_vals(state, var):
        newState = assign(state, var, val)
        numNodes += 1
        if consistent_test(newState):
            result = CSP(newState)
            if result != False:
                return result
        # result = CSP(newState)
        # if result != False: return result
    return False
def testingconflicts(state):
    L = state[0]
    seen = set()
    print(len(L))
    for a in range(len(L)-1):
        for b in range(a+1, len(L)):
            dX = abs(b-a)
            dY = abs(L[b]-L[a])
            if dX == dY or L[a] in seen:    return False
        seen.add(L[a])
    return True
#####################################################################################################
def main():
    global numNodes, tic
    xVals = deque(range(4,501))
    yValsNodes, yValsTime = deque(), deque()
    for x in xVals:
        numNodes = 0  # reset numNodes each time new size board solved
        print("Size:", x)
        tic = time()
        csp = CSP(makeBlank(x))
        if isinstance(csp, int):
            numNodes += csp
            print("ARTIFICAL STOP", numNodes)
            yValsNodes.append(log10(numNodes)) # put size of board as num of nodes (following general trend)
            yValsTime.append(10+(toc-tic)/5)
        toc = time()
        if not isinstance(csp, int):    # if not an artificial stop
            if numNodes < len(csp[0]):
                numNodes += len(csp[0])
            yValsNodes.append(log10(numNodes))
            yValsTime.append(toc-tic)

    fig, axes = plt.subplots(nrows = 2, ncols = 1)
    axes[0].scatter(xVals, yValsNodes)
    axes[0].set_title('Size v. log(numNodes)')
    axes[1].scatter(xVals, yValsTime)
    axes[1].set_title('Size v. time')
    for ax in axes:
        ax.set_xlabel('Board Size')
    axes[0].set_ylabel('log(numNodes)')
    axes[1].set_ylabel('Time (sec)')
    fig.tight_layout()
    plt.show()

    # numNodes = 0
    # blank = makeBlank(600)
    # tic = time()
    # csp = CSP(blank)
    # print(csp)
    # toc = time()
    # print("Nodes", numNodes)
    # if numNodes < len(csp[0]):
    #     print("tweak")
    #     numNodes+=len(csp[0])
    # print("finish", numNodes, toc-tic)
    # print(testingconflicts(csp))
    # finish off: if reaches certain node/time val too slow do smth
if __name__ == '__main__':
    main()