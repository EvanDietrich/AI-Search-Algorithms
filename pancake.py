################################################################################
# Author:   Evan Dietrich
# Course:   Comp 131 - Intro AI
# Prof:     Santini
#
# Assign:   Informed Search
# Date:     10/14/2020
# File:     pancake.py
################################################################################

################################################################################
#       IMPORTS + INITIALS FOR TESTING
################################################################################

import sys
import copy
import os

CAKESTACK = [3, 2, 4, 1, 6, 5]        ## Input your own stack
ALGORITHM = "UCS"               ## Alternatively, ALGORITHM = "UCS"

################################################################################
#       InformedSearch Class: Runs PriorityQueue from Initial CAKESTACK
################################################################################

class InformedSearch:
    # Initialize blanks
    stack, prior_q, visited = [], [], []
    size, goal_state = None, None

    # Initial vals
    def __init__(self, curr_state):
        self.stack = curr_state
        if ALGORITHM == "UCS":
            self.prior_q = [[[], curr_state, 0]]
        elif ALGORITHM == "A*":
            self.prior_q = [[[], curr_state, 0, self.heuristic(curr_state),
            self.heuristic(curr_state)]]
        self.size = len(curr_state)
        self.visited = [curr_state]

    # Compute heuristic cost at current state of pancake stack
    def heuristic(self, curr_state):
        cost = 0
        for x in range(len(curr_state) - 1):
            if abs(curr_state[x] - curr_state[x + 1]) > 1:
                cost += 1
        if curr_state[len(curr_state) - 1] != len(curr_state):
            cost += 1
        return cost

    # Calculate the state after a single flip
    def flip(self, curr_state, x):
        next_state = copy.deepcopy(curr_state)
        for y in range(round(x / 2 + 0.5)):
            temp = next_state[y]
            next_state[y] = next_state[x - y]
            next_state[x - y] = temp
        return next_state

    # Helper swap function for optimally sorting our current CAKESTACK
    def swap(self, x, y):
        temp = self.prior_q[x]
        self.prior_q[x] = self.prior_q[y]
        self.prior_q[y] = temp
        return

    # Sorts our priority queue based on algorithm used
    def sortCakes(self):
        for x in range(len(self.prior_q)):
            for y in range(x, len(self.prior_q)):
                if ALGORITHM == "A*":
                    if self.prior_q[x][4] < self.prior_q[y][4]:
                        self.swap(x, y)
                elif ALGORITHM == "UCS":
                    if self.prior_q[x][2] < self.prior_q[y][2]:
                        self.swap(x, y)
        return True

    # Extend one node and add its children to the prior_q.
    def nextFrontier(self):
        next_frontier = self.prior_q.pop()
        for x in range(1, self.size):
            next_step = copy.deepcopy(next_frontier[0])
            next_step.append(x)
            next_state = copy.deepcopy(next_frontier[1])
            next_state = self.flip(next_state, x)
            backwards_cost = next_frontier[2] + 1

            ## A* includes forwards and backwards costs in determing total cost
            if ALGORITHM == "A*":
                forward_cost = self.heuristic(next_state)
                total_cost = forward_cost + backwards_cost

            ## Update
            if next_state not in self.visited:
                if ALGORITHM == "A*":
                    self.prior_q.insert(0, [next_step, next_state, backwards_cost, forward_cost, total_cost])
                elif ALGORITHM == "UCS":
                    self.prior_q.insert(0, [next_step, next_state, backwards_cost])
                self.visited.append(next_state)

        self.sortCakes()
        return True


    # Check whether the solution is found.
    def isGoalState(self):

        # Automatically exit if no remaining cakes
        if len(self.prior_q) == 0:
            self.goal_state = False
            return True

        for x in self.prior_q:
            if x[1] == list(range(1, self.size + 1)):
                self.goal_state = x
                return True

        # Keep going!
        return False

    # Runs the search procedure and executes the flip procedure
    def run(self):
        print("\nSolving for: " + str(CAKESTACK) + " using " + ALGORITHM + "\n")

        # Continue to next frontier level if goalstate not found
        while not self.isGoalState():
            self.nextFrontier()

        # In case where no goalstate is found (could be bad pancake input)
        if self.goal_state is not None:
            if self.goal_state == False:
                print("No Solution")
                return True

            # Provide instructions to the chef with flipping routine
            flip_step = copy.deepcopy(self.stack)
            flip_count = 0

            for x in self.goal_state[0]:
                x = copy.deepcopy(x)
                flip_count += 1
                flip_step = self.flip(flip_step, x)
                print("Flip Step: " + str(flip_count) +  ". Flip under Pancake #"  + (str(x + 1)) + ":")
                print("Updated Stack: " + str(flip_step))
            print ("\n\n Enjoy!\n\n( ^-^)_旦\n\n")
            return
        return

################################################################################
#       MAIN PROGRAM
################################################################################

if __name__ == '__main__':
    if (ALGORITHM == "A*") or (ALGORITHM == "UCS"):
        p = InformedSearch(CAKESTACK)
        p.run()
    else:
        print("\nPlease select a valid algorithm to run this program with\n")

