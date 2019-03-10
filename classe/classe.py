import numpy as np
import random

class reseaux():

	def __init__(self,configOriginal):

		self.config = configOriginal

		i=0
		self.lay = []
		self.lay.append(np.random.uniform(-0.1,0.1,(self.config["nbTrames"]*26, self.config["neuroneEntree"])))
		self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneEntree"], self.config["neuroneCacher"][i])))
		i+=1
		while i <= self.config["nombreCoucheCachees"]-1:	
			self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneCacher"][i-1], self.config["neuroneCacher"][i])))
			i+=1
		self.lay.append(np.random.uniform(-0.1,0.1,(self.config["neuroneCacher"][i-1], self.config["neuroneSortie"])))

	def activation(self,inputs,arrayPoids):
		#return self.config["fonctionActivation"](np.dot(inputs,arrayPoids))
		return np.dot(inputs,arrayPoids)

	def test(self, input):
		activations=[]
		activations.append(self.activation(input,self.lay[0]))
		for i in range(self.config["nombreCoucheCachees"]+1):
			activations.append(self.activation(activations[i],self.lay[i+1]))
		return activations[-1] #output obtenue

	def train(self, input, outputDesire):

		
		#Activation
		activations=[]
		activations.append(self.activation(input,self.lay[0]))
		for i in range(self.config["nombreCoucheCachees"]+1):
			activations.append(self.activation(activations[i],self.lay[i+1]))
		
		SortieFuncActivation = []
		for i in range(len(activations)):
			sortieFuncActivation.append(self.config["fonctionActivation"](SortieFuncActivation[i]))
		
		#Signal d'erreur (Calcul des deltas d'erreur)
		if self.config["fonctionActivation"] == "sigmoide": #TODO savoir quoi vérifier ici
			deltas=[]
			deltas.insert(0,(outputDesire - sortieFuncActivation[-1])*self.config["fonctionActivation"](sortieFuncActivation[-1],deriv=True))
			for i in range(self.config["nombreCoucheCachees"]+1):
				deltas.insert(0,np.matmul(deltas[-1-i],self.lay[-1-i].T)*self.config["fonctionActivation"](sortieFuncActivation[-2-i],deriv=True)) 
		else:
			deltas=[]
			deltas.insert(0,(outputDesire - sortieFuncActivation[-1])*self.config["fonctionActivation"](activations[-1],deriv=True))
			for i in range(self.config["nombreCoucheCachees"]+1):
				deltas.insert(0,np.matmul(deltas[-1-i],self.lay[-1-i].T)*self.config["fonctionActivation"](activations[-2-i],deriv=True)) 

		#Correction
		omegasDeltas=[]
		omegasDeltas.append(self.config["tauxApprentissage"]*np.outer(input, deltas[0]))
		for i in range(self.config["nombreCoucheCachees"]+1):
			omegasDeltas.append(self.config["tauxApprentissage"]*np.outer(SortieFuncActivation[i], deltas[i+1]))
		
		#actualisation
		for i in range(self.config["nombreCoucheCachees"]+1):
			self.lay[i] += omegasDeltas[i]