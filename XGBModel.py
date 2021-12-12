import xgboost as xgb
import numpy as np
class XGBModel:

	def __init__(self, numRounds = 50, max_depth=4, eta = 1, objective='binary:logistic'):
		self.numRounds = numRounds
		self.params = {'max_depth': max_depth, 'eta': eta, 'objective': objective, 'eval_metric': 'logloss'}
		return

	def trainModel(self, X_train, Y_train):
		dtrain = xgb.DMatrix(X_train, label=Y_train)
		self.model = xgb.train(self.params, dtrain, self.numRounds)

	def backtestModel(self, X_test, Y_test):
		dtest = xgb.DMatrix(X_test)
		prediction = self.model.predict(dtest)
		numCorrect = 0
		numTotal = 0
		for i in range(len(prediction)):
			pred = True if prediction[i] > 0.5  else False
			numTotal += 1
			numCorrect = numCorrect + 1 if pred == Y_test[i] else numCorrect
		return numCorrect, numTotal 

	def predict(self, X):
		dX = xgb.DMatrix(np.reshape(X, (1, -1)))
		return self.model.predict(dX)