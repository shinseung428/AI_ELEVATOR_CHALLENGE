import numpy as np 
from Elevator import Elevator
from Passenger import Passenger 

class Switch(object):
	def __init__(self):
		self.up = " "
		self.down = " "

	def reset(self):
		self.up = " "
		self.down = " "

class Building(object):
	def __init__(self, total_elevator_num, height):
		self.target = 0

		self.total_elevator_num = total_elevator_num
		
		#each elevator has max capacity of 10
		self.elevators = []
		for idx in range(total_elevator_num):
			self.elevators.append(Elevator(idx, 10, height))

		self.height = height
		self.people_in_floors = []
		self.floor_button = []
		for idx in range(height):
			self.people_in_floors.append(0)
			self.floor_button.append(Switch())

	def get_reward(self):
		return self.people_in_floors[0]

	def get_state(self):
		res = [elem for elem in self.people_in_floors]
		for e in self.elevators:
			res.append(e.curr_floor)
			res.append(e.curr_people)

		return res

	def generate_people(self):
		#generate random people in building and button press in each floor
		for floor_num in range(1, self.height):
			if np.random.random() < 0.8:
				people = np.random.randint(1,3)
				self.people_in_floors[floor_num] += people
				self.target += people

 				# if np.random.random() < 0.5 and floor_num < self.height:
				# 	self.floor_button[floor_num].up = "^"
				# elif floor_num > 0:
				# 	self.floor_button[floor_num].down = "v"
		

	def perform_action(self, action):
		for idx,e in enumerate(self.elevators):
			if action[idx] == 4:
				self.people_in_floors[e.curr_floor] += e.unload_people()
			elif action[idx] == 3:
				self.people_in_floors[e.curr_floor] -= e.load_people(self.people_in_floors[e.curr_floor])
			elif action[idx] == 2:
				e.move_up()
			elif action[idx] == 1:
				e.move_down()		


	def print_building(self, step):
		for idx in reversed(range(1,self.height)):
			print "======================================================="
			print "= Floor #%02d ="%idx,
			for e in self.elevators:
				if e.curr_floor == idx:
					print "  Lift #%d"%e.idx,
				else:
					print "         ",

			print " "
			# print "=   %c  %c   ="%(self.floor_button[idx].up, self.floor_button[idx].down),
			print "=  Waiting  =",
			for e in self.elevators:
				if e.curr_floor == idx:
					print "    %02d   "%e.curr_people,
				else:
					print "          ",
			print " "
			print "=    %03d    ="%self.people_in_floors[idx]


		print "======================================================="
		print "= Floor #00 =",
		for e in self.elevators:
			if e.curr_floor == 0:
				print "  Lift #%d"%e.idx,
			else:
				print "         ",

		print " "
		# print "=   %c  %c   ="%(self.floor_button[idx].up, self.floor_button[idx].down),
		print "=  Arrived  =",
		for e in self.elevators:
			if e.curr_floor == 0:
				print "    %02d   "%e.curr_people,
			else:
				print "          ",		
		print " "
		print "=    %03d    ="%self.people_in_floors[0]				
		print "======================================================="
		print ""
		print "People to move: %d "%(self.target - self.people_in_floors[0])
		print "Total # of people: %d"%self.target
		print "Step: %d"%step
