import databaseManager
import eloCalculator
import operator

class playerData:
    
    def __init__(self):
        self.elo = 1000
        self.ladderPoints = 0
        self.games = 0
        self.wins = 0
        self.seasonWins = 0
        self.firstQueued = 0
        
        self.ladderPointGain = 0
        self.ladderPointGains = []
    
    def transferLadderPointGain(self, outdatedGameMultiplier=1):
        self.ladderPointGains.append(self.ladderPointGain * outdatedGameMultiplier)
        
        self.ladderPointGains.sort(reverse=True)
        self.ladderPoints = 0
        multiplier = 1
        
        for pointGain in self.ladderPointGains:
            self.ladderPoints += pointGain * multiplier
            multiplier *= 0.75
        
        self.ladderPointGain = 0

    def displayData(self):
        print('===============================')
        print(self.ladderPoints)

firstQueuedPts = .5
secondQueuedPts = .25
winnerPts = 1

def processScoreMessage(playerID, parameters, rowsToShow=16):
    
    eloOrdered = len(parameters) > 0 and parameters[0] == 'elo'
    response = getLeaderboardAndPlayerData(eloOrdered, playerID)
    
    return response

def calculateLeaderboard():
    global players
    matches = databaseManager.getFinishedMatches(ascending=True)
    if len(matches) != 0:
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
    
    players[match.firstQueued].ladderPointGain += firstQueuedPts
    players[match.secondQueued].ladderPointGain += secondQueuedPts
    players[match.winnerID].ladderPointGain += winnerPts
    
    players[match.winnerID].ladderPointGain *= players[match.loserID].elo/50
    players[match.loserID].ladderPointGain *= players[match.loserID].elo/50
    
    players[match.winnerID].seasonWins += 1
    
    season3End = 1610133548.6195579
    if float(match.timeFinished) < float(season3End):
        players[match.winnerID].transferLadderPointGain(.5)
        players[match.loserID].transferLadderPointGain(.5)
    else:
        players[match.winnerID].transferLadderPointGain()
        players[match.loserID].transferLadderPointGain()
    
    # TODO Delete
# =============================================================================
#     playerID = 157329269435924480
#     if match.winnerID == playerID or match.loserID == playerID:
#         print(players[playerID].ladderPointGains)
#         players[playerID].displayData()
# =============================================================================
    
def setElo(match):
    winner = players[match.winnerID]
    loser = players[match.loserID]
    winnerElo, loserElo = eloCalculator.calculateElo(winner.elo, loser.elo)
    winner.elo = winnerElo
    loser.elo = loserElo

def getLeaderboardAndPlayerData(orderByElo=False, playerID=0, playerToShow=16):
    playerID = int(playerID)
    leaderboard = getLeaderboardData()
    
    if orderByElo:
        leaderboard = sorted(leaderboard, reverse=True)
    else:
        leaderboard = sorted(leaderboard, key=lambda x: x[2], reverse=True)
    
    leaderboardString = "LP = League Points. Your LP is influenced by wins mostly, "\
        "your opponent's elo and also queueing first or just playing games.\n"
    leaderboardString += '```diff\n'
    
    for displayData in leaderboard:
        if int(displayData[3]) == playerID:
            player = players[playerID]
            leaderboardString += f"Name: {displayData[1]}\n"
            leaderboardString += f"Elo: {round(displayData[0])}\n"
            leaderboardString += f"LP: {getLPDisplay(displayData[2])}\n"
            leaderboardString += f"Games: {player.games}\n"
            leaderboardString += f"Wins: {player.wins}\n"
            leaderboardString += f"Times First Queued: {player.firstQueued}\n"
            leaderboardString += "\n"
    
    for displayData in leaderboard:
        toAdd = ""
        if int(displayData[3]) == int(playerID):
            toAdd += "-"
        toAdd += f"Elo: {round(displayData[0])} "
        toAdd = toAdd.ljust(11)
        leaderboardString += toAdd
        leaderboardString += f"| LP: {getLPDisplay(displayData[2])}".ljust(12)
        leaderboardString += f"| {displayData[1]}"
        leaderboardString += "\n"
        
        playerToShow -= 1
        if playerToShow <= 0:
            break
    leaderboardString += '```'
    return leaderboardString

def getLeaderboard(playerToShow=16):
    leaderboard = getLeaderboardData()
    leaderboard = sorted(leaderboard, key=operator.itemgetter(2, 0), reverse=True)
    
    leaderboardString = '```\n'
    for displayData in leaderboard:
        leaderboardString += f"Elo: {round(displayData[0])} ".ljust(11)
        leaderboardString += f"| LP: {getLPDisplay(displayData[2])}".ljust(12)
        leaderboardString += f"| {displayData[1]}"
        leaderboardString += "\n"
        
        playerToShow -= 1
        if playerToShow <= 0:
            break
    leaderboardString += '```'
    return leaderboardString

def getLPDisplay(lpValue):
    return round(lpValue,1)

def getLeaderboardData():
    calculateLeaderboard()
    leaderboard = []
    for playerID in players:
        player = databaseManager.Player(playerID)
        leaderboard.append([players[playerID].elo,player.name,players[playerID].ladderPoints, playerID])
    return leaderboard

players = {}

# =============================================================================
# print(getLeaderboard(5))
# =============================================================================



















