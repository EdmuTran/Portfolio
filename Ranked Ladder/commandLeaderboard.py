import databaseManager
import eloCalculator

class playerData:
    
    def __init__(self):
        self.elo = 1000
        self.ladderPoints = 0
        self.games = 0
        self.wins = 0
        self.firstQueued = 0

firstQueuedPts = .5
secondQueuedPts = .25
winnerPts = 1

def processScoreMessage(playerID, parameters, rowsToShow=15):
    
    eloOrdered = len(parameters) > 0 and parameters[0] == 'elo'
    response = getLeaderboardAndPlayerData(eloOrdered, playerID)
    
    return response

previousNumberOfMatches = 0
def calculateLeaderboard():
    global players
    matches = databaseManager.getFinishedMatches()
    if previousNumberOfMatches != len(matches):
        players = {}
        for match in matches:
            processMatch(match)
    
def processMatch(match):
    if match.firstQueued not in players:
        players[match.firstQueued] = playerData()
    if match.secondQueued not in players:
        players[match.secondQueued] = playerData()
    
    setElo(match)
    
    players[match.firstQueued].games += 1
    players[match.firstQueued].firstQueued += 1
    players[match.secondQueued].games += 1
    players[match.winnerID].wins += 1
    
    players[match.firstQueued].ladderPoints += firstQueuedPts
    players[match.secondQueued].ladderPoints += secondQueuedPts
    players[match.winnerID].ladderPoints += winnerPts
    
def setElo(match):
    winner = players[match.winnerID]
    loser = players[match.loserID]
    winnerElo, loserElo = eloCalculator.calculateElo(winner.elo, loser.elo)
    winner.elo = winnerElo
    loser.elo = loserElo

def getLeaderboardAndPlayerData(orderByElo=False, playerID=0):
    playerID = int(playerID)
    leaderboard = getLeaderboardData()
    
    if orderByElo:
        leaderboard = sorted(leaderboard, reverse=True)
    else:
        leaderboard = sorted(leaderboard, key=lambda x: x[2], reverse=True)
    
    leaderboardString = f"LP = League Points\n+{winnerPts} for wins, +{firstQueuedPts} "\
        f"for queueing first, +{secondQueuedPts} for queueing second\n"
    leaderboardString += '```diff\n'
    
    for displayData in leaderboard:
        if int(displayData[3]) == playerID:
            player = players[playerID]
            leaderboardString += f"Name: {displayData[1]}\n"
            leaderboardString += f"Elo: {displayData[0]}\n"
            leaderboardString += f"LP: {player.ladderPoints}\n"
            leaderboardString += f"Games: {player.games}\n"
            leaderboardString += f"Wins: {player.wins}\n"
            leaderboardString += f"Times First Queued: {player.firstQueued}\n"
            leaderboardString += "\n"
    
    for displayData in leaderboard:
        toAdd = ""
        if int(displayData[3]) == int(playerID):
            toAdd += "-"
        toAdd += f"Elo: {displayData[0]} "
        toAdd = toAdd.ljust(11)
        leaderboardString += toAdd
        leaderboardString += f"| LP: {displayData[2]}".ljust(11)
        leaderboardString += f"| {displayData[1]}"
        leaderboardString += "\n"
    leaderboardString += '```'
    return leaderboardString

def getLeaderboard():
    leaderboard = getLeaderboardData()
    leaderboard = sorted(leaderboard, key=lambda x: x[2], reverse=True)
    
    leaderboardString = '```\n'
    for displayData in leaderboard:
        leaderboardString += f"Elo: {displayData[0]} ".ljust(11)
        leaderboardString += f"| LP: {displayData[2]}".ljust(11)
        leaderboardString += f"| {displayData[1]}"
        leaderboardString += "\n"
    leaderboardString += '```'
    return leaderboardString

def getLeaderboardData():
    calculateLeaderboard()
    leaderboard = []
    for playerID in players:
        player = databaseManager.Player(playerID)
        leaderboard.append([round(players[playerID].elo),player.name,players[playerID].ladderPoints, playerID])
    return leaderboard

players = {}
















