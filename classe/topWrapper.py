
import classe, random, fetch
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import os


class topWrapper():

	def __init__(self):
		self.config_path = "config/config.txt"
		self.dataset_path = "DATA/data_train.txt"
		#config
		self.config = fetch.getConfig(pathToConfig=self.config_path)
		self.configSortie=fetch.getConfigSortie(self.config["FichierConfigSortie"])
		
		#dataset
		self.dataset = fetch.getEpoque(pathToDataSet=self.dataset_path)
		self.indiceInput = random.randrange(0,len(self.dataset))
		self.inputChoisie = np.asarray(self.dataset[self.indiceInput].data)

		self.output = np.asarray(self.configSortie)
		self.outputDesire = self.output[self.dataset[self.indiceInput].resultat]

		#network
		self.bestReseau = classe.reseaux(self.config)

	# les foncitons ici sont des bouttons
	def train(self):
		self.bestReseau.train(self.inputChoisie, self.outputDesire,1)


	def browse_dataset(self):
		self.dataset_path = askopenfilename()
		print(filename)

	def browse_config(self):
		self.config_path= askopenfilename()
		print(filename)
