import numpy as np
from Building import Building


#Create building with 2 elevators, and height 10
building = Building(4, 10)


building.print_building()
building.elevators[0].move_up()
building.generate_people()


building.print_building()