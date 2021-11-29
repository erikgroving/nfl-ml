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
# n_features --> Parameters * 2 --> 22
# Output --> Score Differential (T1 - T2)
def generateDataAndLabels(teams, weeksPerLabel):
	
	
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
def generateDataAndLabels(teams, weeksPerLabel):
	return X, Y


if not exists('teams.pickle'):
	scraper = Scraper()
	teams = scraper.scrape()
	pkl = open('teams.pickle', 'wb')
	pickle.dump(teams, pkl)
else:
	pkl = open('teams.pickle', 'rb')
	teams = pickle.load(pkl)


weekToBacktest = 8
weeksToLookback = 5

X, Y = generateDataAndLabels(teams, weeksToLookback)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
