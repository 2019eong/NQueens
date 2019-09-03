from collections import deque
from heapq import heappush
from matplotlib import pyplot as plt
from time import time
from math import log10
from random import *

global SIZE, fullSet, numNodes

def makeBlank(n):
    global SIZE, fullSet, numNodes
    numNodes = 0
    fullSet = set([x for x in range(1, n+1)])
    blank = tuple([fullSet.copy() for x in range(n)])
    queenDict = dict()
    for x in range(SIZE):
        queenDict[x] = False
    return (blank, queenDict)
def goal_test(board):
    global SIZE
    tup = board[0]
    queenDict = board[1]
    #
    for c in range(SIZE):
        if len(tup[c]) != 1 or queenDict[c]==False:
            return False
    return True
def consistent_test(board):
    tup = board[0]
    for x in tup:
        if len(x) < 1:  # have at least one element in each column's set
            return False
    return True
def get_vals_for_var(board, var):
    global SIZE, fullSet
    tup = board[0]
    queenDict = board[1]
    #
    notVals = set() # all conflicting values
    colWithQueen = set(key for key,val in queenDict.items() if val == True) # columns with queens already placed
    for c in colWithQueen:
        tempRow = list(tup[c])[0]
        notVals.add(tempRow)    # prevent conflicting row
        dX = abs(c - var)
        if tempRow - dX in range(1, SIZE + 1):   notVals.add(tempRow - dX)
        if tempRow + dX in range(1, SIZE + 1):   notVals.add(tempRow + dX)
    return fullSet-notVals
def pick_blank_var(board):    # choose unvisited variable with most constraints AKA smallest set
    global SIZE
    tup = board[0]
    queenDict = board[1]
    #
    colWithQueen = set(key for key in queenDict if queenDict[key] == True)
    unvisited = [x for x in set(range(SIZE))-colWithQueen]  # unvisited is column indexes w/o queens
    unvisited.sort(key = lambda x: len(tup[x]))
    # print(unvisited)
    sameSetLen = set()
    setLen = len(tup[unvisited[0]])
    for x in unvisited:
        if len(tup[x]) > setLen:    break
        else:   sameSetLen.add(x)
    m = min(sameSetLen, key = lambda x: abs((SIZE/2)-x))
    return m
    #
    # return unvisited[randint(0, len(unvisited)-1)]
    #
    # # PREV HEURISTIC N/A
    # m = min(unvisited, key = lambda x: len(tup[x]))
    # return m
def sort_free_val(board, var):
    global SIZE
    tup = board[0]
    queenDict = board[1]
    #
    possibleVals = list(get_vals_for_var(board, var))
    shuffle(possibleVals)
    # colWithQueen = set(key for key, val in queenDict.items() if val == True)
    # weightedVals = []
    # for val in possibleVals:
    #     nConflict = 0
    #     for x in set(range(SIZE))-colWithQueen:   # AKA columns not visited yet
    #         if val in tup[x]: nConflict+=1
    #     heappush(weightedVals, (nConflict, val))
    # sortedVals = [v[1] for v in weightedVals]
    # return sortedVals
    return possibleVals
def assign(board, var, val):  # AKA creates new updated state/"child"
    global SIZE, numNodes
    tup = board[0]
    queenDict = board[1]
    #
    newTup = ()
    for x in range(SIZE):
        newSet = tup[x].copy()
        if x == var:
            newSet.clear()
            newSet.add(val)
        else:   newSet.discard(val)
        newTup+=(newSet,)
    newQueenDict = queenDict.copy()
    newQueenDict[var] = True   # once queen assigned to column, mark off as True
    return (newTup, newQueenDict)

def CSP(board, limit):
    global numNodes
    # L, D = board
    if numNodes > limit*len(board[0]): # random restart
        board, numNodes = makeBlank(len(board[0])), 0
    if goal_test(board):
        return board[0] # return the solved board
    numNodes += 1
    var = pick_blank_var(board)
    # print("tup:", board[0], "var:", var)
    sortedFreeVal = sort_free_val(board, var)
    for value in sortedFreeVal:
        newState = assign(board, var, value)
        # print(newState)

        if consistent_test(newState):
            result = CSP(newState, limit)
            if result != False:
                return result
    return False

###############################################################################################
def main():
    global SIZE, numNodes
    # SIZE = 8
    # blank = makeBlank(SIZE)  # visited also instantiated here
    # print(CSP(blank), numNodes)

    xVals = list(range(4, 101))
    xVals2 = range(101, 151)
    yValsNodes = deque()
    yValsTime = deque()
    for x in xVals:
        SIZE = x
        print("Size:", SIZE)
        tic = time()
        CSP(makeBlank(SIZE), 13)
        toc = time()
        print("Solved!", numNodes)
        yValsNodes.append(log10(numNodes))
        yValsTime.append(toc-tic)
    for x in xVals2:
        SIZE = x
        print("Size:", SIZE)
        tic = time()
        CSP(makeBlank(SIZE), 90)
        toc = time()
        print("Solved!", numNodes)
        yValsNodes.append(log10(numNodes))
        yValsTime.append(toc-tic)
    xVals.extend(xVals2)
    fig, axarr = plt.subplots(nrows=2, ncols=1)
    axarr[0].scatter(xVals, yValsNodes)
    axarr[0].set_title('Size v. log(numNodes)')
    axarr[1].scatter(xVals, yValsTime)
    axarr[1].set_title('Size v. time')
    plt.show()
    # plt.plot(xVals, yValsNodes)
    # plt.scatter(xVals, yValsNodes)
    plt.savefig("plot.png")

if __name__ == '__main__':
    main()


