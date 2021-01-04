import databaseManager

def processExitMessage(playerID):
    playerID = int(playerID)
    
    mentionPlayerCode = f'<@{playerID}>'
    
    activeMatches = databaseManager.getActiveMatches(playerID)
    
    if len(activeMatches) > 0:
        for match in activeMatches:
            if match.firstQueued == playerID or match.secondQueued == playerID:
                match.cancelMatch()
        return f"{mentionPlayerCode} You've been dequeued along with any opponents."
    else:
        return f"{mentionPlayerCode} you aren't queued. No need to !exit"