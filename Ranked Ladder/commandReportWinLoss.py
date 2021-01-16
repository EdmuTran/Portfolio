import databaseManager
import commandLeaderboard

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
        
        commandLeaderboard.calculateLeaderboard()
        
        if match.firstQueued not in commandLeaderboard.players:
            commandLeaderboard.players[match.firstQueued] = commandLeaderboard.playerData()
        if match.secondQueued not in commandLeaderboard.players:
            commandLeaderboard.players[match.secondQueued] = commandLeaderboard.playerData()
        
        p1Old = commandLeaderboard.players[match.firstQueued]
        p2Old = commandLeaderboard.players[match.secondQueued]
        p1EloBefore = p1Old.elo
        p1LadderPointsBefore = p1Old.ladderPoints
        p2EloBefore = p2Old.elo
        p2LadderPointsBefore = p2Old.ladderPoints
        
        print('blar===========')
        print(p1EloBefore)
        print(p1LadderPointsBefore)
        print(p2EloBefore)
        print(p2LadderPointsBefore)
        
        if playerWon:
            match.finishGame(playerID)
        else:
            if playerID == match.firstQueued:
                match.finishGame(match.secondQueued)
            else:
                match.finishGame(match.firstQueued)
        commandLeaderboard.calculateLeaderboard()
        
        p1 = commandLeaderboard.players[match.firstQueued]
        p2 = commandLeaderboard.players[match.secondQueued]
        
        print(p1.elo)
        print(p1.ladderPoints)
        print(p2.elo)
        print(p2.ladderPoints)
        
        response = getStatChangeText(match.firstQueued, (p1.elo - p1EloBefore), 
                                     p1.ladderPoints - p1LadderPointsBefore)
        response += getStatChangeText(match.secondQueued, (p2.elo - p2EloBefore), 
                                      p2.ladderPoints - p2LadderPointsBefore)
        response += "Game recorded. !queue to continue playing games"
        return response
    else:
        return "You aren't matched with anyone"
    
def getStatChangeText(playerId, eloChange, leadderPointChange):
    if eloChange >= 0:
        response = f"<@{playerId}> Elo: +{round(eloChange)}, "\
            f"LP: +{round(leadderPointChange,1)}\n"
    else:
        response = f"<@{playerId}> Elo: {round(eloChange)}, "\
            f"LP: +{round(leadderPointChange,1)}\n"
    return response