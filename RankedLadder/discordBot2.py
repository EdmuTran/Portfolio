import os
import discord
import nest_asyncio
nest_asyncio.apply()
import PlayerManager
PM = PlayerManager
import random
import sys
import asyncio
import commandQueue
import commandExit
import commandHelp
import commandLeaderboard
import commandCancelMatch
import commandMatches
import commandFakePlayer

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
    print('=================== New Message From Somewhere ===================')
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
                response = commandQueue.processQueueMessage(parsedMsg.playerID, parsedMsg.name)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('find-matches','exit',parsedMsg):
                response = commandExit.processExitMessage(parsedMsg.playerID)
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('score','leaderboard',parsedMsg):
                response = commandLeaderboard.processScoreMessage(parsedMsg.playerID)
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
                response = commandFakePlayer.addPlayerZero()
                await replyInSameChat(parsedMsg, response)
                
            elif parsedMessageMatchesCommand('moderation','fakeexit',parsedMsg):
                response = commandFakePlayer.removePlayerZero()
                await replyInSameChat(parsedMsg, response)
            
            else:
                await replyInSameChat(parsedMsg, "Looks like your command is wrong or"\
                                          " you're messaging in the wrong channel. "\
                                              "!help in 'find-matches' or 'score'")
        except Exception as e:
            print(e)
            await messageChannel('moderation', 'unexpected error. Response Likely Failed')

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
        print('Direct Message')
        print('Message Ignored')
        return True
    elif msg.guild != guild:
        print('Message From Other Guild')
        print('Message Ignored')
        return True
    elif parsedMsg.legal == False:
        print('Parsed Msg Not Legal')
        print('Message Ignored')
        return True
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
        self.playerID = playerID
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
        return sectionedContent[0][1:]
    
    def parseMessage():
        1

@tasks.loop(seconds=1.0)
async def tick():
    if clientIsReady == True:
        await setQueuedRole()
        
        try:
            await queuedPlayerNotificationTick()
            await displayMatchedPlayersIfMatched()
        except Exception as e:
            print('An exception occurred')
            print(e)

async def queuedPlayerNotificationTick():
    queuedPlayers = PlayerManager.queuedPlayers
    try:
        if len(queuedPlayers) - len(PM.matchedPlayers)*2 == 1:
            waitingpPlayerID = 0
            for pid in queuedPlayers:
                if not PlayerManager.playerIsMatched(pid):
                    waitingpPlayerID = pid
                
            if PM.players[waitingpPlayerID].timeQueued == 60/6:
                addons = ['Let there be blood!', 'To War!', "Don't leave them hanging!",
                          'Let me know if people actually use this channel.',
                          'Free elo points!']
                message = 'A player is queued and ready to play. ' + random.choice(addons)
                await messageChannel('game-announcements', message)
                
    except Exception as e:
        print(e)

async def displayMatchedPlayersIfMatched():
    matchedPlayers = PlayerManager.matchPlayers()
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
        await messageChannel('find-matches', message)

async def setQueuedRole():
    try:
        for member in guild.members:
            if member.id in PM.queuedPlayers:
                queuedRole = discord.utils.get(guild.roles, name="Queued")
                await member.add_roles(queuedRole)
        
        for role in guild.roles:
            if role.name == 'Queued':
                for member in role.members:
                    if member.id not in PM.queuedPlayers:
                        queuedRole = discord.utils.get(member.guild.roles, name="Queued")
                        await member.remove_roles(queuedRole)
    except Exception as e:
        print(e)

def getMaps():
    my_file = open("maps.txt", "r")
    content = my_file.read()
    maps = content.split('\n')
    mapSample = random.sample(maps, k=3)
    return mapSample

tick.start()
client.run(TOKEN)


















