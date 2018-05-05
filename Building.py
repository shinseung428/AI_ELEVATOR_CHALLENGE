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
	def __init__(self, total_elevator_num, height, max_people):
		self.target = 0

		self.total_elevator_num = total_elevator_num
		self.max_people_in_floor = max_people

		#each elevator has max capacity of 10
		self.elevators = []
		for idx in range(total_elevator_num):
			self.elevators.append(Elevator(idx, 10, height))

		self.height = height
		self.people_in_floors = []
		self.floor_button = []
		for idx in range(height):
			self.people_in_floors.append([])
			self.floor_button.append(Switch())

	def get_reward(self):
		res = self.get_arrived_people()
		# if res == 0:
		# 	res = -1
		return res
		
	def get_arrived_people(self):
		return len(self.people_in_floors[0])

	def get_wait_time(self):
		total = 0
		for people in self.people_in_floors[1:]:
			for p in people:
				total += p.wait_time

		for elevator in self.elevators:
			for p in elevator.curr_people:
				total += p.wait_time
		return total

	def get_state(self):
		res = [len(elem)/self.max_people_in_floor for elem in self.people_in_floors]
		for e in self.elevators:
			res.append(e.curr_floor/self.height)
			res.append(len(e.curr_people)/e.max_people)
		return res

	def empty_building(self):
		self.people_in_floors = []
		for idx in range(self.height):
			self.people_in_floors.append([])

	def generate_people(self, prob):
		#generate random people in building and button press in each floor
		for floor_num in range(1, self.height):
			if np.random.random() < prob and len(self.people_in_floors[floor_num]) < self.max_people_in_floor:
				people = np.random.randint(1,6)
				if len(self.people_in_floors[floor_num]) + people > self.max_people_in_floor:
					people = self.max_people_in_floor - (len(self.people_in_floors[floor_num]) + people)

				tmp_list = []
				for p in range(people):
					tmp_list.append(Passenger())
				self.people_in_floors[floor_num] += tmp_list
				self.target += people

 				# if np.random.random() < 0.5 and floor_num < self.height:
				# 	self.floor_button[floor_num].up = "^"
				# elif floor_num > 0:
				# 	self.floor_button[floor_num].down = "v"
		
	def perform_action(self, action):
		for idx,e in enumerate(self.elevators):
			if action[idx] == 3:
				res = e.unload_people(self.people_in_floors[e.curr_floor], self.max_people_in_floor)
				for p in res:
					self.people_in_floors[e.curr_floor].append(p)
			elif action[idx] == 2:
				self.people_in_floors[e.curr_floor] = e.load_people(self.people_in_floors[e.curr_floor])
			elif action[idx] == 1:
				e.move_up()
			elif action[idx] == 0:
				e.move_down()

	def increment_wait_time(self):
		for people in self.people_in_floors[1:]:
			for p in people:
				p.wait_time+=1

		for elevator in self.elevators:
			for p in elevator.curr_people:
				p.wait_time+=1

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
					print "    %02d   "%len(e.curr_people),
				else:
					print "          ",
			print " "
			print "=    %03d    ="%len(self.people_in_floors[idx])


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
				print "    %02d   "%len(e.curr_people),
			else:
				print "          ",		
		print " "
		print "=    %03d    ="%len(self.people_in_floors[0])
		print "======================================================="
		print ""
		print "People to move: %d "%(self.target - len(self.people_in_floors[0]))
		print "Total # of people: %d"%self.target
		print "Step: %d"%step
