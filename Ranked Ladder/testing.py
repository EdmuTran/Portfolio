import databaseManager as dbm
from databaseManager import Player
import PlayerManager as PM
import commandMatches
import commandExit
import commandReportWinLoss
import commandLeaderboard
import commandQueue

def queueMatchAndReportTest():
    print(commandQueue.queuePlayer(157329269435924480, 'ent'))
    print(commandQueue.queuePlayer(271328317188079617, 'ben'))
    print(commandQueue.queuePlayer(219597559801446412, 'asd'))
    print(commandQueue.queuePlayer(585731887432204319, 'qwe'))
    print(PM.matchPlayers())
    print(PM.getMatchesAsString())
    print(commandReportWinLoss.reportWin(157329269435924480))
    print(commandReportWinLoss.reportWin(585731887432204319))

def getLeaderboard():
    print(commandLeaderboard.processScoreMessage(157329269435924480, rowsToShow=15))
    
def createAndEndMatch():
    dbm.addMatch(1)
    match = dbm.getActiveMatch(1)
    match.addPlayer(2)
    match.finishGame(1)

def getOrCreatePlayer():
    p1 = Player(2, 'playe11111111Test')

# =============================================================================
# updateAttributeTest()
# print('==================== Test 1 Done ====================\n\n')
# queueMatchAndReportTest()
# print('==================== Test 2 Done ====================\n\n')
# getLeaderboard()
# print('==================== Test 3 Done ====================\n\n')
# =============================================================================



for row in dbm.getLastestCompletedMatches(157329269435924480):
    print(row.getData())