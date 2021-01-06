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
        
        response = getStatChangeText(match.firstQueued, round(p1.elo - p1EloBefore), 
                                     p1.ladderPoints - p1LadderPointsBefore)
        response += getStatChangeText(match.secondQueued, round(p2.elo - p2EloBefore), 
                                      p2.ladderPoints - p2LadderPointsBefore)
        response += "Game recorded. !queue to continue playing games"
        return response
    else:
        return "You aren't matched with anyone"
    
def getStatChangeText(playerId, eloChange, leadderPointChange):
    if eloChange >= 0:
        response = f"<@{playerId}> Elo: +{eloChange}, "\
            f"LP: +{leadderPointChange}\n"
    else:
        response = f"<@{playerId}> Elo: {eloChange}, "\
            f"LP: +{leadderPointChange}\n"
    return response