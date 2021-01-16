# this class is for low level database functions. Not calculations and checks

import traceback
import sqlite3 as sl
from shutil import copyfile
import PlayerManager
PM = PlayerManager
import time

databaseLocation = 'PlayerData/'
databaseName = 'my-test.db'
databasePath = databaseLocation + databaseName
    
# ================================  Player Class  =================================

class Player:
    def __init__(self, playerID, name=''):
        self.id = playerID
        
        playerData = self.get()
        if playerData != None and len(playerData) > 0:
            self.initializeVariables(playerData)
            if self.name != '':
                self.save()
        elif name != '':
            self.add(name)
            playerData = self.get()
            self.initializeVariables(playerData)
            
    def initializeVariables(self, playerData):
        self.name = playerData[1]
    
    def get(self):
        con = sl.connect(databasePath)
        try:
            with con:
                data = con.execute("SELECT * FROM Players WHERE id=?", (self.id,))
                for row in data:
                    return row
        except:
            print(traceback.format_exc())
            return None
        finally:
            con.close()
        return None
    
    def add(self, name):
        con = sl.connect(databasePath)
        
        try:
            data = (self.id, name)
            
            sql = 'INSERT INTO Players (id, name) values(?,?)'
            
            with con:
                con.execute(sql, data)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            con.close()
    
    def save(self):
        con = sl.connect(databasePath)
        
        try:
            with con:
                sql = 'UPDATE Players SET name=? WHERE id=?'
                data = (self.name, self.id)
                con.execute(sql, data)
        except:
            print(traceback.format_exc())
        finally:
            con.close()

# ================================  Match Class  =================================

class Match:
    def __init__(self, matchData):
        self.firstQueued = matchData[0]
        self.secondQueued = matchData[1]
        self.winnerID = matchData[2]
        self.timeQueued = matchData[3]
        self.timeFinished = matchData[4]
        self.cancelled = matchData[5]
        self.queueTimeout = matchData[6]
        if self.firstQueued == self.winnerID:
            self.loserID = self.secondQueued
        else:
            self.loserID = self.firstQueued
    
    def addPlayer(self, playerID):
        self.secondQueued = playerID
        self.save()
    
    def cancelMatch(self):
        self.cancelled = 1
        self.save()
    
    def finishGame(self, winnerID):
        self.winnerID = winnerID
        self.timeFinished = time.time()
        self.save()
    
    def getData(self):
        return (self.firstQueued, self.secondQueued, self.winnerID, 
                        self.timeQueued, self.timeFinished, self.cancelled, self.queueTimeout)
    
    def save(self):
        con = sl.connect(databasePath)
        
        try:
            with con:
                sql = 'UPDATE LoggedGames SET firstQueued=?, secondQueued=?,'\
                    ' winnerID=?, timeQueued=?, timeFinished=?, cancelled=?, queueTimeout=? WHERE timeQueued=?'
                data = self.getData() + (self.timeQueued,)
                con.execute(sql, data)
        except:
            print(traceback.format_exc())
        finally:
            con.close()

def addMatch(playerID, queueTimeout):
    con = sl.connect(databasePath)
    timeQueued = time.time()
    
    try:
        data = (timeQueued, playerID, queueTimeout)
        
        sql = 'INSERT INTO LoggedGames (timeQueued, firstQueued, queueTimeout) values(?,?,?)'
        
        with con:
            con.execute(sql, data)
    except:
        print(traceback.format_exc())
    finally:
        con.close()

# ================================  Backup  =================================

def backup():
    backupNum = incrementBackupNum()
    copyfile(databasePath, f'PlayerData/backup{backupNum}.db')

def getBackupNum():
    f = open("PlayerData/backupCounter.txt", "r")
    fileText = f.read()
    numCount = int(fileText)
    f.close()
    return numCount

def incrementBackupNum():
    backupNum = getBackupNum() + 1
    f = open('PlayerData/backupCounter.txt','w')
    f.write(str(backupNum))
    f.close()
    return backupNum

# ================================  Specific Queries  =================================

def getQueuedPlayers():
    sql = "SELECT firstQueued FROM LoggedGames "\
        "WHERE secondQueued IS NULL AND cancelled=0 "\
        "AND timeFinished IS NULL"
    queuedIDs = []
    for tpl in selectQuery(sql):
        queuedIDs.append(tpl[0])
    return queuedIDs

def getAllActiveMatches():
    sql = "SELECT * FROM LoggedGames "\
        "WHERE cancelled=0 "\
        "AND winnerID IS NULL"
    activeMatches = []
    for row in selectQuery(sql):
        activeMatches.append(Match(row))
    return activeMatches

def getActiveMatches(playerID):
    sql = "SELECT * FROM LoggedGames "\
        "WHERE (firstQueued=? OR secondQueued=?) AND cancelled=0 "\
        "AND winnerID IS NULL"
    parameters = (playerID,playerID)
    activeMatches = []
    for row in selectQuery(sql, parameters):
        activeMatches.append(Match(row))
    return activeMatches

def getPlyingMatches(playerID):
    sql = "SELECT * FROM LoggedGames "\
        "WHERE (firstQueued=? OR secondQueued=?) AND cancelled=0 "\
        "AND winnerID IS NULL AND secondQueued IS NOT NULL"
    parameters = (playerID,playerID)
    activeMatches = []
    for row in selectQuery(sql, parameters):
        activeMatches.append(Match(row))
    return activeMatches

def getOpenMatches():
    sql = "SELECT * FROM LoggedGames "\
        "WHERE firstQueued IS NOT NULL AND secondQueued IS NULL AND cancelled=0 "\
        "AND timeFinished IS NULL"
    matchDataRows = selectQuery(sql)
    openMatches = []
    for row in matchDataRows:
        openMatches.append(Match(row))
    return openMatches

def getLastestCompletedMatches(playerID):
    sql = "SELECT * FROM LoggedGames "\
        "WHERE (firstQueued=? OR secondQueued=?) AND winnerID IS NOT NULL AND "\
            "cancelled=0 ORDER BY timeFinished DESC"
    matchDataRows = selectQuery(sql, (playerID,playerID))
    openMatches = []
    for row in matchDataRows:
        openMatches.append(Match(row))
    return openMatches

def getFinishedMatches(ascending=False):
    sql = "SELECT * FROM LoggedGames "\
        "WHERE winnerID IS NOT NULL AND "\
            "cancelled=0 ORDER BY timeFinished DESC"
    if ascending:
        sql += "DESC"
    else:
        sql += "ASC"
    matchDataRows = selectQuery(sql)
    finishedMatches = []
    for row in matchDataRows:
        finishedMatches.append(Match(row))
    return finishedMatches

def selectQuery(sql, parameters=[]):
    con = sl.connect(databasePath)
    returnData = []
    try:
        with con:
            pulledData = con.execute(sql, parameters)
            for row in pulledData:
                returnData.append(row)
        con.close()
        return returnData
    except:
        print(traceback.format_exc())
        return None
    finally:
        con.close()
    return None








