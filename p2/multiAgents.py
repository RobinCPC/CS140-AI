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
      successorGameState = currentGameState.generatePacmanSuccessor(action)
      newPosition = successorGameState.getPacmanPosition()
      oldFood = currentGameState.getFood()
      newGhostStates = successorGameState.getGhostStates()
      newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  
      oldCapsule = currentGameState.getCapsules()
      "*** YOUR CODE HERE ***"
      # 1. add manhatDist b/w agent and ghost
      # sum total manhatDist of foods, and add its reciprocal
      if action == 'Stop':        # no stop action for relex agent (reduce computing and speed up game pace)
          return 0
      
      ### compute heuristic (manhattan) value of all ghost
      ghPositions = [ ghostState.getPosition() for ghostState in newGhostStates]      # get the positions of all ghosts
      ghHeuDists = [util.manhattanDistance(newPosition, ghP) for ghP in ghPositions]  # get manhattan distance b/w ghost and agent
      
      # if ghost is far awary, keep their heurist value equal (don't put too much weight)
      for i in range(len(ghHeuDists)):
          if ghHeuDists[i] > 5:
              ghHeuDists[i] = 5
      
      while 0 in ghHeuDists:
        ghHeuDists.remove(0)
      ghHeuDistsRec = [ 1./i for i in ghHeuDists]
      
      # if ghost is next to Pacman, keep close in scared time; avoid in normal time
      closeGhAvoid = 0 
      if newPosition in ghPositions:
          #ghHeuDists.remove(0)   # already increase its value
          if  newGhostStates[ ghPositions.index(newPosition)].scaredTimer == 0: 
              closeGhAvoid = -20          # need avoid new ghost (not in scared)
          else:
              closeGhAvoid = 5            # add wieght to keep closing scared ghost
  
      ### compute heuristic (mahanttan) value of food (pellets)
      foodList = oldFood.asList()         # get positions of all foods
      closefoodAward = 0
      if newPosition in foodList:         # remove food with the same position as agent 
          foodList.remove(newPosition)
          closefoodAward = 15             # add more heuristic value in the closest food.
      fdHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, foodPos)) for foodPos in foodList ]  # get reciprocal of heuristic of foods
  
      
      ### compute heuristic (manhattan) value of capsule
      capsuleAward = 0
      if sum(newScaredTimes)/ len(newScaredTimes) == 40:   # PacMan just eat a capsule in current state
          oldCapsule.remove(newPosition)
          capsuleAward = 10               # add more heuristic value in the closest capsule.
      if newPosition in oldCapsule:
          oldCapsule.remove(newPosition)
      capHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, cap)) for cap in oldCapsule ]        # get reciprocal of heuristic of capsules
      
      
      ### compute total evaluation score
      '''
      The total score for evaluation function is linear combination of heuristic value of pellets, ghosts, and capsules.
      In normal condition:
          Combine with heuristc distance of ghosts, reciprocal heuristic distance of foods & capsules and extra value of closed food, ghost
          I put more weighting on food & capsule heuristic value, and extra closed capsule reward (when ghost are closed)        
      In scared condition:
          Combine with reciprocal heuristic distance of ghosts, foods & capsules and extra value of closed food, ghost
          all weightinh for reciprocal heuristic value are the same, and extra reward for closed capsule
      '''
      if sum(newScaredTimes) == 0:        # PacMan need to avoid ghosts
          evalScore = sum(ghHeuDists) + 5*sum(fdHeuDistsRec) + 10*sum(capHeuDistsRec) + closefoodAward + closeGhAvoid #+ sum(ghHeuDistsRec)*capsuleAward
      else:                               # PacMan could chase scared ghosts
          evalScore = sum(ghHeuDistsRec) + sum(fdHeuDistsRec) + sum(capHeuDistsRec) + closefoodAward + closeGhAvoid + sum(ghHeuDists)*capsuleAward
          
      return evalScore
    
    

    

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
    self.currentDepth = 0   # initial as 0th layer


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
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
    legalMoves = gameState.getLegalActions(self.index)
    #ghlegalMoves = gameState.getLegalActions(1)
    #SucStates = gameState.generateSuccessor(self.index, legalMoves[0])
    #PacSucState =  gameState.generatePacmanSuccessor(legalMoves[0])
    #ghSucState = gameState.generateSuccessor(1, ghlegalMoves[0])
    #n_agent = gameState.getNumAgents()  # find how many ghost in current game
    #print self.evaluationFunction(PacSucStates)
    #print self.treeDepth
    
    ''' start minmax_dec here'''
    # return argmax_a  ACTIONS(s) MIN-VALUE(RESULT(state, a))
    # Collect legal moves and successor states
    
    PacSucStates = []           # a list to store possible successor state after PacMan move
    for action in legalMoves:
        PacSucStates.append( gameState.generatePacmanSuccessor(action) )
    
    
    scores = []                 # a list to store possible eval score for possible state
    for PacSucState in PacSucStates:
        scores.append(self.MinValue(PacSucState, 1, 0))     # compute min value of first ghost moves. 1 mean first ghost agent, next 0 mean just start 1st layer
    
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)                # Pick randomly among the best
    
    return legalMoves[chosenIndex]
    
  '''
  Min-Value function of Minmax-Decision Algorithm
  '''
  def MinValue(self, curState, ghostIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():     # agent die or eat all pellets
        return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth) and ( ghostIndex == curState.getNumAgents()-1 ):  # cut-off status
        return self.evaluationFunction(curState)
    
    v = 999999     # assign an large enough value
    ghLegalMoves = curState.getLegalActions( ghostIndex )   # get legal moves of ghost
    
    ghSucStates = []                # a list to store possible successor state after ghost move
    for action in ghLegalMoves:
        ghSucStates.append( curState.generateSuccessor(ghostIndex, action) )
    
    ghScore = []                    # a list to store possible eval score for possible state
    for SucState in ghSucStates:
        if not ghostIndex == curState.getNumAgents()-1:     # if current ghost is not last one, compute the value of next ghost
            ghScore.append( self.MinValue(SucState, ghostIndex+1, curDepth ) )
        else:                       # after all ghost move, compute the max value of PacMan move in next depth 
            ghScore.append( self.MaxValue(SucState, self.index, curDepth+1) )
    
    v = min(ghScore)                # find the minimum value from one of possible state
    return v
            
  '''
  Max-Value function of Minmax-Decision Algorithm
  '''
  def MaxValue(self, curState, pacIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():   # agent die or eat all pellets
      return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth):          # cut-off status
       return self.evaluationFunction(curState)
    
    v = -999999
    pacLegalMoves = curState.getLegalActions(self.index)    # get legal move of pacman
        
    pacSucStates = []               # l list to store possible successor state after PacMan move
    for action in pacLegalMoves:
        pacSucStates.append( curState.generatePacmanSuccessor(action) )
        
    pacScores = []                  # a list to store possible eval score for possible state
    for SucState in pacSucStates:
        pacScores.append( self.MinValue( SucState, 1, curDepth ) )      # compute min value of first ghost move.
    
    v = max(pacScores)              # find the maximum value from one of possible state
    return v
        

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # return argmax_a  ACTIONS(s) MIN-VALUE(RESULT(state, a))
    # Collect legal moves and successor states

    legalMoves = gameState.getLegalActions(self.index)
    
    PacSucStates = []           # a list to store possible successor state after PacMan move
    for action in legalMoves:
        PacSucStates.append( gameState.generatePacmanSuccessor(action) )

    scores = []                 # a list to store possible eval score for possible state
    alpha = -999999             # initial alpha an small enough value
    beta = 999999               # initial beta an large enough value

    for PacSucState in PacSucStates:
        scores.append(self.MinValue(PacSucState, alpha, beta, 1, 0)) # compute min value of first ghost moves. 1 mean first ghost agent, next 0 mean just start 1st layer
    
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)                # Pick randomly among the best
    
    return legalMoves[chosenIndex]    
    
  '''
  Min-Value function of Alpha-Beta-Search Algorithm
  '''
  def MinValue(self, curState, alpha, beta, ghostIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():     # agent die or eat all pellets
        return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth) and ( ghostIndex == curState.getNumAgents()-1 ):      # cut-off status
        return self.evaluationFunction(curState)
    
    v = 999999      # assign an large enough number
    ghLegalMoves = curState.getLegalActions( ghostIndex )   # get legal moves of ghost
    
    ghSucStates = []                # a list to store possible successor state after ghost move
    for action in ghLegalMoves:
        ghSucStates.append( curState.generateSuccessor(ghostIndex, action) )
    
    ghScore = []                    # a list to store possible eval score for possible state
    for SucState in ghSucStates:
        if not ghostIndex == curState.getNumAgents()-1:         # if current ghost is not last one, compute the value of next ghost
            ghScore.append( self.MinValue(SucState, alpha, beta, ghostIndex+1, curDepth ) )
        else:                       # after all ghost move, compute the max value of PacMan move in next depth 
            ghScore.append( self.MaxValue(SucState, alpha, beta, self.index, curDepth+1) )
    #=====================
    v = min(ghScore)                # find the minimum value from one of possible state
    if v <= alpha:
        return v
    beta = min(beta, v)
    #======================
    
    return v
            
  '''
  Max-Value function of Alpha-Beta-Search Algorithm
  '''
  def MaxValue(self, curState, alpha, beta, pacIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():       # agent die or eat all pellets
      return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth):              # cut-off status
       return self.evaluationFunction(curState)
    
    v = -999999
    pacLegalMoves = curState.getLegalActions(self.index)        # get legal move of pacman
        
    pacSucStates = []               # a list to store possible successor state after PacMan move
    for action in pacLegalMoves:
        pacSucStates.append( curState.generatePacmanSuccessor(action) )
        
    pacScores = []                  # a list to store possible eval score for possible state
    for SucState in pacSucStates:
        pacScores.append( self.MinValue( SucState, alpha, beta, 1, curDepth ) )     # compute min value of first ghost move.
    
    #=====================
    v = max(pacScores)              # find the maximum value from one of possible state
    if v >= beta:
        return v
    alpha = max(alpha, v)
    #=====================
    
    return v
    
    

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
    # return argmax_a  ACTIONS(s) MIN-VALUE(RESULT(state, a))
    # Collect legal moves and successor states

    legalMoves = gameState.getLegalActions(self.index)
    
    PacSucStates = []           # a list to store possible successor state after PacMan move
    for action in legalMoves:
        PacSucStates.append( gameState.generatePacmanSuccessor(action) )

    scores = []                 # a list to store possible eval score for possible state
    alpha = -999999             # initial alpha an small enough value
    beta = 999999               # initial beta an large enough value
    
    for PacSucState in PacSucStates:
        scores.append(self.MinValue(PacSucState, alpha, beta, 1, 0)) # compute min value of first ghost moves. 1 mean first ghost agent, next 0 mean just start 1st layer
    
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)                # Pick randomly among the best
    
    return legalMoves[chosenIndex]    
    

  '''
  Min-Value function of Expectimax-Decision Algorithm
  '''  
  def MinValue(self, curState, alpha, beta, ghostIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():     # agent die or eat all pellets
        return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth) and ( ghostIndex == curState.getNumAgents()-1 ):      # cut-off status
        return self.evaluationFunction(curState)
    
    v = 999999     # assign an large enough number
    ghLegalMoves = curState.getLegalActions( ghostIndex )   # get legal moves of ghost
    
    ghSucStates = []                # a list to store possible successor state after ghost move
    for action in ghLegalMoves:
        ghSucStates.append( curState.generateSuccessor(ghostIndex, action) )
    
    ghScore = []                    # a list to store possible eval score for possible state
    for SucState in ghSucStates:
        if not ghostIndex == curState.getNumAgents()-1:         # if current ghost is not last one, compute the value of next ghost
            ghScore.append( self.MinValue(SucState, alpha, beta, ghostIndex+1, curDepth ) )
        else:                       # after all ghost move, compute the max value of PacMan move in next depth 
            ghScore.append( self.MaxValue(SucState, alpha, beta, self.index, curDepth+1 ) )
    #=====================
    v = sum(ghScore)/len(ghScore)   # get the expextation from all possible states
    if v <= alpha:
        return v
    beta = min(beta, v)
    #======================
    
    return v
            
  '''
  Max-Value function of Expectimax-Decision Algorithm
  '''
  def MaxValue(self, curState, alpha, beta, pacIndex, curDepth):
    # check if in terminal state (win, lose, or got last layer)
    if curState.isLose() or curState.isWin():       # agent die or eat all pellets
      return self.evaluationFunction(curState)
    elif (curDepth >= self.treeDepth):              # cut-off status
       return self.evaluationFunction(curState)
    
    v = -999999
    pacLegalMoves = curState.getLegalActions(self.index)        # get legal move of pacman
        
    pacSucStates = []                   # a list to store possible successor state after PacMan move
    for action in pacLegalMoves:
        pacSucStates.append( curState.generatePacmanSuccessor(action) )
        
    pacScores = []                      # a list to store possible eval score for possible state
    for SucState in pacSucStates:
        pacScores.append( self.MinValue( SucState, alpha, beta, 1, curDepth ) )     # compute min value of first ghost move.
    
    #=====================
    v = max(pacScores)              # find the maximum value from one of possible state
    if v >= beta:
        return v
    alpha = max(alpha, v)
    #=====================
    
    return v
    

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPosition = currentGameState.getPacmanPosition()
  oldFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

  oldCapsule = currentGameState.getCapsules()
  
  ### compute heuristic (manhattan) value of all ghost
  ghPositions = [ ghostState.getPosition() for ghostState in newGhostStates]      # get the positions of all ghosts
  ghHeuDists = [util.manhattanDistance(newPosition, ghP) for ghP in ghPositions]  # get manhattan distance b/w ghost and agent

  # if ghost is far awary, keep their heurist value equal (don't put too much weight)
  for i in range(len(ghHeuDists)):
      if ghHeuDists[i] > 5:
          ghHeuDists[i] = 5

  while 0 in ghHeuDists:
      ghHeuDists.remove(0)
  ghHeuDistsRec = [ 1./i for i in ghHeuDists]

  # if ghost is next to Pacman, keep close in scared time; avoid in normal time
  closeGhAvoid = 0 
  if newPosition in ghPositions:
      #ghHeuDists.remove(0)   # already increase its value
      if  newGhostStates[ ghPositions.index(newPosition)].scaredTimer == 0:
          closeGhAvoid = -20            # need avoid new ghost (not in scared)
      else:
          closeGhAvoid = 5              # add wieght to keep closing scared ghost

  foodList = oldFood.asList()           # get positions of all foods
  closefoodAward = 0
  if newPosition in foodList:           # remove food with the same position as agent 
      foodList.remove(newPosition)
      closefoodAward = 15               # add more heuristic value in the closest food.
  fdHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, foodPos)) for foodPos in foodList ]  # get reciprocal of positions of food

  ### compute heuristic (manhattan) value of capsule
  capsuleAward = 0
  if sum(newScaredTimes)/ len(newScaredTimes) == 40:   # PacMan just eat a capsule in current state
      oldCapsule.remove(newPosition)
      capsuleAward = 10                 # add more heuristic value in the closest capsule.
  capHeuDistsRec = [ 1./(util.manhattanDistance(newPosition, cap)) for cap in oldCapsule ]

  ### compute total evaluation score
  '''
  The total score for evaluation function is linear combination of heuristic value of pellets, ghosts, and capsules.
  In normal condition:
      Combine with heuristc distance of ghosts, reciprocal heuristic distance of foods & capsules and extra value of closed food, ghost & capsule
      I put more weighting on food & capsule heuristic value, and extra closed capsule reward (when ghost are closed)        
  In scared condition:
      Combine with reciprocal heuristic distance of ghosts, foods & capsules and extra value of closed food, ghost
      all weightinh for reciprocal heuristic value are the same, and no extra reward for closed capsule
  '''
  if sum(newScaredTimes) == 0:          # PacMan need to avoid ghosts
      evalScore = currentGameState.getScore() + sum(ghHeuDists) + 5*sum(fdHeuDistsRec) + 10*sum(capHeuDistsRec) + closefoodAward + closeGhAvoid + sum(ghHeuDistsRec)*capsuleAward
  else:                                 # PacMan could chase scared ghosts
      evalScore = currentGameState.getScore() + sum(ghHeuDistsRec) + sum(fdHeuDistsRec) + sum(capHeuDistsRec) + closefoodAward + closeGhAvoid #+ sum(ghHeuDists)*capsuleAward

  return evalScore

  
  
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(ExpectimaxAgent):
  """
    Your agent for the mini-contest
  """
  
  def __init__(self, evalFn = 'betterEvaluationFunction', depth = '3'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)
    
  """
  My ContestAgent Class inherent EpectimaxAgent, so it directly call getAction function from ExpectimaxAgent.
  Its evaluation function is betterEvaluationFunction. Also, I set defualt depth to '3'. 
  """
#  def getAction(self, gameState):
#    """
#      Returns an action.  You can use any method you want and search to any depth you want.
#      Just remember that the mini-contest is timed, so you have to trade off speed and computation.
#
#      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
#      just make a beeline straight towards Pacman (or away from him if they're scared!)
#    """
#    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()

