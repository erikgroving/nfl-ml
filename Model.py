import xgboost as xgb
import numpy as np
class Model:

	def __init__(self, numRounds = 5000, max_depth=6, eta = 0.3, objective='binary:logistic'):
		self.numRounds = numRounds
		self.params = {'max_depth': max_depth, 'eta': eta, 'objective': objective, 'eval_metric': 'error'}
		return

	def trainModel(self, X_train, Y_train):
		dtrain = xgb.DMatrix(X_train, label=Y_train)
		self.model = xgb.train(self.params, dtrain, self.numRounds)

	def backtestModel(self, model, X_test, Y_test):
		return

	def predict(self, X):
		dX = xgb.DMatrix(np.reshape(X, (1, -1)))
		return self.model.predict(dX)