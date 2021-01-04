import PlayerManager

def processCancelMatchMessage(parameters):
    if len(parameters) == 1:
        try:
            matchIndex = int(parameters[0])
            p1ID = PlayerManager.matchedPlayers[matchIndex][0]
            p2ID = PlayerManager.matchedPlayers[matchIndex][1]
            matchCancelSuccess = PlayerManager.cancelMatchAtIndex(matchIndex)
            if matchCancelSuccess:
                return f'<@{p1ID}> and <@{p2ID}> dequeued and match canceled'
            else:
                return "unexpected error. Attempted to cancel match that doesn't exist"
        except Exception as e:
            print(e)
            return "unexpected error on cancel match"
    else:
        return 'Invalid parameter count'