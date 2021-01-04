import PlayerManager as pm
import random

# =============================================================================
# for playerID in pm.players:
#     if pm.players[playerID].elo == 1000:
#         print('=====================')
#         print(pm.players[playerID].name)
#         print(pm.players[playerID].elo)
#         print(pm.players[playerID].gamesPlayed)
# pm.savePlayers()
# =============================================================================

def getMaps():
    my_file = open("maps.txt", "r")
    content = my_file.read()
    maps = content.split('\n')
    mapSample = random.sample(maps, k=3)
    return mapSample

print(getMaps())

# =============================================================================
# for playerID in pm.players:
#     print(pm.players[playerID].elo)
#     pm.players[playerID].elo = int(float(pm.players[playerID].elo))
# pm.savePlayers()
# =============================================================================

# =============================================================================
# def playerWins(i,playerID):
#     if pm.playerIsMatched(playerID):
#         pair = pm.getMatchedPair(playerID)
#         
#         if pair[0] == playerID:
#             player2ID = pair[1]
#         else:
#             player2ID = pair[0]
#         
#         if pm.playerIsMatched(playerID):
#             if playerID == 0:
#                 print(f'Game played and finished at {i}. {playerID} > {player2ID}')
#                 print()
#                 print(pm.getPlayerInfoAsText(playerID))
#                 print(pm.getPlayerInfoAsText(player2ID))
#                 print()
#             idDifference = player2ID - playerID
#             winPercent = min(idDifference / 5, 1)
#             roll = random.uniform(0,1)
#             if roll < winPercent:
#                 pm.playerWins(playerID)
#             else:
#                 pm.playerWins(player2ID)
#             
# def passSecond(i):
#     pm.matchPlayers()
#     for x in range(players):
#         if pm.playerIsMatched(x):
#             pm.players[x].winsIn -= 1
#         pair = pm.getMatchedPair(x)
#         if pair != None and pm.players[pair[0]].winsIn <= 0:
#             if pair[0] < pair[1]:
#                 playerWins(i,pair[0])
#             else:
#                 playerWins(i,pair[1])
# 
# #pm.clearPlayers()
# players = 26
# 
# randomPlayerOrder = list(range(players))
# random.shuffle(randomPlayerOrder)
# for i in randomPlayerOrder:
#     pm.queuePlayer(f'e{i}',i)
# 
# for i in range(60*60*3):
#     passSecond(i)
# 
# for i in range(players):
#     pm.dequeuePlayer(i)
# 
# for i in range(60*60):
#     passSecond(i)
#     
# print('============================')
# for playerID in range(0,players,5):
#     print(pm.getPlayerInfoAsText(playerID))
# =============================================================================
    
    












