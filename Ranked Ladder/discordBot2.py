import os
import discord
import nest_asyncio
nest_asyncio.apply()
import PlayerManager
PM = PlayerManager
import commandQueue
import commandExit
import commandHelp
import commandLeaderboard
import commandCancelMatch
import commandMatches
import commandModeration
import commandReportWinLoss
import traceback
import databaseManager
import queueTimeout

from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

guild = None

clientIsReady = False

botID = 778772923984379904

@client.event
async def on_ready():
    global guild
    global clientIsReady
    print(f'{client.user} has connected to Discord!')
    for g in client.guilds:
        if g.name == GUILD:
            guild = g
            break
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    clientIsReady = True

@client.event
async def on_message(msg):
    try:
        parsedMsg = ParsedMessage(msg)
    except Exception as e:
        print(e)
        print('error parsing message. action aborted')
        return
    
    if isMessageToIgnore(msg, parsedMsg):
        return
    else:
        printMsgData(parsedMsg)
        
        try:
            if parsedMessageMatchesCommand('find-matches','help',parsedMsg):
                response = commandHelp.processFindOpponentHelpMessage()
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('find-matches','queue',parsedMsg):
                response, lobbyCreated = commandQueue.processQueueMessage(parsedMsg.playerID, parsedMsg.name, parsedMsg.parameters)
                await replyInSameChat(parsedMsg, response)
                if lobbyCreated:
                    await messageChannel('game-notifications', 'A player is waiting for a game.') 
                
            elif parsedMessageMatchesCommand('find-matches','exit',parsedMsg):
                response = commandExit.processExitMessage(parsedMsg.playerID)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('find-matches','reportwin',parsedMsg):
                response = commandReportWinLoss.reportWin(parsedMsg.playerID)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('find-matches','reportloss',parsedMsg):
                response = commandReportWinLoss.reportLoss(parsedMsg.playerID)
                await replyInSameChat(parsedMsg, response)
                
                
            elif parsedMessageMatchesCommand('score','leaderboard',parsedMsg):
                response = commandLeaderboard.processScoreMessage(parsedMsg.playerID, parsedMsg.parameters)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('score','help',parsedMsg):
                response = commandHelp.processScoreHelpMessage()
                await replyInSameChat(parsedMsg, response)
                
                
            elif parsedMessageMatchesCommand('moderation','matches',parsedMsg):
                response = commandMatches.processMatchesMessage()
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('moderation','cancelmatch',parsedMsg):
                response = commandCancelMatch.processCancelMatchMessage(parsedMsg.parameters)
                await messageChannel('find-matches', response)
                
            elif parsedMessageMatchesCommand('moderation','leaderboard',parsedMsg):
                response = commandLeaderboard.processScoreMessage(parsedMsg.playerID,30)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('moderation','queuedplayers',parsedMsg):
                await replyInSameChat(parsedMsg, str(PM.queuedPlayers))
                
            elif parsedMessageMatchesCommand('moderation','fakequeue',parsedMsg):
                response = commandModeration.addPlayer(parsedMsg.parameters)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('moderation','fakeexit',parsedMsg):
                response = commandModeration.removePlayer(parsedMsg.parameters)
                await replyInSameChat(parsedMsg, response)
            
            else:
                await replyInSameChat(parsedMsg, "Looks like your command is wrong or"\
                                          " you're messaging in the wrong channel. "\
                                              "!help in 'find-matches' or 'score'")
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            response = 'unexpected error. Occured durring ! message\n'
            response += f'command: {parsedMsg.command}'
            await messageChannel('moderation', response)

def getChannel(channelName):
    channels = guild.channels
    for channel in channels:
        if channel.name == channelName:
            return channel

async def messageChannel(channelName, response):
    channel = getChannel(channelName)
    await channel.send(response)

def printMsgData(parsedMsg):
    print(f'PlayerID: {parsedMsg.playerID}')
    print(f'name: {parsedMsg.name}')
    print(f'channelName: {parsedMsg.channelName}')
    print(f'command: {parsedMsg.command}')

async def replyInSameChat(parsedMsg, response):
    channel = client.get_channel(parsedMsg.channelID)
    await channel.send(response)

