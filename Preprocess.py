import numpy as np

class Preprocessor:
	
	def generateDataAndLabels(self, teams, curWeek, weeksPerLabel, scoreDifferential):
		week = curWeek-1
		data = []
		labels = []
		while week < curWeek:
			d, l = self.generateTrainingDataForWeek(teams, week, weeksPerLabel, scoreDifferential)
			data.append(d)
			labels.append(l)
			week += 1

		X = data[0]
		Y = labels[0]
		for el in data[1:]:
			X = np.append(X, el, axis=0)
		for el in labels[1:]:
			Y = np.append(Y, el, axis=0)

		return X, Y

	def generateTrainingDataForWeek(self, teams, week, weeksPerLabel, scoreDifferential):
		data = []
		labels = []
		for _,team in teams.items():
			if team.schedule[week].opponentName == 'Week': 
				continue
			d, l = self.generateInputAndLabel(teams, team, week, weeksPerLabel, scoreDifferential)
			data.append(d)
			labels.append(l)
		X = np.asarray(data)
		Y = np.asarray(labels)
		return X, Y

	def generateGameFeatureVec(self, game):
		featureVec = np.empty([7])
		featureVec[0] = game.pointsFor
		featureVec[1] = game.pointsAgainst
		featureVec[2] = game.totalYards
		featureVec[3] = game.turnovers
		featureVec[4] = game.defYdsAllowed
		featureVec[5] = game.defTurnovers
		featureVec[6] = game.awayGame

		return featureVec


	def generateInput(self, teams, team, week, weeksPerLabel):
		features = []
		for idx in range(week - weeksPerLabel, week):
			game = team.schedule[idx]

			i = idx
			if game.opponentName == 'Week':
				i = idx - 1 if idx == week - 1 else idx + 1
			game = team.schedule[i]
			
			featureVec = self.generateGameFeatureVec(game)
			opponent = team.schedule[i].opponentName
			opponentTeam = teams[opponent]
			oppGame = opponentTeam.schedule[i]
			oppFeatureVec = self.generateGameFeatureVec(oppGame)
			feature = np.concatenate((featureVec, oppFeatureVec), axis=0)
			features.append(feature)

		game = team.schedule[week]
		X = np.reshape(np.asarray(features), (-1))
		
		featureVec = np.empty([1])
		featureVec[0] = game.awayGame

		X = np.append(X, featureVec, axis=0)
		return X
	
	def generateTestInput(self, teams, week, weeksPerLabel):
		data = []
		for _,team in teams.items():
			if team.schedule[week].opponentName == 'Week': 
				continue
			d = self.generateInput(team, week, weeksPerLabel)
			data.append(d)
		X = np.asarray(data)
		return X

		

	def generateInputAndLabel(self, teams, team, week, weeksPerLabel, scoreDifferential):
		game = team.schedule[week]
		X = self.generateInput(teams, team, week, weeksPerLabel)
		Y = game.pointsFor + scoreDifferential > game.pointsAgainst
		return X, Y