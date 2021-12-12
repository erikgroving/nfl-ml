import numpy as np
import torch
from torch import nn
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torchvision import transforms

class NeuralNet(nn.Module):

	def __init__(self, n_features):
		super().__init__()
		self.n_features = n_features
		self.loss_function = nn.BCELoss()
		self.epochs = 100
		l1_size = 128
		l2_size = 16
		self.layers = nn.Sequential(
			nn.Flatten(),
			nn.Linear(n_features, l1_size),
			nn.Dropout(p=0.1),
			nn.ReLU(),
			nn.Linear(l1_size, l2_size),
			nn.Dropout(p=0.1),
			nn.ReLU(),
			nn.Linear(l2_size, 1),
			nn.Sigmoid()
		)



	def trainModel(self, X_tr, Y_tr):
		X_train = torch.from_numpy(X_tr)
		Y_train = torch.from_numpy(Y_tr).to(torch.double)
		Y_train = torch.reshape(Y_train, (-1, 1))
		dataset = TensorDataset(X_train, Y_train)
		loader = DataLoader(dataset, batch_size=24)
		optimizer = torch.optim.Adam(self.parameters(), lr=1e-6)
		for epoch in range(self.epochs):
			for i, data in enumerate(loader):
				inputs, targets = data


				optimizer.zero_grad()
				outputs = self.layers(inputs)
				loss = self.loss_function(outputs, targets)

				loss.backward()

				optimizer.step()


	def backtestModel(self, X_te, Y_te):
		X_test = torch.from_numpy(X_te)
		Y_test = torch.from_numpy(Y_te).to(torch.double)
		Y_test = torch.reshape(Y_test, (-1, 1))
		prediction = self.layers(X_test)
		numCorrect = 0
		numTotal = 0
		for i in range(len(prediction)):
			pred = True if prediction[i] > 0.5  else False
			numTotal += 1
			numCorrect = numCorrect + 1 if pred == Y_test[i] else numCorrect
		return numCorrect, numTotal 

	def predict(self, X):
		x_ = torch.from_numpy(X)
		self.layers(x_)