import os
import discord
import nest_asyncio
nest_asyncio.apply()
import PlayerManager
PM = PlayerManager
import random
import sys
import asyncio

from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
QUEUE = os.getenv('QUEUE_CHAT')
REPORT = os.getenv('REPORT_CHAT')
SCORE = os.getenv('SCORE_CHAT')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

matchmakingChannelID = 779529614652604417
gamenotificationsChannelID = 781274234671333377
enticityID = 157329269435924480
queuedRoleID = 780987014266748948

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
# =============================================================================
#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')
# =============================================================================
    channel = client.get_channel(matchmakingChannelID)
    #await channel.send("Matchmaking Open. Bot is Running. This will also appear whenever I update the bot code. Ranked is open as long as I'm online")

secondCounter = 0

def timeToMsg():
    return secondCounter % 5 == 0

async def setQueuedRole():
    try:
        channel = client.get_channel(matchmakingChannelID)
        
        for member in channel.guild.members:
            if member.id in PM.queuedPlayers:
                queuedRole = discord.utils.get(channel.guild.roles, name="Queued")
                await member.add_roles(queuedRole)
        
        for role in channel.guild.roles:
            if role.id == queuedRoleID:
                for member in role.members:
                    if member.id not in PM.queuedPlayers:
                        queuedRole = discord.utils.get(member.guild.roles, name="Queued")
                        await member.remove_roles(queuedRole)
    except Exception as e:
        print(e)

previousPlayerStatusMsg = ''

@tasks.loop(seconds=1.0)
async def matchPlayers():
    global secondCounter
    global previousPlayerStatusMsg
    secondCounter += 1
    
    await setQueuedRole()
    
    if timeToMsg():
        msg = f'queued players: {PlayerManager.queuedPlayers}'
        msg += f'matched players {PlayerManager.matchedPlayers}'
        if previousPlayerStatusMsg != msg:
            print(msg)
            previousPlayerStatusMsg = msg
    
    try:
        matchedPlayers = PlayerManager.matchPlayers()
        channel = client.get_channel(matchmakingChannelID)
        
        queuedPlayers = PlayerManager.queuedPlayers
        
        try:
            if len(queuedPlayers) - len(PM.matchedPlayers)*2 == 1:
                waitingpPlayerID = 0
                for pid in queuedPlayers:
                    if not PlayerManager.playerIsMatched(pid):
                        waitingpPlayerID = pid
                    
                if PM.players[waitingpPlayerID].timeQueued == 60/6:
                    channel = client.get_channel(gamenotificationsChannelID)
                    addons = ['Let there be blood!', 'To War!', "Don't leave them hanging!",
                              'Let me know if people actually use this channel.',
                              'Free elo points!']
                    message = 'A player is queued and ready to play. ' + random.choice(addons)
                    print('msg Sent')
                    print(message)
                    await channel.send(message)
                    
        except Exception as e:
            print(e)
        
        if len(matchedPlayers) > 0:
            print(f'Matched Players:\n{matchedPlayers}')
        for pair in matchedPlayers:
            playerID1 = pair[0]
            playerID2 = pair[1]
            message = f'Match Found <@{playerID1}> vs <@{playerID2}>\n'
            
            if random.randint(0,1) == 0:
                message += f'<@{playerID1}> picks first\n'
            else:
                message += f'<@{playerID2}> picks first\n'
                
            try:
                message += str(getMaps())
            except:
                message += 'Maps could not be found'
            await channel.send(message)
        if len(matchedPlayers) == 0:
            1
    except Exception as e:
        print('An exception occurred')
        print(e)

def getMaps():
    my_file = open("maps.txt", "r")
    content = my_file.read()
    maps = content.split('\n')
    mapSample = random.sample(maps, k=3)
    return mapSample

matchPlayers.start()

@client.event
async def on_message(message):
    global counter
    global paused
    
    print('---------------')
# =============================================================================
#     print(message)
#     print('---------------')
#     print(f'Author ID: {message.author.id}')
#     print(message.author.name)
#     print(message.author.nick)
# =============================================================================
    print(message.content)
    
    updatePlayerName(message)
    
    if message.author.bot == False:
    
        # For when I direct message the bot
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author.id == enticityID: # My ID
                channel = client.get_channel(matchmakingChannelID)
                
                content = message.content
                if content == '!shutdown':
                    await channel.send('Bot Shutting Down')
                    sys.exit()
        
                response = processDirectMessageFromEnticity(message)
                if response != '':
                    await channel.send(response)
            
        elif str(message.channel.name)==SCORE:
            response = processScoreMessage(message)
            if response != '':
                await message.channel.send(response)
            
        elif not paused:
            print(message.channel)
            
            response = ''
            if str(message.channel.name)==QUEUE:
                responseToAdd, playerQueued, playerDequeued = processQueueMessage(message)
                response += responseToAdd
                
                responseToAdd, playersDequeued, winnerID, loserID = processReportMessage(message)
                response += responseToAdd
                
                if response != '':
                    await message.channel.send(response)

