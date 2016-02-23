# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.016
  """Description:
  by reducing noise, agent will move to desired action.
  Then, agent can learn currect value for its desired action
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables 
  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.5
  answerNoise = 0.016
  answerLivingReward = -1.0
  """Description:
  [Enter a description of what you did here.]
  By reducing noise, agent can move as it want, so it prefer to pass by cliff.
  By reducing discount and add negative living reward, agent will get lower 
  final reward in the distant exit, so agent would prefer the close exit.
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables 
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.5
  answerNoise = 0.1
  answerLivingReward = -1.0
  """Description:
  By using higher noise, agent can not move as it want, so it prefer to avoid the cliff.
  By reducing discount and add negative living reward, agent will get lower 
  final reward in the distant exit, so agent would prefer the close exit.
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables 
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.7
  answerNoise = 0.05
  answerLivingReward = -1.0
  """Description:
  By reducing noise, agent can move as it want, so it prefer to pass by cliff.
  By higher discount and add slight negative living reward, agent will get higher 
  final reward in the distant exit, so agent would prefer the distant exit.
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.3
  answerLivingReward = 0.0
  """Description:
  By using higher noise, agent can not move as it want, so it prefer to avoid the cliff.
  By higher discount, agent will get higher final reward in the distant exit, so agent 
  would prefer the distant exit.
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.3
  answerLivingReward = 2.0
  """Description:
  By using higher noise, agent can not move as it want, so it prefer to avoid the cliff.
  By using positive living reward, agent can get more reward without goint to exit, so 
  agent will avoid any exit
  """
  """ YOUR CODE HERE """
  # nothing here, just directly change value of above variables
  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = 0.85
  answerLearningRate = 0.8
  """Description:
  I try to make epsilon bigger so that agent will explore more (not stick with current best policy)
  And, I make learnning rate bigger in order to make the new sample get more effect on q-vlaue 
  """
  """ YOUR CODE HERE """
  # return NOT POSSIBLE is that I can't find a pair that can let agent learn to cross bridge
  # but agent cant fin the best policy to the close exit.
  
  # I also try to implement exploration function, but still 100 iteration to cross bridge
  """ END CODE """
  return 'NOT POSSIBLE' #answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
