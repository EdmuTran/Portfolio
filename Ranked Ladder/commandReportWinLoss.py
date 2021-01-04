import databaseManager

def reportWin(playerID):
    return reportGameResult(playerID, True)

def reportLoss(playerID):
    return reportGameResult(playerID, False)

def reportGameResult(playerID, playerWon):
    playerID = int(playerID)

    matches = databaseManager.getPlyingMatches(playerID)
    if len(matches) > 0:
        databaseManager.backup()
        match = matches[0]
        if playerWon:
            match.finishGame(playerID)
        else:
            if playerID == match.firstQueued:
                match.finishGame(match.secondQueued)
            else:
                match.finishGame(match.firstQueued)
        return f"<@{match.firstQueued}> <@{match.secondQueued}> Game recorded. !queue to continue playing games"
    
    else:
        return "You aren't matched with anyone"
    
