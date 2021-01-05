import databaseManager
from databaseManager import Player
import random
import traceback

# Do the logic for queueing and return the response message
def processQueueMessage(playerID, playerName, parameters):
    playerID = int(playerID)
    
    try:
        queueTimeout = 30
        if len(parameters) > 0:
            queueTimeout = int(parameters[0])
    except:
        print(traceback.format_exc())
        queueTimeout = 30
    
    response, lobbyCreated = queuePlayer(playerID, playerName, queueTimeout)
    return response, lobbyCreated

def queuePlayer(playerID, playerName, queueTimeout=30):
    playerID = int(playerID)
    Player(playerID, playerName)
    
    mentionPlayerCode = f'<@{playerID}>'
    
    if inActiveMatch(playerID):
        lobbyCreated = False
        return f"{mentionPlayerCode} You're already queued up. '!exit' to manual dequeue.", lobbyCreated
    
    openMatches = databaseManager.getOpenMatches()
    lastOpponentID = getLastOpponent(playerID)
    for match in openMatches:
        if match.firstQueued != lastOpponentID:
            lobbyCreated = False
            return matchPlayer(match, playerID), lobbyCreated
    
    lobbyCreated = True
    return newOpenMatch(playerID, queueTimeout), lobbyCreated

def newOpenMatch(playerID, queueTimeout):
    mentionPlayerCode = f'<@{playerID}>'
    databaseManager.addMatch(playerID, queueTimeout)
    response = f"{mentionPlayerCode} You're queued up. Auto-dequeue in "\
            f"{queueTimeout} minutes. '!exit' to manual dequeue. '!Queue #' to set a time."
    return response

def matchPlayer(match, playerID):
    mentionPlayerCode = f'<@{playerID}>'
    player2ID = match.firstQueued
    mentionPlayerCodePlayer2 = f'<@{player2ID}>'
    match.addPlayer(playerID)
    response = f"{mentionPlayerCode} and {mentionPlayerCodePlayer2}, You've matched.\n\n"
    
    if random.choice([True,False]):
        temp = mentionPlayerCode
        mentionPlayerCode = mentionPlayerCodePlayer2
        mentionPlayerCodePlayer2 = temp
    
    response += f"**Pick Ban System:**\n{mentionPlayerCode} Picks first, Bans 2. Then switch. "\
        f"Ace match, {mentionPlayerCode} picks 3, bans 1. {mentionPlayerCodePlayer2} counter picks"\
        f" and bans 1 of the 3. {mentionPlayerCode} selects from the remaining 2.\n\n"
    
    response += "**Finishing/Canceling Matches:**\n'!exit' to cancel the match.\n One player must !reportwin or !reportloss after the bo3 is done.\n\n"
    response += "**Maps:**\n" + str(getMaps())
    return response

def getLastOpponent(playerID):
    lastMatches = databaseManager.getLastestCompletedMatches(playerID)
    if len(lastMatches) > 0:
        match = lastMatches[0]
        if match.firstQueued == playerID:
            return match.secondQueued
        else:
            return match.firstQueued
    else:
        return -1

def inActiveMatch(playerID):
    activeMatches = databaseManager.getActiveMatches(playerID)
    
    for match in activeMatches:
        if match.firstQueued == playerID or match.secondQueued == playerID:
            return True
    return False

def getMaps():
    my_file = open("maps.txt", "r")
    content = my_file.read()
    maps = content.split('\n')
    mapSample = random.sample(maps, k=3)
    return mapSample







