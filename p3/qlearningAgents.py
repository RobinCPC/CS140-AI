# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    #import pdb; pdb.set_trace()
    self.qValues = util.Counter()               # a counter to Q-value of (state, action)
    self.vitCount = util.Counter()              # record how many times an action get visited


  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    return the q-value for current state & action
    """
    """ YOUR CODE HERE """
    return self.qValues[(state, action)]
    """ END CODE """



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    first get legal actions of current state and find the max q-value among all legalaction. 
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)
    if len(legalActions) == 0:
        return 0.0
    maxValues = max([ self.getQValue(state, a) for a in legalActions])
    return maxValues
    
    """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    Find all of q-values of current state, and choose the action 
    with the hight q-value as optimal policy
    """
    """ YOUR CODE HERE """
    legalActions = self.getLegalActions(state)
    action = None
    policy = util.Counter()     # use counter to store action and its q-value
    
    if len(legalActions) == 0:
        return action
    
    for a in legalActions:
        policy[a] = self.getQValue(state, a)
    action = policy.argMax()
    return action

    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
    Use util.flipCoin, if return true then randomly choice from legalAction
    if flase, then sue getPolicy to get best policy action
    """
    """ YOUR CODE HERE """
    if len(legalActions) == 0:
        return action   # None
    
    if util.flipCoin(self.epsilon):
        ''' exploration function (not work well)''' 
#         posPol = util.Counter()
#         for a in legalActions:
#             if self.getQValue(state,a) >= 0:
#                 posPol[a] = -1*self.getQValue(state, a) + (1000/(self.vitCount[(state,a)]+0.0001))
#                 #print "posPol[", a, "]= ",posPol[a]
#             #posPol[a] = (self.getQValue(state, a) * self.epsilon** self.vitCount[(state,a)]) + ( self.epsilon/(self.vitCount[(state,a)]+0.1) )
#         if len(posPol) == 0:
#             action = random.choice(legalActions)
#         else:
#             action = posPol.argMax()  # random.choice(posPol.keys())
        ''' Random exploration '''
        action = random.choice(legalActions)
    else:
        action = self.getPolicy(state)
    
    """ END CODE """

    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    Use Q-Learning algoritm in slide 58 of MDP
    """
    """ YOUR CODE HERE """
    maxQns = self.getValue(nextState)   # get max q-value of next state
    if maxQns == None:
        maxQns = 0
    Qsa = self.getQValue(state, action) #self.qValues[(state, action)]
    difference  = reward + self.discountRate * maxQns - Qsa
    self.qValues[(state, action)] += self.alpha * difference
    
    self.vitCount[(state, action)] += 1
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    # currently, it is a empty counter, but will add keys in getQvalue or update function
    # According to which Extractor user choose, weight counter will have equal number of keys.
    self.weight = util.Counter() 
    

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
    [Enter a description of what you did here.]
    Use first equation in slide 71 of MDP to compute q-value depond on weights and current features.
    
    !! But I think what I did is not work for IdentityExtractor. Because feature of IdentityExtrator always return 1,
       it did not change even a ghost is closing.
    """
    """ YOUR CODE HERE """
    # if weight is empty, then weight will need to initial to 1 for all features
    # According to which Extractor user choose, weight counter will have equal number of keys.
    if len(self.weight) == 0:
        feat = self.featExtractor.getFeatures(state, action)
        self.weight.incrementAll(feat.keys(), 1)
    
    qValue = self.weight * self.featExtractor.getFeatures(state,action)
    return qValue
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    Use second equation in slide 71 of MDP
    Adjest weight of active features depend on tranistion 
    """
    """ YOUR CODE HERE """
    feat = self.featExtractor.getFeatures(state, action)

    # if weight is empty, then weight will need to initial to 1 for all features
    # According to which Extractor user choose, weight counter will have equal number of keys.
    if len(self.weight) == 0:
        feat = self.featExtractor.getFeatures(state, action)
        self.weight.incrementAll(feat.keys(), 1)
    
    maxQns = self.getValue(nextState)
    if maxQns == None:
        maxQns = 0
    Qsa = self.getQValue(state, action)
    difference = ( reward + self.discountRate * maxQns ) - Qsa
    
    for key in self.weight.keys():
        self.weight[key] += (self.alpha * difference * feat[key])
    
    
    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      print "Currrent weights: ", self.weight

