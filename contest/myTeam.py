#------------------------------------------------------------------------------#
# Final Programming Project: Pacman Capture the Flag                           #
# Team Name: AStars                                                            #
# Team Members: Chien-Pin Chen and Jacob Preston                               #
#------------------------------------------------------------------------------# 

from captureAgents import CaptureAgent
from util import nearestPoint
import random, time, util
from game import Directions
import game

#---------------#
# Team creation #
#---------------#

# This function should return a list of two agents that will form the
# team, initialized using firstIndex and secondIndex as their agent
# index numbers.  isRed is True if the red team is being created, and
# will be False if the blue team is being created.
#
# As a potentially helpful development aid, this function can take
# additional string-valued keyword arguments ("first" and "second" are
# such arguments in the case of this function), which will come from
# the --redOpts and --blueOpts command-line arguments to capture.py.
# For the nightly contest, however, your team will be created without
# any extra arguments, so you should make sure that the default
# behavior is what you want for the nightly contest.
def createTeam(firstIndex, secondIndex, isRed,
               first = 'Bane', second = 'Bane'):

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]
  
#------------------------------------------------------------------------------#
# Agents                                                                       #
#------------------------------------------------------------------------------#

# BaseBehaviorAgent - creates structure for agent and holds all the beahvior
# functions for the extended classes to use. 
class BaseBehaviorAgent(CaptureAgent):
 
  # This method handles the initial setup of the
  # agent to populate useful fields (such as what team
  # we're on). 
  #  
  # A distanceCalculator instance caches the maze distances
  # between each pair of positions, so your agents can use:
  # self.distancer.getDistance(p1, p2)
  #
  # IMPORTANT: This method may run for at most 15 seconds.
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
  
  def food(self, successor):
    return self.getFood(successor).asList()
  
  # Finds the next successor which is a grid position (location tuple).  
  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor
  
  # checks if there is an invading enemy  
  def isInvading(self, gameState):
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    return True if invaders.__len__() > 0 else False
  
  # invasiion behavior - agent will invade opponent's side and startswith
  # collecting pellets, while avoiding ghosts. Defensive agents can exploit
  # this behavior if we're winning in order to get more pellets.
  def invade(self, gameState):
    actions = gameState.getLegalActions(self.index)
    actions.remove('Stop')
    max = float('-inf')
    ghostFeature,capFeature = (0,)*2
    bestAction = actions[0]
    for action in actions:
      successor = self.getSuccessor(gameState, action)
      foodList = self.food(successor)
      score = self.getScore(successor)
      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      defenders = [a for a in enemies if not a.isPacman and a.getPosition() != None] 
      if defenders.__len__() > 0:
        for defender in defenders:
          ghostDistance = self.getMazeDistance(myPos,defender.getPosition())
          if ghostDistance >= 1 and defender.scaredTimer != 0:
            ghostFeature = -2000
      caps = self.getCapsules(successor)
      if caps.__len__() > 0:
        capFeature = min([self.getMazeDistance(myPos, cap) for cap in caps])
      for dot in foodList:
        dotDistance = self.getMazeDistance(myPos,dot)
        value = -1*dotDistance+100*score + ghostFeature + -1*capFeature
        if max < value:
          max = value
          bestAction = action
        ghostFeature,capFeature = (0,)*2 
    return bestAction
  
  # defensive behavior - ghosts will seek and destroy invading pacman. 
  # agents can be given this behavior initially or become defensive (instead
  # of invasive) if we're losing. 
  def defend(self, gameState):
    actions = gameState.getLegalActions(self.index)
    onDefense = 1
    actions.remove('Stop')
    reverse,min_dist = (0,)*2
    max = float('-inf')
    bestAction = actions[0]
    actionMap = {}
    flag = 1
    for action in actions:
      successor = self.getSuccessor(gameState, action)
      score = self.getScore(successor)
      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
      invaderNum = len(invaders)
      if myState.isPacman: 
        onDefense = -100
      if invaderNum > 0:
        dist = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders if a.scaredTimer != 0]
        if dist.__len__() > 0:
          min_dist = (min(dist)+1)**(-1)
      rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
      if action == rev: 
        reverse = 1
      value = min_dist + -2*reverse + 100*onDefense + -1000*invaderNum
      actionMap[action] = value
      if max == value:
        actionsWithSameValue = [k for k,v in actionMap.iteritems() if v == value]
        bestAction = random.choice(actionsWithSameValue)
        actionMap.clear()
        actionMap[bestAction] = value
        flag = 0
      if max < value and flag == 1:
        max = value
        bestAction = action
      flag,onDefense = (1,)*2  
      reverse,min_dist = (0,)*2
    return bestAction    
  
#------------------------------------------------------------------------------# 
# Bane - "The Fire Rises"                                                      #
#------------------------------------------------------------------------------# 
class Bane(BaseBehaviorAgent):
  
  # chooeses the best action through a behavior depending
  # on game features
  def chooseAction(self, gameState):
    if self.isInvading(gameState):
      return self.defend(gameState)
    return self.invade(gameState)
