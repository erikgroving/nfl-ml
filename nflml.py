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
def generateDataAndLabels(teams, curWeek, weeksPerLabel):
	week = 0 + weeksPerLabel
	data = []
	labels = []
	while week < curWeek:
		d, l = generateTrainingDataForWeek(teams, week, weeksPerLabel)
		data.append(d)
		labels.append(l)
		week += 1
	X = np.asarray(data)
	Y = np.asarray(labels)
	return X, Y

def generateTrainingDataForWeek(teams, week, weeksPerLabel):
	data = []
	labels = []
	for _,team in teams.items():
		d, l = generateInputAndLabel(team, week, weeksPerLabel)
		data.append(d)
		labels.append(l)
	X = np.asarray(data)
	Y = np.asarray(labels)
	return X, Y

def generateInputAndLabel(team, week, weeksPerLabel):
	features = []
	for i in range(week - weeksPerLabel, week):
		teamVec = np.zeros([32])
		oppVec = np.zeros([32])
		teamVec[team.id] = 1
		game = team.schedule[i]

		oppVec[game.opponent] = 1

		featureVec = np.empty([10])
		featureVec[0] = game.pointsFor
		featureVec[1] = game.pointsAgainst
		featureVec[2] = game.totalYards
		featureVec[3] = game.passYards
		featureVec[4] = game.rushYards
		featureVec[5] = game.turnovers
		featureVec[6] = game.defYdsAllowed
		featureVec[7] = game.defPassYards
		featureVec[8] = game.defRushYards
		featureVec[9] = game.defTurnovers
		
		feature = np.concatenate((teamVec, oppVec, featureVec), axis=0)
		features.append(feature)

	X = np.reshape(np.asarray(features), (-1))
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

X, Y = generateTrainingDataForWeek(teams, 10, 4)
#X, Y = generateDataAndLabels(teams, weeksToLookback, weekToBacktest)
print(X.shape)
print(Y)
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X, Y)
