import PlayerManager

def processScoreMessage(playerID, rows=15):
    atMessage = f'<@{playerID}>'
    playerInfo = PlayerManager.getPlayerInfoAsText(playerID)
    
    response = atMessage + '\n' + playerInfo + '\n'
    response += PlayerManager.getLeaderboard(rows=rows)
    return response
