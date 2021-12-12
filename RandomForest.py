from sklearn.ensemble import RandomForestClassifier
class RandomForest:

	def __init__(self):
		self.model = RandomForestClassifier(n_estimators=1000)

	def trainModel(self, X_train, Y_train):
		self.model.fit(X_train, Y_train)

	def backtestModel(self, X_test, Y_test):
		prediction = self.model.predict(X_test)
		numCorrect = 0
		numTotal = 0
		for i in range(len(prediction)):
			pred = True if prediction[i] > 0.5  else False
			numTotal += 1
			numCorrect = numCorrect + 1 if pred == Y_test[i] else numCorrect

		print(numCorrect)
		print(numTotal)
		return numCorrect, numTotal 

	def predict(self, X):
		return self.model.predict(X)
