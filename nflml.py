from Scraper import Scraper
import xgboost as xgb
import pickle
import numpy as np
from os.path import exists
from sklearn import tree


# Model --> Classify score difference
# Input:
# Parameters for T1
# Parameters for T2
# 	Parameters
		# self.team = team
		# self.opponent = opponent
		# self.pointsFor = pointsFor
		# self.pointsAgainst = pointsAgainst
		# self.totalYards = totalYards
		# self.passYards = passYards
		# self.rushYards = rushYards
		# self.turnovers = turnovers
		# self.defYdsAllowed = defYdsAllowed
		# self.defPassYards = defPassYards
		# self.defRushYards = defRushYards
		# self.defTurnovers = defTurnovers
# n_features --> Parameters * 2 --> 22, but opponent will be onehot vector
# Output --> Score Differential (T1 - T2)
def generateDataAndLabels(teams, weeksPerLabel, currentWeek):
	week = 0 + weeksPerLabel
	data = []
	labels = []
	while week < currentWeek:
		d, l = generateTrainingDataForWeek(teams, weeksPerLabel, week)
		data.append(d)
		labels.append(l)
		week += 1
	return data, labels

def generateTrainingDataForWeek(teams, weeksPerLabel, week):
	data = []
	labels = []
	for _,team in teams.items():
		d, l = generateInputAndLabel(team, week, weeksPerLabel)
		data.append(d)
		labels.append(l)
	return data, labels

def generateInputAndLabel(team, week, weeksPerLabel):
	for i in range(week - weeksPerLabel, week):
		teamVec = np.zeros([1, 32])
		oppVec = np.zeros([1, 32])
		teamVec[0][team.id] = 1
		oppVec[0][team.schedule[i].opponent] = 1

	X = np.concatenate((teamVec, oppVec), axis=0)
	game = team.schedule[week]
	Y = game.pointsFor - game.pointsAgainst
	return X, Y

# Model --> Classify score difference
# Input:
# Parameters for T1
# Parameters for T2
# 	Parameters
		# self.opponent = opponent
		# self.pointsFor = pointsFor
		# self.pointsAgainst = pointsAgainst
		# self.totalYards = totalYards
		# self.passYards = passYards
		# self.rushYards = rushYards
		# self.turnovers = turnovers
		# self.defYdsAllowed = defYdsAllowed
		# self.defPassYards = defPassYards
		# self.defRushYards = defRushYards
		# self.defTurnovers = defTurnovers
# Output --> T1 points scored against T2
#def generateDataAndLabels(teams, weeksPerLabel):
#	return X, Y


if not exists('teams.pickle'):
	scraper = Scraper()
	teams = scraper.scrape()
	pkl = open('teams.pickle', 'wb')
	pickle.dump(teams, pkl)
else:
	pkl = open('teams.pickle', 'rb')
	teams = pickle.load(pkl)


weekToBacktest = 11
weeksToLookback = 5

for _,team in teams.items():
	print(team.name + ' ' + str(team.id))

X, Y = generateDataAndLabels(teams, weeksToLookback, weekToBacktest)
print(X)
print(Y)
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X, Y)
