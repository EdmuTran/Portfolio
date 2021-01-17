import matplotlib.pyplot as plt
import databaseManager
import commandLeaderboard

commandLeaderboard.calculateLeaderboard()

toPlot = commandLeaderboard.players[157329269435924480].eloTracker
timeTracker = commandLeaderboard.players[157329269435924480].timeTracker

print(timeTracker)
print(toPlot)

plt.plot(timeTracker, toPlot)
plt.ylabel('some numbers')
plt.show()



