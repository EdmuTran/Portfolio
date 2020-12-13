import PlayerManager

def addPlayerZero():
    PlayerManager.addPlayer("Player 0", -1)
    return 'player zero added'

def removePlayerZero():
    PlayerManager.dequeuePlayer(-1)
    return 'player zero removed'