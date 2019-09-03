# Elise Ong
# Pd. 6

from collections import *
from heapq import *
from time import *
from matplotlib import pyplot as plt
from math import *
from random import *

# GOING COLUMN BY COLUMN
# Column counting starts with 0; Row counting starts with 1
global SIZE, fullSet, visited

def makeBlank(n):
    global fullSet
    fullSet = set([x for x in range(1, n+1)])
    b = tuple([fullSet.copy() for x in range(n)])
    return b
def goal_test(tup):
    if len(visited) != SIZE:    return False
    for c in tup:
        if len(c) != 1: return False    # AKA false if columns not assigned OR no valid value for col --> column's set empty
    return True
def get_vals_for_var(tup, c): # all possible numbers that can be put in index c column
    global SIZE
    vals = set()
    diffFunct = lambda x: lambda y: abs(x - y)
    for x in range(1, SIZE+1):  # going thru all possible rows
        tempBool = True
        for y in range(c):  # going thru all previously filled columns
            xDiff = diffFunct(c)(y)
            yDiff = diffFunct(x)(list(tup[y])[0])
            if xDiff == yDiff or yDiff == 0:    # if share diagonal or same row
                tempBool = False
                break
        if tempBool:    vals.add(x)
    return vals
############################################################################################
def consistent_test(tup):   # checks that at least one element exists in each set
    for t in tup:
        if len(t) < 1:  return False
    return True
def pick_blank_var(tup):    # picks variable with LEAST possibles
    global visited
    unevaluated = [x for x in list(tup) if tup.index(x) not in visited]     # QUESTIONABLE
    if unevaluated == []:
        print("Col1Change")
        visited = set()
        return 0
    minLenSet = min(unevaluated, key = lambda x:len(x))
    return tup.index(minLenSet)
def sort_free_val(tup, var):    # var is index of column
    global SIZE
    possible = get_vals_for_var(tup, var)
    conflictVal = []
    for p in possible:
        numConflict = 0
        for x in range(var+1, SIZE):
            if p in tup[x]: numConflict+=1
        heappush(conflictVal, (numConflict,p))
    sortedVals = [x[1] for x in conflictVal]    # take 2nd element of tuple, AKA the possible val to put in column
    print("var2", var)
    return sortedVals
def assign(tup, var, val):  # var is index of column, val is the actual value to assign to column var
    global SIZE, visited
    visited.add(var)
    state = ()
    for col in range(SIZE):
        if col==var:
            state+=({val},)
        else:
            newS = set([b for b in tup[col] if b != val])
            state+=(newS,)
    print(var, state)
    return state
def CSP(tup):
    if goal_test(tup):
        return tup
    var = pick_blank_var(tup)   # picks blank variable w/ most constraints on it
    print("tup:", tup, "var:", var)
    sortedFreeVal = sort_free_val(tup, var)
    print("var3", var)
    for value in sortedFreeVal:     # sort possible values by which has least constraining impact on others vars
        print(len(visited))
        print("VAR", var)   #SKETCHY
        newState = assign(tup, var, value)    # make this
        print("\tfree:", sortedFreeVal, "val:", value)
        print("\t", newState, "\n")
        if consistent_test(newState):
            result = CSP(newState)
            if result:  return result
    return False
############################################################################################
def main():
    global numNodes, SIZE, visited

    #################################################
    # TESTING CSP
    SIZE = 3
    visited = set()
    print("Size:", SIZE)
    blank = makeBlank(SIZE)
    print("blank:",blank)
    print("CSP-----")
    print(CSP(blank))
    print("-----CSP")

    # print(sort_free_val(({2}, {1, 3}, {1, 3}), 1))
    # print(assign(({2}, {1, 3}, {1, 3}), 1, 1))

if __name__ == '__main__':
    main()