# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))
    explored = set()\

    while not frontier.isEmpty():
        # Pop a state and its corresponding actions from the frontier
        state, actions = frontier.pop()
        
        if state in explored:
            # Skip this state if it has already been explored
            continue
        # Add the current state to the explored set
        explored.add(state)

        if problem.isGoalState(state):
            # Return the list of actions that leads to the goal state
            return actions 
        
        for successor, action,stepCost in problem.getSuccessors(state):
            if successor not in explored:
                # Add the successor state and the updated list of actions to the frontier
                frontier.push((successor, actions + [action]))

    return []  # Return an empty list if no solution is found

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))
    explored = set()

    while not frontier.isEmpty():
        # Pop a state and its corresponding actions from the frontier
        state, actions = frontier.pop()

        if state in explored:
            # Skip this state if it has already been explored
            continue
        # Add the current state to the explored set
        explored.add(state)

        if problem.isGoalState(state):
            # Return the list of actions that leads to the goal state
            return actions
        
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in explored:
                # Calculate the total cost of the actions to reach the successor
                frontier.push((successor, actions + [action]))

    return []  # Return an empty list if no solution is found

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0), 0)
    best_cost = {start: 0}

    while not frontier.isEmpty():
        # Pop a state, its corresponding actions, and the total cost from the frontier
        state, actions, cost = frontier.pop()

        if cost != best_cost[state]:
            # Skip this state if it has already been explored with a lower cost
            continue

        if problem.isGoalState(state):
            # Return the list of actions that leads to the goal state
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            # Calculate the new cost to reach the successor state
            new_cost = cost + stepCost 

            if successor not in best_cost or new_cost < best_cost[successor]:
                # Update the best cost for the successor state and add it to the frontier
                best_cost[successor] = new_cost
                frontier.push((successor, actions + [action], new_cost), new_cost)

    return []  # Return an empty list if no solution is found

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0), heuristic(start, problem))
    best_cost = {start: 0}

    while not frontier.isEmpty():
        # Pop a state, its corresponding actions, and the total cost from the frontier
        state, actions, cost = frontier.pop()

        if cost > best_cost[state]:
            # Skip this state if it has already been explored with a lower cost
            continue
        
        if problem.isGoalState(state):
            # Return the list of actions that leads to the goal state
            return actions
        
        for successor, action, stepCost in problem.getSuccessors(state):
            # Calculate the new cost to reach the successor state
            new_cost = cost + stepCost

            if successor not in best_cost or new_cost < best_cost[successor]:
                # Update the best cost for the successor state and add it to the frontier
                best_cost[successor] = new_cost
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, actions + [action], new_cost), priority)

    return []  # Return an empty list if no solution is found


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