def updatePlayerName(message):
    try:
        name = message.author.nick
    except:
        name = message.author.name
    if str(name) == 'None':
        name = message.author.name
    
    playerID = message.author.id
    if playerID in PM.players:
        PM.players[playerID].name = name

paused = False

def processDirectMessageFromEnticity(message):
    global paused
    content = message.content
    if content == '!stop':
        paused = True
        return 'Bot Paused'
    if content == '!start':
        paused = False
        return 'Bot Started'
    if content == '!matches':
        return  PlayerManager.getMatchesAsString()
    if content.startswith('!cancelmatch '):
        try:
            i = int(content.split('!cancelmatch ')[1])
            result = PlayerManager.cancelMatchAtIndex(i)
            return result
        except Exception as e:
            print(e)
            return ''
    

def processScoreMessage(message):
    if not paused:
        content = message.content
        playerID = message.author.id
        atMessage = f'<@{playerID}>'
        playerInfo = PlayerManager.getPlayerInfoAsText(playerID)
        
        if content == '!leaderboard':
            response = atMessage + '\n' + playerInfo + '\n'
            response += PlayerManager.getLeaderboard()
            return response
        elif content == '!help' or content.startswith('!'):
            return '"!leaderboard to see stats'
        else:
            return ''

def processQueueMessage(message):
    content = message.content
    playerID = message.author.id
    
    try:
        name = message.author.nick
    except:
        name = message.author.name
    if str(name) == 'None':
        name = message.author.name
    
    atMessage = f'<@{playerID}>'
    playerQueued = False
    playerDequeued = False
    
    if content == '!queue':
        playerQueuedAlready = PlayerManager.queuePlayer(name, playerID)
        if playerQueuedAlready:
            response = f"{atMessage} You're already queued up. '!exit' to dequeue"
        else:
            response = f"{atMessage} You're queued up now. '!exit' to dequeue\nOne player must !reportwin or !reportloss after the bo3 is done."
            
            playerQueued = True
        queuedCount = len(PlayerManager.queuedPlayers)
        if queuedCount < 5:
            response += f'\nqueue times could be long {queuedCount} players queued'
        else:
            response += f'\n{queuedCount} players queued'
        return response, playerQueued, playerDequeued
        
    elif content == '!exit':
        playerDequeued = PlayerManager.dequeuePlayer(playerID)
        if playerDequeued:
            response = f"{atMessage} You've been dequeued. If you are still matched, ask your opponent to !exit."
            playerDequeued = True
            return response, playerQueued, playerDequeued
        else:
            response = f"{atMessage} You're already dequeued"
            return response, playerQueued, playerDequeued
    elif content == '!help':
        response = '!queue to queue up\n!exit to leave.\n'\
            '!reportwin if you won\n!reportloss if you lost.'
        return response, playerQueued, playerDequeued
    else:
        response = ''
        return response, playerQueued, playerDequeued

def processReportMessage(message):
    content = message.content.lower()
    playerID = message.author.id
    playersDequeued = False
    
    if content == '!reportwin' or content == '!reportloss':
        if PlayerManager.getPlayer(playerID).timeMatched < 60*10:
            return 'You must wait 10 minutes before reporting', playersDequeued, 0, 0
        
        if PlayerManager.getMatchedPair(playerID) == None:
            return "<@{playerID}> You aren't matched with anyone", playersDequeued, 0, 0
    
        if content.startswith('!reportwin'):
            loserID = PlayerManager.getMatchedOpponent(playerID)
            winnerID = playerID
        elif content.startswith('!reportloss'):
            winnerID = PlayerManager.getMatchedOpponent(playerID)
            loserID = playerID
            
        matchClosed = PlayerManager.playerWins(winnerID)
        if matchClosed:
            playersDequeued = True
            return f"<@{winnerID}> <@{loserID}> Game recorded. !queue to continue playing games", playersDequeued, winnerID, loserID
        else:
            return 'Something went wrong', playersDequeued, 0, 0
    else:
        return '', playersDequeued, 0, 0

def processMatchData(matchData):
    banKeywords = {'ban', 'bans'}
    
    # Check that ban is in the correct position
    viableBanPositions = {0,2}
    for i in range(5):
        if matchData[i] in banKeywords and i not in viableBanPositions:
            return False
        
    # Check that ban occures once only
    banCounter = 0
    for i in range(5):
        if matchData[i] in banKeywords:
            banCounter += 1
    if banCounter >= 2:
        return False
    
client.run(TOKEN)































