import databaseManager
import eloCalculator

class playerData:
    
    def __init__(self):
        self.elo = 1000
        self.ladderPoints = 0

firstQueuedPts = .5
secondQueuedPts = .25
winnerPts = 1

def processScoreMessage(playerID, parameters, rowsToShow=15):
    
    eloOrdered = len(parameters) > 0 and parameters[0] == 'elo'
    response = getLeaderboard(eloOrdered)
    
    return response


def calculateLeaderboard():
    global players
    players = {}
    matches = databaseManager.getFinishedMatches()
    for match in matches:
        processMatch(match)
    
def processMatch(match):
    if match.firstQueued not in players:
        players[match.firstQueued] = playerData()
    if match.secondQueued not in players:
        players[match.secondQueued] = playerData()
    
    setElo(match)
    
    players[match.firstQueued].ladderPoints += firstQueuedPts
    players[match.secondQueued].ladderPoints += secondQueuedPts
    players[match.winnerID].ladderPoints += winnerPts
    
def setElo(match):
    winner = players[match.winnerID]
    loser = players[match.loserID]
    winnerElo, loserElo = eloCalculator.calculateElo(winner.elo, loser.elo)
    winner.elo = winnerElo
    loser.elo = loserElo

def getLeaderboard(orderByElo=False):
    leaderboard = getLeaderboardData()
    
    if orderByElo:
        leaderboard = sorted(leaderboard, reverse=True)
    else:
        leaderboard = sorted(leaderboard, key=lambda x: x[2], reverse=True)
    
    leaderboardString = f"LP = League Points\n+{winnerPts} for wins, +{firstQueuedPts} "\
        f"for queueing first, +{secondQueuedPts} for queueing second\n"
    leaderboardString += '```\n'
    for displayData in leaderboard:
        leaderboardString += f"Elo: {displayData[0]} ".ljust(11)
        leaderboardString += f"| LP: {displayData[2]}".ljust(11)
        leaderboardString += f"| {displayData[1]}\n"
        
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


















