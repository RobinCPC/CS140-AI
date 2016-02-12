# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
    """
    def __init__(self, mdp, discountRate = 0.9, iters = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
    
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = util.Counter() # A Counter is a dict with default 0
    
        """Description:
        [Enter a description of what you did here.]
        Compute V (Utility) value (and Q-Value here?)
        Using Value Interation (slide 10 of MDP II)
        """
        """ YOUR CODE HERE """
        #import pdb; pdb.set_trace()
        allStates = self.mdp.getStates()                                                # get all states (position of all grids)
        #posAction = self.mdp.getPossibleActions(allStates[1])                           # get legal action of certain state
        #TranPos = self.mdp.getTransitionStatesAndProbs(allStates[1], posAction[0])      # get successor state and T(s, a, s')
        #rew = self.mdp.getReward(allStates[1], posAction[0], TranPos[0][0])             # get R(s, a, s')
        
        #self.values[allStates[0]] = TranPos[0][1]*(rew + discountRate * self.values[allStates[0]])
        
        # Do value iteration below:
        tpCnt = self.values.copy()
        for i in range(self.iters):     # total times of iteration
            for state in allStates[1:]:
                pAction = self.mdp.getPossibleActions(state)
                tpCnt[state] = max([ sum( [ trans[1] * (self.mdp.getReward(state, a, trans[0]) + self.discountRate*self.values[trans[0]]) for trans in self.mdp.getTransitionStatesAndProbs(state, a ) ] ) for a in pAction ])
                #self.values[state] = max([ sum( [ trans[1] * (self.mdp.getReward(state, a, trans[0]) + self.discountRate*self.values[trans[0]]) for trans in self.mdp.getTransitionStatesAndProbs(state, a ) ] ) for a in pAction ])
            self.values= tpCnt.copy()       # update self.values after update the utility of all states in each iteration
            #import pdb; pdb.set_trace()
        
        #self.values= tpCnt.copy()
        """ END CODE """

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]
    
        """Description:
        [Enter a description of what you did here.]
        """
        """ YOUR CODE HERE """
        util.raiseNotDefined()
        """ END CODE """

    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        """Description:
        [Enter a description of what you did here.]
        Using policy evaluation (slide 18 of MDPII)
        or 
        using current values do bellman equation to get q value (after converge one more loop will not affect q-value)
        just compute Q*(s,a) by equation in slide 9 of MDP II        
        """
        """ YOUR CODE HERE """
        #import pdb; pdb.set_trace()
        #qvalus = util.Counter()     # declaim a counter for qvalue of certain policy
        trans = self.mdp.getTransitionStatesAndProbs(state, action)
        qvalues = sum([ tr[1] * ( self.mdp.getReward(state, action, tr[0]) + self.discountRate * self.values[tr[0]] ) for tr in trans])
        return qvalues        
        """ END CODE """

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
    
        """Description:
        [Enter a description of what you did here.]
        Using policy extraction (slide 20 of MDP II)
        """
        """ YOUR CODE HERE """
        import random
        if self.mdp.isTerminal(state):
            return None
        
        posAction = self.mdp.getPossibleActions( state )   # get legal action of certain state
        #transProbs = [ self.mdp.getTransitionStatesAndProbs(state, a) for a in posAction]   # successor and its possibility        
        
        #import pdb; pdb.set_trace()
        qvalues = [ sum( [ tr[1] * (self.mdp.getReward(state, a, tr[0]) + self.discountRate * self.values[tr[0]])  for tr in self.mdp.getTransitionStatesAndProbs(state, a)] ) for a in posAction] 
        maxq = max(qvalues)
        maxIndex = [index for index in range(len(qvalues)) if qvalues[index] == maxq]
        choseindex = random.choice(maxIndex)
        
        return posAction[choseindex]
        """ END CODE """

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
