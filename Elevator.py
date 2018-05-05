import numpy as np 


class Elevator(object):
	def __init__(self, num, max_people, max_height):
		self.idx = num
		self.max_height = max_height
		self.max_people = max_people
		#we don't need this right now since everyone's going down to the ground floor 
		# self.dest_floors = []
		self.curr_floor = 0
		self.curr_people = []

	def move_up(self):
		if self.curr_floor < self.max_height-1:
			self.curr_floor += 1

	def move_down(self):
		if self.curr_floor > 0:
			self.curr_floor -= 1

	# def press_button(self, dest_floor):
	# 	if dest_floor > 0 and dest_floor < max_height:
	# 		self.dest_floors.append(dest_floor)


	def load_people(self, people_in_floor):
		res = 0
		if len(people_in_floor) > (self.max_people - len(self.curr_people)):
			res = people_in_floor[self.max_people - len(self.curr_people):]
			# self.curr_people += (self.max_people - self.curr_people)
			for p in people_in_floor[:self.max_people - len(self.curr_people)]:
				self.curr_people.append(p)
		else:
			for p in people_in_floor:
				self.curr_people.append(p)
			# self.curr_people += people_in_floor
			res = []
		
		return res

		# dest_floor = np.random.randint(floor+1,self.max_height) if button.up == "^" else np.random.randint(0,floor-1)		
		# if not dest_floor in self.dest_floors:
		# 	self.dest_floors.append(dest_floor)
		# sorted(self.dest_floors)

	def unload_people(self, people_in_floor, max_capacity):
		num_in_floor = len(people_in_floor)
		num_in_lift = len(self.curr_people)
		res = self.curr_people
		if self.curr_floor == 0 or num_in_floor + num_in_lift < max_capacity:
			self.curr_people = []
		else:
			self.curr_people = res[0:num_in_floor + num_in_lift - max_capacity]
			res = res[num_in_floor + num_in_lift - max_capacity:]

		return res














