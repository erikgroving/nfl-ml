from Scraper import Scraper
from Scraper import Team
from Preprocess import Preprocessor
from Model import Model
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
weekToPredict = 12
weeksToLookback = 4
scoreDifferential = 0

preproc = Preprocessor()
train_X, train_Y = preproc.generateDataAndLabels(teams, weekToPredict, weeksToLookback, scoreDifferential)



print(train_X.shape)
print(train_Y.shape)



model = Model()
model.trainModel(train_X, train_Y)
test_X = preproc.generateInput(teams['Bengals'], weekToPredict, weeksToLookback)
print(model.predict(test_X))
