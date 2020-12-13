import PlayerManager

# Do the logic for queueing and return the response message
def processQueueMessage(playerID, playerName):
    
    mentionPlayerCode = f'<@{playerID}>'
    
    response = getQueueInfo(mentionPlayerCode, playerID, playerName)
    response += getPlayersQueued()
    return response


def getQueueInfo(mentionPlayerCode, playerID, playerName):
    playerQueuedAlready = PlayerManager.playerQueued(playerID)
    if playerQueuedAlready:
        return f"{mentionPlayerCode} You're already queued up. '!exit' to dequeue"
    else:
        PlayerManager.queuePlayer(playerName, playerID)
        return f"{mentionPlayerCode} You're queued up now. '!exit' to dequeue\n"\
            "One player must !reportwin or !reportloss after the bo3 is done."


def getPlayersQueued():
    queuedCount = len(PlayerManager.queuedPlayers)
    if queuedCount < 5:
        return f'\nqueue times could be long {queuedCount} players queued'
    else:
        return f'\n{queuedCount} players queued'