def isMessageToIgnore(msg, parsedMsg):
    if msg.author.bot == True:
        return True
    elif isDirectMessage(msg):
        print('=================== New Message From Somewhere ===================')
        print('Direct Message')
        print('Message Ignored')
        return True
    elif msg.guild != guild:
        print('=================== New Message From Somewhere ===================')
        print('Message From Other Guild')
        print('Message Ignored')
        return True
    elif parsedMsg.legal == False:
        #print('Parsed Msg Not Legal')
        #print('Message Ignored')
        return True
    print('=================== New Message From Somewhere ===================')
    return False

def isDirectMessage(msg):
    return isinstance(msg.channel, discord.channel.DMChannel)

def parsedMessageMatchesCommand(channelName, commandName, parsedMsg):
    return parsedMsg.channelName == channelName and parsedMsg.command == commandName

class ParsedMessage:
    def __init__(self,msg):
        playerID = msg.author.id
        sectionedContent = msg.content.split(' ')
        list(filter((' ').__ne__, sectionedContent))
        
        self.parameters = sectionedContent[1:]
        self.playerID = str(playerID)
        self.channelID = msg.channel.id
        self.channelName = msg.channel.name
        self.legal = self.isLegal(sectionedContent)
        self.command = self.getCommand(sectionedContent)
        try:
            playerName = msg.author.nick
        except:
            playerName = msg.author.name
        if str(playerName) == 'None':
            playerName = msg.author.name
        self.name = playerName

    def isLegal(self, sectionedContent):
        return sectionedContent[0][0] == '!'
    
    def getCommand(self, sectionedContent):
        return sectionedContent[0][1:].lower()

@tasks.loop(seconds=1.0)
async def tick():
    try:
        if clientIsReady == True:
            await setQueuedRoles()
            await setTournamentEligibleRoles()
            await queueTimeoutTick()
            await notifyPlayersOfOpenGame()
            await updateLeaderboard()
    except KeyboardInterrupt:
        print('Loop Closed')
    except:
        print(traceback.format_exc())

async def queueTimeoutTick():
    response = queueTimeout.checkForTimeout()
    if response != None:
        await messageChannel('find-matches', response)

# =============================== Role Setting ===============================

async def setQueuedRoles():
    queuedPlayers = []
    matches = databaseManager.getAllActiveMatches()
    for match in matches:
        if match.firstQueued != None:
            queuedPlayers.append(match.firstQueued)
        if match.secondQueued != None:
            queuedPlayers.append(match.secondQueued)
    await setRoles(queuedPlayers, "Queued")

async def setTournamentEligibleRoles():
    leaderboardData = commandLeaderboard.getLeaderboardData()
    qualifiedPlayers = []
    for item in leaderboardData:
        playerID = item[3]
        leaguePoints = item[2]
        if leaguePoints >= 2:
            qualifiedPlayers.append(playerID)
    await setRoles(qualifiedPlayers, "Tournament Eligible")

async def setRoles(playerIds, roleName):
    try:
        for member in guild.members:
            if member.id in playerIds:
                queuedRole = discord.utils.get(guild.roles, name=roleName)
                await member.add_roles(queuedRole)
        
        for role in guild.roles:
            if role.name == roleName:
                for member in role.members:
                    if member.id not in playerIds:
                        queuedRole = discord.utils.get(member.guild.roles, name=roleName)
                        await member.remove_roles(queuedRole)
    except Exception as e:
        print(e)

# =============================== Game notifications ===============================

async def notifyPlayersOfOpenGame():
    try:
        channel = getChannel('game-notifications')
        openMatches = databaseManager.getOpenMatches()
        
        toSkip = len(openMatches)
        msgs = await channel.history(limit=toSkip+2).flatten()
        
        for msg in msgs:
            if msg.author.id == botID:
                if toSkip <= 0:
                    await msg.edit(content='A player is waiting for a game. (The match is now closed)')
                toSkip -= 1
    except:
        #print(traceback.format_exc())
        print('Player Notification of Open Game Exception')

# =============================== Leaderboard Updates ===============================

async def updateLeaderboard():
    channel = getChannel('leaderboard')
    msgs = await channel.history(limit=1).flatten()
    
    if len(msgs) == 0:
        await messageChannel('leaderboard', commandLeaderboard.getLeaderboard())
    
    for msg in msgs:
        if msg.author.id == botID:
            await msg.edit(content=commandLeaderboard.getLeaderboard())

tick.start()
client.run(TOKEN)


















