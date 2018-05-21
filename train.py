import numpy as np
import os
from Building import Building
from Agent import Agent

#====================================================================================


#====================================================================================
#Building Setting
lift_num = 4
buliding_height = 10
max_people_in_floor = 30

add_people_at_step = 25
add_people_prob = 0.8

#Create building with 4 elevators, height 10, max people 30 in each floor
building = Building(lift_num, buliding_height, max_people_in_floor)

#Agent controls each elevator
agent = Agent(buliding_height, lift_num, 4)

#The goal is to bring down all the people in the building to the ground floor
batch_size = 64
epochs = 50
max_steps = 100
global_step = 0

for epoch in range(epochs):
	#generate poeple with 80% probability in each floor
	building.empty_building()
	building.generate_people(add_people_prob)
	for step in range(max_steps):
		states = []
		actions = []
		rewards = []
		ave_reward = 0
		if step % add_people_at_step == 0:
			building.generate_people(add_people_prob)

		for batch_idx in range(batch_size):
			os.system('clear')
			state = building.get_state()
			prev_people = building.get_arrived_people()
			state_input = np.array(state).reshape(1,-1)
			action = agent.get_action(state_input)
			building.perform_action(action)
			reward = building.get_reward(prev_people)
			
			states.append(state)
			actions.append(action)
			rewards.append(reward)
			
			ave_reward += reward
			building.increment_wait_time()
			building.print_building(step)
			# raw_input("")

			# add more people if everyone in the building are moved to the ground floor
			if building.get_arrived_people() == building.target:
				building.generate_people(add_people_prob)

			print "Epoch: %d Step: %d Average Reward: %.4f"%(epoch, step, ave_reward/batch_size)
		#update network here 
		agent.update_network(states, actions, rewards, step)
		# print "Epoch: %d Step: %d Average Reward: %.4f"%(epoch, step, ave_reward/batch_size)
		global_step += 1
	agent.save(global_step)

		# raw_input("enter:")
