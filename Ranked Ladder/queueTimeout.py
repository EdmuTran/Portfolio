import databaseManager
import time
import commandExit

def checkForTimeout():
    
    matches = databaseManager.getOpenMatches()
    
    response = 'Dequeued due to timeout\n\n'
    
    playerDequeued = False
    for match in matches:
        secondsSinceQueue = time.time() - match.timeQueued
        if secondsSinceQueue/60 > match.queueTimeout:
            playerDequeued = True
            response += commandExit.processExitMessage(match.firstQueued) + '\n\n'
    
    if playerDequeued:
        return response
    else:
        return None
