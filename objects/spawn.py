import os, random
import numpy as np
import constants
import helpers
from objects import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Spawn:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.chance = constants.SPAWN_CHANCE

    def get_type(self):
        return constants.SPAWN

    def do_step(self, map, cars, despawns):
        if random.uniform(0, 1) < self.chance:
            self.spawn_car(map, cars, despawns)

    def spawn_car(self, map, cars, despawns):
        road = helpers.get_nearby_object(map, self.pos_x, self.pos_y, constants.ROAD)

        if helpers.road_occupied(cars, road.pos_x, road.pos_y) is False:
            cars.append(Car(road.pos_x, road.pos_y, helpers.direction(self.pos_x, self.pos_y, road.pos_x, road.pos_y)))
