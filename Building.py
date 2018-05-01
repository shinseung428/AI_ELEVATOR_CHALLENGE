import numpy as np 
from Elevator import Elevator

class Building(object):
	def __init__(self, total_elevator_num, height):
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
			self.floor_button.append(("N","N"))

	def generate_people(self):
		#generate random people in building and button press in each floor
		for floor_num in range(self.height):
			if np.random.random() < 0.3:
				self.people_in_floors[floor_num] += np.random.randint(1,5)
				if np.random.random() < 0.5:
					self.floor_button[floor_num] = ("U","N")
				else:
					self.floor_button[floor_num] = ("N","D")


	def load_people(self, num):
		pass

	def print_building(self):
		for idx in reversed(range(0,self.height)):
			print "===================================================="
			print "= Floor #%d ="%idx,
			for e in self.elevators:
				if e.curr_floor == idx:
					print "  Lift #%d"%e.idx,
				else:
					print "         ",

			print " "
			print "=   %c  %c   ="%(self.floor_button[idx][0], self.floor_button[idx][1]),
			for e in self.elevators:
				if e.curr_floor == idx:
					print "    %02d   "%e.curr_people,
				else:
					print "          ",
			print " "
			print "=    %02d"%self.people_in_floors[idx], "   ="
		print "===================================================="
