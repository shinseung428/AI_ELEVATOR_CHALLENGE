import numpy as np
import os
from Building import Building
from Agent import Agent

#====================================================================================


#====================================================================================

lift_num = 1
buliding_height = 5
#Create building with 2 elevators, and height 10
building = Building(lift_num, buliding_height)
# building.generate_people()

agent = Agent(buliding_height, lift_num, 5)

#The goal is to bring down all the people in the building to the ground floor
max_steps = 1000
agent.reload()

building.generate_people()
for step in range(max_steps):
	ave_reward = 0
	

	os.system('clear')
	state = building.get_state()
	state_input = np.array(state).reshape(1,-1)
	action = agent.get_action(state_input)
	building.perform_action(action)
	reward = building.get_reward()	
	
	building.increment_wait_time()
	building.print_building(step)
	raw_input("enter:")


	