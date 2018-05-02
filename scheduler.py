import numpy as np
import os
from Building import Building
from Agent import Agent

#====================================================================================


#====================================================================================

lift_num = 4
buliding_height = 10
#Create building with 2 elevators, and height 10
building = Building(lift_num, buliding_height)
building.generate_people()

agent = Agent(buliding_height, lift_num, 5)

#The goal is to bring down all the people in the building to the ground floor


batch_size = 64
epochs = 50
max_steps = 1000


for epoch in range(epochs):
	for step in range(max_steps):
		states = []
		actions = []
		rewards = []
		ave_reward = 0
		for batch_idx in range(batch_size):

			# os.system('clear')
			state = building.get_state()
			state = np.array(state).reshape(1,-1)
			action = agent.get_action(state)
			
			building.perform_action(action)
			# building.print_building(step)
			reward = building.get_reward()
			
			step += 1
			states.append(state)
			actions.append(action)
			rewards.append(reward)
			ave_reward += reward
			# raw_input("enter:")


		#update network here 
		agent.update_network(states, actions, rewards, step)
		print "Epoch: %d Step: %d Reward: %.4f"%(epoch, step, ave_reward/batch_size)
