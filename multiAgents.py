# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = successorGameState.getFood().asList()
        value=0
        n=successorGameState.getNumAgents()-1        #number of ghosts
        if (successorGameState.isWin()):
            return 400
        elif (successorGameState.isLose()):
            return -400
        if (action=="Stop"):        #no need to stop
            return -100                                                      #ghost and scaryness weightage
        sum_ghost = sum([ ((-1+(ghostState.scaredTimer /20))/ manhattanDistance(newPos,(ghostState.getPosition()))) for ghostState in newGhostStates])
                                                                                    
        l=len(newFoodList)       #food count of state
        value+= 5 * abs(len(currentGameState.getCapsules()) - len(successorGameState.getCapsules())) #capsule weightage
        if (currentGameState.hasFood(newPos[0],newPos[1])):
            value+= 3                           # nearby food weightage
        sum_food =sum([( 1/ manhattanDistance(newPos,p)) for p in newFoodList ])    #food location weightage(value,nearby food)
        if (l<=n):                           #Evaluation parameters can be made variable with time/food count
            value+= n * sum_food
            value += sum_ghost
        elif (l>(n*5) and n!=0) :
            value += (l/(5*n))*sum_ghost

            value+= sum_food
        else:
            value += sum_ghost
            value+= sum_food
            
        return value
    
def scoreEvaluationFunction(currentGameState):
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
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getNext(self,gameState,gameStateId,d,agent):
        #print(agent,type(agent))
        gameState=gameState.generateSuccessor(agent,gameStateId)
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        agent+=1
        if agent==gameState.getNumAgents():
            d=d-1
            agent=0
        if d==0:
            return self.evaluationFunction(gameState)
        #print(agent,numA)
        l=gameState.getLegalActions(agent)
        next=[]
        for i in l:
            next.append(self.getNext(gameState,i,d,agent))
        if agent==0:
            return max(next)
        return min(next)


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        d=self.depth
        l=gameState.getLegalActions(0)
        #gameStatec=gameState
        next=[]
        for i in l:
            next.append((self.getNext(gameState,i,d,0),i))
        pair=max(next)
        return pair[1]
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getNext(self,gameState,gameStateId,d,agent,alpha,beta):
        gameState=gameState.generateSuccessor(agent,gameStateId)
        if gameState.isLose():
            a=self.evaluationFunction(gameState)
            return a
        if gameState.isWin():
            a=self.evaluationFunction(gameState)
            return a
        agent+=1
        if agent==gameState.getNumAgents():
            d=d-1
            agent=0
        if d==0:
            a=self.evaluationFunction(gameState)
            return a
        l=gameState.getLegalActions(agent)
        next=[]
        for i in l:
            value=self.getNext(gameState,i,d,agent,alpha,beta)
            next.append(value)
            if agent==0:
                if value>alpha:
                    alpha=value
                if beta<alpha:
                    return alpha
            if agent>=1: 
                if value<beta:
                    beta=value
                if beta<alpha:
                    return beta
        if agent==0:
            return max(next)
        return min(next)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        d=self.depth
        l=gameState.getLegalActions(0)
        alpha=float('-inf')
        beta=float('inf')
        idx=0
        for i in l:
            value=self.getNext(gameState,i,d,0,alpha,beta)
            if value>alpha:
                alpha=value
                idx=i
        return idx
    


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getNext(self,gameState,gameStateId,d,agent):
        #print(agent,type(agent))
        gameState=gameState.generateSuccessor(agent,gameStateId)
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        agent+=1
        if agent==gameState.getNumAgents():
            d=d-1
            agent=0
        if d==0:
            return self.evaluationFunction(gameState)
        #print(agent,numA)
        l=gameState.getLegalActions(agent)
        next=[]
        for i in l:
            next.append(self.getNext(gameState,i,d,agent))
        if agent==0:
            return max(next)
        return sum(next)/len(next)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        d=self.depth
        l=gameState.getLegalActions(0)
        #gameStatec=gameState
        next=[]
        for i in l:
            next.append((self.getNext(gameState,i,d,0),i))
        pair=max(next)
        return pair[1]
        util.raiseNotDefined()
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    newFoodList = successorGameState.getFood().asList()
    value=0
    n=successorGameState.getNumAgents()-1        #number of ghosts
    if (successorGameState.isWin()):
        return float('inf')
    elif (successorGameState.isLose()):
        return float('-inf')
    #if (action=="Stop"):        #no need to stop
    #    return -50                                                      #ghost and scaryness weightage
    sum_ghost = sum([((-1+(ghostState.scaredTimer /10))/ manhattanDistance(newPos,(ghostState.getPosition()))) for ghostState in newGhostStates])
                                                                                
    l=len(newFoodList)       #food count of state
    value+= 5 * abs(len(currentGameState.getCapsules()) - len(successorGameState.getCapsules())) #capsule weightage
    if (currentGameState.hasFood(newPos[0],newPos[1])):
        value+= 3                           # nearby food weightage
    sum_food =sum([( 1/ manhattanDistance(newPos,p)) for p in newFoodList ])    #food location weightage(value,nearby food)
    if (l<=n):                           #Evaluation parameters can be made variable with time/food count
        value+=  n*sum_food
        value += sum_ghost
    elif (l>(n*5) and n!=0) :
        value += (l/(5*n))*sum_ghost
        value+= sum_food/5
    else:
        value += sum_ghost
        value+= sum_food/10
    return value"""
    Currpos = currentGameState.getPacmanPosition()
    currentScore=currentGameState.getScore()
    if currentGameState.isLose(): 
        return float("-inf")
    elif currentGameState.isWin():
        return float("inf")
    food = currentGameState.getFood().asList()
    Capsules=currentGameState.getCapsules()
    dtcFood = min(map(lambda x: util.manhattanDistance(Currpos, x), food))
    scaredGhosts, activeGhosts = [], []
    ghosts=currentGameState.getGhostStates()
    for ghost in ghosts:
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else: 
            scaredGhosts.append(ghost)
    dtcActiveGhosts =0
    dtcScaredGhosts = 0
    dtcCapsule=0

    if activeGhosts:
        dtcActiveGhosts = min(map(lambda g: util.manhattanDistance(Currpos, g.getPosition()), activeGhosts))
        
    if scaredGhosts:
        dtcScaredGhosts = min(map(lambda g: util.manhattanDistance(Currpos, g.getPosition()), scaredGhosts)) 
    if Capsules:
        dtcCapsule = min(map(lambda x: util.manhattanDistance(Currpos, x), Capsules))

    value=0
    if dtcActiveGhosts<=8:
        value = 15 * currentScore -30 * dtcFood -30 * (dtcActiveGhosts) -170*dtcScaredGhosts +random.random()+\
                -30 * dtcCapsule+\
                -30 * len(food)-30 * len(Capsules)    #+570.0/(1.0 + dtcCapsule)
    else:
        value = 10 * currentScore -20* dtcFood- 170* (dtcActiveGhosts)-50* dtcScaredGhosts + \
                -30 * len(food) + 50*random.random()
    return value

# Abbreviation
better = betterEvaluationFunction
