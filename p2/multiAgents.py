# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    #import pdb; pdb.set_trace()
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    #import pdb; pdb.set_trace()
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    oldCapsule = currentGameState.getCapsules()
    "*** YOUR CODE HERE ***"
    # 1. add manhatDist b/m agent and ghost
    # sum total manhatDist of foods, and add its reciprocal
    if action == 'Stop':
        return 0
        
    ghPositions = [ ghostState.getPosition() for ghostState in newGhostStates]      # get the positions of all ghosts
    ghHeuDists = [util.manhattanDistance(newPosition, ghP) for ghP in ghPositions]  # get manhattan distance b/w ghost and agent
    
    for i in range(len(ghHeuDists)):
        if ghHeuDists[i] > 5:
            ghHeuDists[i] = 5
#        if ghHeuDists[i] == 0:
#            ghHeuDists[i] = 0
#        elif ghHeuDists[i] <= 5:
#            ghHeuDists[i] *= 5  # weighting the score of the closed ghost
        
    #ghHeuDists.sort()   # let most close ghost in first element
    #if ghHeuDists[0] <= 5:
    #    ghHeuDists[0] *= 5  # weighting the score of the closed ghost

    foodList = oldFood.asList()         # get positions of all foods
    closefoodAward = 0
    if newPosition in foodList:         # remove food with the same position as agent 
        foodList.remove(newPosition)
        closefoodAward = 15
    fdHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, foodPos)) for foodPos in foodList ]  # get reciprocal of positions of food

    
    capsuleAward = 0
    if sum(newScaredTimes)/ len(newScaredTimes) == 40:   # PacMan just eat a capsule
        #import pdb; pdb.set_trace()
        oldCapsule.remove(newPosition)
        capsuleAward = 2
    capHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, cap)) for cap in oldCapsule ]
    
    closeGhAvoid = 0 
    if newPosition in ghPositions:
        ghHeuDists.remove(0)   # already increase its value
        if  newGhostStates[ ghPositions.index(newPosition)].scaredTimer == 0:     # new ghost need avoid
            closeGhAvoid = -20
        else:
            closeGhAvoid = 5

    if sum(newScaredTimes) == 0: # PacMan need to avoid ghosts
        evalScore = sum(ghHeuDists) + 5*sum(fdHeuDistsRec) + closefoodAward + closeGhAvoid + sum(capHeuDistsRec)
    else:

        
        ghHeuDistsRec = [ 1./i for i in ghHeuDists]
        evalScore = sum(ghHeuDistsRec) + sum(fdHeuDistsRec) + closefoodAward + sum(ghHeuDists)*capsuleAward + closeGhAvoid + sum(capHeuDistsRec)
    
    return evalScore    #successorGameState.getScore() + sum(ghHeuDists) + sum(fdHeuDistsRec)
    
    

    

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

