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
  # Class vairable
  ProFoods = []
  FoodList = []
  FoodGrp0 = []
  FoodGrp1 = []

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
    
    #import pdb; pdb.set_trace()
    # record initial food list to check if enemies it our food
    #global ProFoods, FoodList, FoodGrp0, FoodGrp1        # may not a good way to share variable between objects
    BaseBehaviorAgent.ProFoods = self.getFoodYouAreDefending(gameState).asList()
    BaseBehaviorAgent.FoodList = self.food(gameState)
    
    if self.index < 2:
        self.doKmeans(gameState)
    
  
  def doKmeans(self, gameState):
    ''' use k-means to clauster food in two group, let agent split for diff food groups'''
    #wall_list = gameState.getWalls().asList()
    cen_pnts=[]  # list to store centroids
    
    # random pick two centroid point
    for i in xrange(2):
        seed = random.randint(1,10)
        centroid = random.Random(seed).choice(BaseBehaviorAgent.FoodList)        
        while centroid in cen_pnts:
          seed = random.randint(1,10)
          centroid = random.Random(seed).choice(BaseBehaviorAgent.FoodList)
        cen_pnts.append(centroid)
        #cen_pnts.append(random.Random(random.randint(1,500)).choice(FoodList))
    
    # claustering by K-means
    self.foodGrp0 = []
    self.foodGrp1 = []
    n_iter = 0      # number of iteration cauld do
    MAX_ITER = 10
    b_converge = False
    
    print cen_pnts
    while n_iter < MAX_ITER and not b_converge:
      for food in BaseBehaviorAgent.FoodList:
        dst0 = util.manhattanDistance(cen_pnts[0], food) #self.getMazeDistance(cen_pnts[0], food)
        dst1 = util.manhattanDistance(cen_pnts[1], food) #self.getMazeDistance(cen_pnts[1], food)
        if dst0 <= dst1:
          if not food in self.foodGrp0:
            self.foodGrp0.append(food)
          if food in self.foodGrp1:
            self.foodGrp1.remove(food)
        else:
          if not food in self.foodGrp1:
            self.foodGrp1.append(food)
          if food in self.foodGrp0:
            self.foodGrp0.remove(food)
      #update centroid points
      cent0x = sum([i[0] for i in self.foodGrp0])/len(self.foodGrp0)
      cent0y = sum([i[1] for i in self.foodGrp0])/len(self.foodGrp0)
      cent1x = sum([i[0] for i in self.foodGrp1])/len(self.foodGrp1)
      cent1y = sum([i[1] for i in self.foodGrp1])/len(self.foodGrp1)
      
      if cen_pnts[0] == (int(cent0x), int(cent0y)) and cen_pnts[1] == (int(cent1x), int(cent1y)):
        print "# of iter: ", n_iter+1
        b_converge = True
      else:
        cen_pnts[0] = (int(cent0x), int(cent0y))
        cen_pnts[1] = (int(cent1x), int(cent1y))
      print cen_pnts
      n_iter += 1
      
    BaseBehaviorAgent.FoodGrp0 = self.foodGrp0
    BaseBehaviorAgent.FoodGrp1 = self.foodGrp1
    for i in self.foodGrp0:
        self.debugDraw(i, [1,0,0])
    for j in self.foodGrp1:
        self.debugDraw(j, [0,1,0])
   
  
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
      
      # update FoodGrp and protected food
      if myPos in BaseBehaviorAgent.FoodGrp0:
        BaseBehaviorAgent.FoodGrp0.remove(myPos)
      elif myPos in BaseBehaviorAgent.FoodGrp1:
        BaseBehaviorAgent.FoodGrp1.remove(myPos)
#      newProFood = self.getFoodYouAreDefending(gameState).asList()
#      if len(newProFood) == len(BaseBehaviorAgent.ProFoods):
#        BaseBehaviorAgent.ProFoods = newProFood
      
      minFGdist = 0     #initial as zero
      if self.index < 2:
        if len(BaseBehaviorAgent.FoodGrp0) > 0:
          minFGdist = min( [self.getMazeDistance(myPos, food) for food in BaseBehaviorAgent.FoodGrp0 ] )
      else:
        if len(BaseBehaviorAgent.FoodGrp1) > 0:
          minFGdist = min( [self.getMazeDistance(myPos, food) for food in BaseBehaviorAgent.FoodGrp1 ] )
              
    
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
        value = -1*dotDistance + 100*score + ghostFeature + -1*capFeature + -2 * minFGdist
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
    
    newProFoods = self.getFoodYouAreDefending(gameState).asList()
    min_Gdst = 0
    if len(newProFoods) != len(BaseBehaviorAgent.ProFoods):
      curState = gameState.getAgentState(self.index)
      curPos = curState.getPosition()
      old_set = set(BaseBehaviorAgent.ProFoods)
      new_set = set(newProFoods)
      lost_food = old_set - new_set
      min_Gdst = min( [self.getMazeDistance(curPos, food) for food in lost_food] )
      if min_Gdst != 0:
        min_Gdst = min_Gdst**-1
      BaseBehaviorAgent.ProFoods = newProFoods
    
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
      value = min_dist + -2*reverse + 100*onDefense + -1000*invaderNum + 2*min_Gdst
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
