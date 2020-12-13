import PlayerManager

def processExitMessage(playerID):
    
    mentionPlayerCode = f'<@{playerID}>'
    
    playerDequeued = PlayerManager.dequeuePlayer(playerID)
    if playerDequeued:
        return f"{mentionPlayerCode} You've been dequeued. If you are still matched, ask your opponent to !exit."
    else:
        return f"{mentionPlayerCode} You don't need to !exit since you aren't queued."