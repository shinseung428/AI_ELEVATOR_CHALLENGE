import numpy as np 


class Elevator(object):
	def __init__(self, num, max_people, max_height):
		self.idx = num
		self.max_height = max_height
		self.dest_floors = []
		self.curr_floor = 0
		self.curr_people = 0

	def move_up(self):
		if self.curr_floor < self.max_height:
			self.curr_floor += 1

	def move_down(self):
		if self.curr_floor > 0:
			self.curr_floor -= 1

	def press_button(self, num):
		if num > 0 and num < max_height:
			self.dest_floors.append(num)


