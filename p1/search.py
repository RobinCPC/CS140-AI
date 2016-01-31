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
  #print "Start:", problem.startingState()
  #print "Is the start a goal?", problem.isGoal(problem.startingState())
  #print "Start's successors:", problem.successorStates(problem.startingState())
  #print "action south cost: ", problem.actionsCost(['South'])
  #print dir(problem)

  node = problem.startingState()


  # initialize the explored set to be empty
  exploded = set()


  solution = [] # record each step to goal
  stateDic = {} # dict to store state (key) and its previos state and action from prevState
  preState = 'none'    # initial as 'none'
  action = 'Stop'    # initial as 'Stop'
  vitCorner = (False, False, False, False)#0 #[]    # record all corner

  #initialize fringe with initial state
  fringe = util.Stack()

  # put initail state, it direction, cost, previosu state and previous headign direction
  fringe.push((node, action, [] ,preState, action, vitCorner))     
  
  # dummy check if already put at goal position
  #if (problem.isGoal( (node, vitCorner) )):
  #    return solution

  while not fringe.isEmpty():
      node, action, cost, preState, preDir, preCorner = fringe.pop()

      vitCorner = CornerCherck(problem.corners, node, preCorner)

      if not (node, action, vitCorner) in exploded:
          exploded.add( (node, action, vitCorner) )
          stateDic[(node, action, vitCorner)] = (preState, preDir, preCorner)
          if (problem.isGoal( (node, vitCorner) )):
              return PathCreate(problem.startingState(), node, action, vitCorner, stateDic) #actions

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0],v[1], vitCorner) in exploded:
                  fringe.push( (v[0],v[1],v[2], node, action, vitCorner ) )    # record next successor, its action, its cost, and current node & its heading direction


  return [] # search all path but fail




def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"

  #print "Start's successors:", problem.successorStates(problem.startingState())
  node = problem.startingState()

  # initialize the explored set to be empty
  exploded = set()

  solution = [] # record each step to goal
  stateDic = {} # dict to store state (key) and its previos state and action from prevState
  preState = 'none'    # initial as 'none'
  action = 'Stop'    # initial as 'Stop'
  vitCorner = (False, False, False, False)#0 #[]    # record all corner

  #initialize fringe with initial state
  fringe = util.Queue()
  fringe.push((node, action, [] ,preState, action, vitCorner))

  # dummy check is already put at goal position
  #if (problem.isGoal( (node, vitCorner) ) ):
  #    return solution

  while not fringe.isEmpty():
      node, action, cost, preState, preDir, preCorner = fringe.pop()

      vitCorner = CornerCherck(problem.corners, node, preCorner)

      #import pdb; pdb.set_trace()
      if not (node, action, vitCorner) in exploded:
          exploded.add( (node, action, vitCorner) )
          stateDic[(node, action, vitCorner)] = (preState, preDir, preCorner)
          if (problem.isGoal( (node, vitCorner) )):
              #import pdb; pdb.set_trace()
              return PathCreate(problem.startingState(), node, action, vitCorner, stateDic) #actions

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0],v[1], vitCorner) in exploded:
                  fringe.push( (v[0],v[1],v[2], node, action, vitCorner ) )


  return [] # search all path but fail


def CornerCherck( corners, node, vitCorner):
    if node in corners:
        check = [False, False, False, False]
        for i in range(len(corners)):
            if node == corners[i]:
                check[i] = True
            else:
                check[i] = vitCorner[i]
        return (check[0], check[1], check[2], check[3])
        #if b_food: 
        #    vitCorner += 1 
        
        #if not node in vitCorner:
        #    vitCorner.append(node)
    return vitCorner

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  #print "Start:", problem.startingState()
  #print "Is the start a goal?", problem.isGoal(problem.startingState())
  #print "Start's successors:", problem.successorStates(problem.startingState())
  #print "action south cost: ", problem.actionsCost(['South'])
  #print dir(problem)


  node = problem.startingState()

  # initialize the explored set to be empty
  exploded = set()

  solution = [] # record each step to goal
  stateDic = {} # dict to store state (key) and its previos state and action from prevState
  preState = 'none'    # initial as 'none'
  action = 'Stop'    # initial as 'Stop'
  vitCorner = (False, False, False, False)#0 #[]    # record all corner

  #initialize fringe with initial state
  fringe = util.PriorityQueue()
  fringe.push((node, action, 0 ,preState, action, vitCorner), 0)

  #dummy check if already put at goal position
  #if (problem.isGoal( (node, vitCorner) )):
  #    return solution

  while not fringe.isEmpty():
      node, action, cost, preState, preDir, preCorner = fringe.pop()

      vitCorner = CornerCherck(problem.corners, node, preCorner)

      if not (node, action, vitCorner) in exploded:
          exploded.add( (node, action, vitCorner) )
          stateDic[(node, action, vitCorner)] = (preState, preDir, preCorner)
          if (problem.isGoal( (node, vitCorner) )):
              #import pdb; pdb.set_trace()
              return PathCreate(problem.startingState(), node, action, vitCorner, stateDic) #actions

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0], v[1], vitCorner) in exploded:
                  fringe.push( (v[0], v[1], cost + v[2], node, action, vitCorner ), cost + v [2] )


  return [] # search all path but fail
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  #print "Start:", problem.startingState()
  #print "Is the start a goal?", problem.isGoal(problem.startingState())
  #print "Start's successors:", problem.successorStates(problem.startingState())
  #print "dir(problem): ", dir(problem)

  #print "heuristic(problem.startingState(), problem): ", heuristic(problem.startingState(), problem)
  #print "dir(heuristic): ", dir(heuristic)

  #import pdb; pdb.set_trace()

  node = problem.startingState()

  # initialize the explored set to be empty
  exploded = set()

  solution = [] # record each step to goal
  stateDic = {} # dict to store state (key) and its previos state and action from prevState
  preState = 'none'    # initial as 'none'
  action = 'Stop'    # initial as 'Stop'
  vitCorner = (False, False, False, False)#0 #[]    # record all corner

  #initialize fringe with initial state
  fringe = util.PriorityQueue()
  fringe.push((node, action, 0 ,preState, action, vitCorner), 0)

  # dummy check if already put at goal position
  #if (problem.isGoal( (node,vitCorner) )):
  #    return solution

  while not fringe.isEmpty():
      node, action, cost, preState, preDir, preCorner = fringe.pop()

      vitCorner = CornerCherck(problem.corners, node, preCorner)

      if not (node, action, vitCorner) in exploded:
          exploded.add( (node, action, vitCorner ) )
          stateDic[(node, action, vitCorner)] = (preState, preDir, preCorner)
          if (problem.isGoal( (node,vitCorner) )):
              #import pdb; pdb.set_trace()
              return PathCreate(problem.startingState(), node, action, vitCorner, stateDic) #actions

          succStates  = problem.successorStates(node)
          for v in succStates:
              if not (v[0], v[1], vitCorner) in exploded:
                  h_n = heuristic( (v[0], vitCorner) , problem)
                  fringe.push( (v[0], v[1], cost + v[2], node, action, vitCorner ), h_n + cost + v [2] )


  return [] # search all path but fail
  util.raiseNotDefined()



def PathCreate( start, goal, action, corner, stateDic):
    solution=[]
    #import pdb; pdb.set_trace()
    solution.append(action)
    preNode, direction, preCorner = stateDic[(goal,action, corner)]
    solution.insert(0, direction)
    while not (preNode, direction) == (start,'Stop'):
        preNode, direction, preCorner = stateDic[(preNode, direction, preCorner)]
        solution.insert(0, direction)

    #print solution
    return solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
