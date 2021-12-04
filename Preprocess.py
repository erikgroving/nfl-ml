import numpy as np


class Preprocessor:

	def generateDataAndLabels(self, teams, curWeek, weeksPerLabel, scoreDifferential):
		week = 0 + weeksPerLabel
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
			d, l = self.generateInputAndLabel(team, week, weeksPerLabel, scoreDifferential)
			data.append(d)
			labels.append(l)
		X = np.asarray(data)
		Y = np.asarray(labels)
		return X, Y

	def generateInput(self, team, week, weeksPerLabel):
		features = []
		for i in range(week - weeksPerLabel, week):
			teamVec = np.zeros([32])
			oppVec = np.zeros([32])
			teamVec[team.id] = 1
			game = team.schedule[i]
			
			if game.opponentName == 'Week':
				game = team.schedule[i - 1] if i == week - 1 else team.schedule[i + 1]


			oppVec[game.opponent] = 1

			featureVec = np.empty([11])
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
			featureVec[10] = game.awayGame

			feature = np.concatenate((teamVec, oppVec, featureVec), axis=0)
			features.append(feature)

		game = team.schedule[week]
		X = np.reshape(np.asarray(features), (-1))
		
		featureVec = np.empty([2])
		featureVec[0] = team.id
		featureVec[1] = game.opponent

		X = np.append(X, featureVec, axis=0)
		return X

	def generateInputAndLabel(self, team, week, weeksPerLabel, scoreDifferential):
		game = team.schedule[week]
		X = self.generateInput(team, week, weeksPerLabel)
		Y = game.pointsFor + scoreDifferential > game.pointsAgainst
		return X, Y