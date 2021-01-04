import PlayerManager
import commandQueue

def addPlayer(parameters):
    if len(parameters) == 1:
        return commandQueue.queuePlayer(parameters[0], "Player 0")
    else:
        return 'parameter count not expected. Aborting'

def removePlayer(parameters):
    if len(parameters) == 1:
        return PlayerManager.dequeuePlayer(int(parameters[0]))
    else:
        return 'parameter count not expected. Aborting'