# Elise Ong
# Pd. 6

from collections import deque
from time import *
from matplotlib import pyplot as plt
from math import *

# GOING COLUMN BY COLUMN
# Column counting starts with 0; Row counting starts with 1
global SIZE
# SIZE = 8

def makeBlank(n):
    b = ()
    for x in range(n):
        b += (0,)
    return b
def goal_test(tup):
    return 0 not in tup      # AKA no more unfilled columns
def get_unassigned_var(tup):   # returns column numbers that have no queens in them
    return tup.index(0)
def get_vals_for_var(tup, c): # returns all possible numbers that can be put in the column
    global SIZE
    vals = set()
    # c = the column to fill (INDEX)
    for x in range(1, SIZE+1):
        tempBool = True
        for y in range(c):
            xDiff = abs(c - y)
            yDiff = abs(x - tup[y])
            if xDiff == yDiff or yDiff == 0: # if conflicting diagonals with any prev cols OR in same row
                tempBool = False
                break
        if tempBool:    vals.add(x)
    return vals
def make_children_states(tup):    # given current board and desired direction, return new board
    curCol = get_unassigned_var(tup)
    before = tup[:curCol]
    after = tup[curCol+1:]
    ###
    children = set()
    for c in get_vals_for_var(tup, curCol):
        newC = before+(c,)+after
        children.add(newC)
    return children
def DFS(tup):
    global numNodes
    numNodes = 0

    fringe = deque()
    fringe.append(tup)
    while len(fringe) > 0:
        temp = fringe.pop()  # remove from end, treat like a stack
        # print(temp)
        if goal_test(temp) == True:  # if state is the goal state
            return temp
        else:  # if state is NOT goal state, put on valid children that haven't been visited yet
            children = make_children_states(temp)
            for c in children:
                # print(c)
                fringe.append(c)
                numNodes+=1
            # print("---------------------------------------")
    return None

def main():
    global numNodes, SIZE
    # print(len(DFS(makeBlank(SIZE))))
    # xVals = range(4, 101)
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


    # TESTING
    SIZE = 5
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