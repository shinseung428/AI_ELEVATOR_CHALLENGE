import os
import numpy as np
import tensorflow as tf

class Agent():
	def __init__(self, building_height, elevator_nums, actions):
		self.elevator_nums = elevator_nums
		self.actions = actions

	def get_action(self, state):
		#random action for each elevator
		return np.random.randint(0,self.actions, (self.elevator_nums))

	def update_network(self, states, actions, advantages, counter):
		pass

	def build_model(self):
		pass

	
	def build_loss(self):
		pass

	def save(self, num):
		pass

	def reload(self):
		pass