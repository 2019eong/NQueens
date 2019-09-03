from collections import *
from heapq import *

global SIZE, fullSet, visited

def makeBlank(n):
    global fullSet, visited
    visited = set()
    fullSet = set([x for x in range(1, n+1)])
    blank = tuple([fullSet.copy() for x in range(n)])
    return blank
def goal_test(tup):
    global SIZE, visited
    if len(visited) == SIZE:    # AKA all columns have been evaluated to fit constraints
        for s in tup:
            if len(s) != 1: return False
        return True
    return False
def consistent_test(tup):
    global fullSet, visited
    # for x in range(len(tup)):
    #     if len(tup[x]) < 1:
    #         visited.discard(x)
    #         return True
    # for s in tup:
    #     if len(s) < 1: return False
    # return True

    # tempBool = True
    # for x in range(len(tup)):
    #     if len(tup[x]) < 1:
    #         visited.discard(x)
    #         return True
    for s in tup:
        if len(s) < 1: return False
    return True
def get_vals_for_var(tup, var): # returns set of possible vals for column var
    global SIZE, fullSet, visited
    notVals = set() # all conflicting values
    diff = lambda x: lambda y: abs(x - y)
    for c in range(SIZE):   # goes thru ALL columns bc they weren't guaranteed filled L-to-R
        if c in visited:
            tempRow = list(tup[c])[0]
            notVals.add(tempRow)    # prevent same row
            dX = diff(c)(var)
            if tempRow-dX in range(1, SIZE+1):   notVals.add(tempRow-dX)
            if tempRow+dX in range(1, SIZE+1):   notVals.add(tempRow+dX)
    return fullSet-notVals
def pick_blank_var(tup):    # choose unvisited variable with most constraints AKA smallest set
    global SIZE, visited
    unvisited = [tup[x] for x in set(range(SIZE))-visited]
    # if unvisited == []: # AKA all columns have been visited
    #     print("COL-CHANGE")
    #     visited.clear()
    #     return 0
    # if unvisited == [] and goal_test(tup)==False: # AKA all columns have been visited
    #     print("COL-CHANGE")
    #     visited.discard(prevCol)
    #     # visited.clear()
    #     return prevCol
    m = min(unvisited, key = lambda x: len(x))
    print(m)
    return tup.index(m)
def sort_free_val(tup, var):
    global SIZE, visited
    possibleVals = get_vals_for_var(tup, var)
    # visited.add(var)
    weightedVals = []
    for val in possibleVals:
        nConflict = 0
        for x in set(range(SIZE))-visited:   # AKA columns not visited yet
            if val in tup[x]: nConflict+=1
        heappush(weightedVals, (nConflict, val))
    sortedVals = [v[1] for v in weightedVals]
    return sortedVals
def assign(tup, var, val):  # AKA creates new updated state/"child"
    global SIZE, visited
    # visited.add(var)    # once child created, add column var to visited set
    newTup = tup
    for x in range(SIZE):
        if x == var: newTup[x].clear(), newTup[x].add(val)  # make col var contain only val
        else: newTup[x].discard(val)
    return newTup

def CSP(tup):
    global visited

    if goal_test(tup):
        return tup
    variable = pick_blank_var(tup)
    visited.add(variable)
    print("tup:", tup, "var:", variable)
    sortedFreeVal = sort_free_val(tup, variable)
    for value in sortedFreeVal:
        print("loopagain")
        print("var2:", variable)
        print("\tvisited:",visited)
        newState = assign(tup, variable, value)
        print("\tfree:", sortedFreeVal, "val:", value)
        print("\t", newState, consistent_test(newState), "\n")
        if consistent_test(newState):
            result = CSP(newState)
            if result != False:
                return result
    return False

#############################################################################################
def main():
    global SIZE, visited
    SIZE = 4
    blank = makeBlank(SIZE)  # visited also instantiated here
    print("Blank:", blank)
    print(CSP(blank))
    # print(goal_test(({2},{4},{1},{3})))
    # visited = {0,2}
    # visited = {}
    # print(sort_free_val(({2},{1,2,3,4},{1},{1,2,4}), 3))
    # print(pick_blank_var(({2},{1,2,3,4},{1},{1,2,4})))
    # print(get_vals_for_var(({1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}), 0))
    # print(assign(blank, 1, 3))

if __name__ == '__main__':
    main()