# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  really implementation in searchAgents.py class PositionSearchProblem

  You do not need to change anything in this class, ever.
  """

  def startingState(self):
    """
    Returns the start state for the search problem
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
 

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """

  node = problem.startingState()        # contain position of agent and other (corner, or food information)


  # initialize the explored set to be empty
  exploded = set()


  stateDic = {}         # dict to store state (key) and its previos state and action from prevState
  preState = 'none'     # initial as 'none' (dummy value)
  action = 'Stop'       # initial as 'Stop' (dummy value)

  #initialize fringe with initial state
  fringe = util.Stack()

  # put initail state, its direction, cost, previosu state and previous heading direction
  fringe.push((node, action, [] ,preState, action))     
  

  while not fringe.isEmpty():
      node, action, cost, preState, preDir = fringe.pop()       # choose the last state

      if not ( node ) in exploded:
          exploded.add( (node) )    
          stateDic[(node, action)] = (preState, preDir)         # set node as exploded and bookkeeping
          if (problem.isGoal( (node) )):                        # check if reach gaol state
              return PathCreate(problem.startingState(), node, action, stateDic)    # get path from bookkeeping structure (stateDic)

          succStates  = problem.successorStates(node)           # get successor state
          for v in succStates:
              if not (v[0]) in exploded:
                  fringe.push( (v[0],v[1],v[2], node, action ) )    # record next successor, its action, its cost, and current node & its heading direction


  return [] # search all path but fail




def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"

  node = problem.startingState()    # contain position of agent and other (corner, or food information) 

  # initialize the explored set to be empty
  exploded = set()

  stateDic = {}         # dict to store state (key) and its previos state and action from prevState
  preState = 'none'     # initial as 'none' (dummy value)
  action = 'Stop'       # initial as 'Stop' (dummy value)

  #initialize fringe with initial state
  fringe = util.Queue()
  
  # put initail state, its direction, cost, previosu state and previous heading direction
  fringe.push((node, action, [] ,preState, action))


  while not fringe.isEmpty():
      node, action, cost, preState, preDir = fringe.pop()     # choose the first state

      if not ( node ) in exploded:
        exploded.add( (node ) )
        stateDic[(node, action)] = (preState, preDir)         # set node as exploded and bookkeeping
        if (problem.isGoal( node )):                          # check if reach gaol state
            return PathCreate(problem.startingState(), node, action, stateDic)  # get path from bookkeeping structure (stateDic)

        succStates  = problem.successorStates(node)           # get successor state
        for v in succStates:
            if not (v[0]) in exploded:
                fringe.push( (v[0],v[1],v[2], node, action ) )     # record next successor, its action, its cost, and current node & its heading direction 


  return [] # search all path but fail




def uniformCostSearch(problem):
  "Search the node of least total cost first. "


  node = problem.startingState()    # contain position of agent and other (corner, or food information)

  # initialize the explored set to be empty
  exploded = set()

  stateDic = {}        # dict to store state (key) and its previos state and action from prevState
  preState = 'none'    # initial as 'none'  (dummy value)
  action = 'Stop'      # initial as 'Stop'  (dummy value)

  #initialize fringe with initial state
  fringe = util.PriorityQueue()

  # put initail state, its direction, cost, previosu state and previous heading direction
  fringe.push((node, action, 0 ,preState, action), 0)


  while not fringe.isEmpty():
      node, action, cost, preState, preDir = fringe.pop()   # choose the state with the smallest priority value

      if not ( node ) in exploded:
          exploded.add( (node ) )
          stateDic[(node, action)] = (preState, preDir)     # set node as exploded and bookkeeping
          if (problem.isGoal( node )):
              return PathCreate(problem.startingState(), node, action, stateDic) # get path from bookkeeping structure (stateDic)

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0]) in exploded:
                  fringe.push( (v[0], v[1], cost + v[2], node, action ), cost + v [2] )  # record next successor, its action... and storage total costs during the path


  return [] # search all path but fail


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0


def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  node = problem.startingState()    # contain position of agent and other (corner, or food information)

  # initialize the explored set to be empty
  exploded = set()

  stateDic = {}         # dict to store state (key) and its previos state and action
  preState = 'none'     # initial as 'none' (dummy value)
  action = 'Stop'       # initial as 'Stop' (dummy value)

  #initialize fringe with initial state
  fringe = util.PriorityQueue()

  # put initail state, its direction, cost, previosu state and previous heading direction
  fringe.push((node, action, 0 ,preState, action), 0)


  while not fringe.isEmpty():
      node, action, cost, preState, preDir = fringe.pop()   # choose the state with the smallest priority value

      if not ( node ) in exploded:
          exploded.add( (node ) )
          stateDic[(node, action)] = (preState, preDir)     # set node as exploded and bookkeeping
          if (problem.isGoal( node )):
              #import pdb; pdb.set_trace()
              return PathCreate(problem.startingState(), node, action, stateDic) # get path from bookkeeping structure (stateDic)

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0]) in exploded:
                  h_n = heuristic( v[0] , problem)
                  fringe.push( (v[0], v[1], cost + v[2], node, action ), h_n + cost + v [2] ) # record next successor, its action... and storage total costs during the path + heristic value


  return [] # search all path but fail


# collecting the path from bookkeeping structure (stateDic)
def PathCreate( start, goal, action, stateDic):
    solution=[]
    solution.append(action)   # put last step (to goal) in list
    preNode, direction = stateDic[(goal,action)]      # use goal ans its action to track previous state and previos action
    solution.insert(0, direction)
    while not (preNode, direction) == (start,'Stop'):       # keep tracking until arrive starting state
        preNode, direction = stateDic[(preNode, direction)]
        solution.insert(0, direction)

    #print solution
    solution.pop(0)     # pop out unnecessary 'Stop' action in intial position
    return solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
