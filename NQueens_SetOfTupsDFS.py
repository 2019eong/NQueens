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
global SIZE, fullSet

def makeBlank(n):
    global fullSet
    fullSet = set([x for x in range(1, n+1)])
    b = tuple([fullSet.copy() for x in range(n)])
    return b
def goal_test(tup):
    for c in tup:
        if len(c) != 1: return False    # AKA false if columns not assigned OR no valid value for col --> column's set empty
    return True
def get_unassigned_var(tup):   # returns column numbers that have no queens in them
    global fullSet
    return tup.index(fullSet)   # returns index of set with all row nums
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
def make_children_states(tup):    # given current board and desired direction, return new board
    global SIZE
    curCol = get_unassigned_var(tup)
    before = tup[:curCol]
    after = tup[curCol+1:]
    possibleVals = get_vals_for_var(tup, curCol)
    children = [before+({p},)+after for p in possibleVals]
    return children
def DFS(tup):
    global numNodes
    numNodes = 0
    fringe = deque()
    fringe.append(tup)
    while len(fringe) > 0:
        temp = fringe.pop()  # remove from end, treat like a stack
        if goal_test(temp):  # if state is the goal state
            return temp
        else:  # if state is NOT goal state, put on valid children that haven't been visited yet
            children = make_children_states(temp)
            for c in children:
                fringe.append(c)
                numNodes += 1
            # print("-------------------------------")
    return None
############################################################################################
def main():
    global numNodes, SIZE
    # xVals = range(4, 50)
    # yVals = deque()
    # for x in xVals:
    #     SIZE = x
    #     print("Size:", SIZE)
    #     if x not in (71, 82, 91):
    #         DFS(makeBlank(SIZE))
    #         print("Solved!", numNodes)
    #     else:
    #         print("-----Skipped-----")
    #     yVals.append(log10(numNodes))
    #
    # plt.plot(xVals, yVals)
    # plt.scatter(xVals, yVals)
    # plt.show()
    # plt.savefig("plot.png")

    #################################################
    # TESTING DFS
    SIZE = 4
    print("Size:", SIZE)
    blank = makeBlank(SIZE)
    print(DFS(blank))


if __name__ == '__main__':
    main()

# a tuple made up of sets; each set holds all the possible values for that particular column; when
# assigning a value to the current column, make sure to update the sets for all other columns by
# removing that row number from the set. That will get rid of conflicting rows (also make sure
# to remove all numbers that are in conflicting diagonals from other columns' sets as well).
# that way the constraints are taken care of.

    # newAfter = ()
    # for x in range(curCol+1, SIZE): # AKA remove curCol value from other columns
    #     newAfterCol = tup[x].copy()
    #     newAfterCol.remove(c)
    #     newAfter += (newAfterCol,)
    # newC = newBefore + (newCurCol,) + newAfter