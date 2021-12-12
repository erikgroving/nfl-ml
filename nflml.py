from Scraper import Scraper
from Scraper import Team
from Preprocess import Preprocessor
from XGBModel import XGBModel
from RandomForest import RandomForest
from NeuralNet import NeuralNet
import pickle
from os.path import exists





if not exists('teams.pickle'):
	scraper = Scraper()
	teams = scraper.scrape()
	pkl = open('teams.pickle', 'wb')
	pkl2 = open('teams2.pickle', 'wb')
	pickle.dump(teams, pkl)
	pickle.dump(Team.idToTeam, pkl2)
else:
	pkl = open('teams.pickle', 'rb')
	pkl2 = open('teams2.pickle', 'rb')
	teams = pickle.load(pkl)
	Team.idToTeam = pickle.load(pkl2)
weekToPredict = 11
weeksToLookback = 4
scoreDifferential = 0

preproc = Preprocessor()
weekToStart = 6
weekToEnd = 12
numTotal = 0
numCorrect = 0
for i in range(weekToStart, weekToEnd):
	train_X, train_Y = preproc.generateDataAndLabels(teams, i, weeksToLookback, scoreDifferential)
	test_X, test_Y = preproc.generateTrainingDataForWeek(teams, i, weeksToLookback, scoreDifferential)
	print(train_X.shape)
	print(train_Y.shape)
	
	model = NeuralNet(train_X.shape[1])
	model.double()
	#model = RandomForest()
	#model = XGBModel()
	model.trainModel(train_X, train_Y)
	nC, nT = model.backtestModel(test_X, test_Y)
	#nC, nT = model.backtestModel(train_X, train_Y)
	numCorrect += nC
	numTotal += nT 

	print('Week ' + str(i) + ' Accuracy: ' + str(nC/nT))
print('Overall Accuracy: ' + str(numCorrect/numTotal))





