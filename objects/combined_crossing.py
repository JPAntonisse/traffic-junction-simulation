import os, random
import constants
from helpers import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class CombinedCrossing:
    bottom_left, top_right, bottom_right, top_left = 0, 0, 0, 0
    exits, entrances = [], []

    clock_remaining = 0  # Time the current traffic stays on a certain thing
    current_active = ''

    def __init__(self, crossings, map, cars):
        # self.bottom_left, self.top_right, self.bottom_right, self.top_left = 0, 0, 0, 0
        self.exits = []
        self.entrances = []
        self.cars = cars
        self.mode = constants.CROSSING_MODE
        self.crossings = crossings
        self.set_crossings()
        self.set_exits(map)
        self.set_entrances(map)
        self.set_lights()

    def do_step(self, map):
        self.clock_remaining -= 1
        if self.mode == 'clock':
            if self.clock_remaining <= 0:
                self.clock_step()
        elif self.mode == 'plate':
            if self.clock_remaining <= 0:
                self.plate_step()
        return

    def set_lights(self):
        if self.mode == 'clock':
            self.top_left.set_light(constants.LIGHT_GREEN)
            self.current_active = 'north'
            self.clock_remaining = constants.GREEN_TIME
        elif self.mode == 'plate':
            return
        return

    def plate_step(self):
        self.all_red()
        busy_crossing = []
        for crossing in self.crossings:
            if crossing.has_waiting_vehicles():
                busy_crossing.append(crossing)

        if len(busy_crossing) is 0:
            return
        if len(busy_crossing) is 1:
            busy_crossing[0].set_light(constants.LIGHT_GREEN)
            self.current_active = busy_crossing[0].get_direction()
            self.clock_remaining = constants.GREEN_TIME
            return
        if len(busy_crossing) > 1:
            if self.current_active is '':
                busy_crossing[0].set_light(constants.LIGHT_GREEN)
                self.current_active = busy_crossing[0].get_direction()
                self.clock_remaining = constants.GREEN_TIME
            else:
                # Get the next busy crossing turn it to green
                next_exit = self.exits[(self.exits.index(self.current_active) + 1) % len(self.exits)]
                while self.get_next_exit(next_exit) not in busy_crossing:
                    next_exit = self.exits[(self.exits.index(next_exit) + 1) % len(self.exits)]
                next = self.get_next_exit(next_exit)
                self.current_active = next_exit
                next.set_light(constants.LIGHT_GREEN)
                self.clock_remaining = constants.GREEN_TIME
            return

        return

    def clock_step(self):
        next_exit = self.exits[(self.exits.index(self.current_active) + 1) % len(self.exits)]
        next = self.get_next_exit(next_exit)

        self.all_red()

        self.current_active = next_exit
        next.set_light(constants.LIGHT_GREEN)
        self.clock_remaining = constants.GREEN_TIME

    def get_next_exit(self, next_exit):
        if next_exit is 'north':
            return self.top_left
        if next_exit is 'east':
            return self.top_right
        if next_exit is 'south':
            return self.bottom_right
        if next_exit is 'west':
            return self.bottom_left

    def set_crossings(self):
        top_left = self.crossings[0]
        for crossing in self.crossings:
            crossing.set_cars(self.cars)
            crossing.set_combined(self)
            if crossing.pos_x < top_left.pos_x or crossing.pos_y < top_left.pos_y:
                top_left = crossing
        for crossing in self.crossings:
            if crossing.pos_x == top_left.pos_x + 1 and crossing.pos_y == top_left.pos_y:
                self.bottom_left = crossing
            if crossing.pos_x == top_left.pos_x and crossing.pos_y == top_left.pos_y + 1:
                self.top_right = crossing
            if crossing.pos_x == top_left.pos_x + 1 and crossing.pos_y == top_left.pos_y + 1:
                self.bottom_right = crossing
        self.top_left = top_left

    def random_crossing(self, x, y):
        crossing = self.get_crossing(x, y)
        choices = self.exits.copy()
        # Remove the direction where the car came from
        if crossing.direction == 'north':
            choices.remove('east')
        if crossing.direction == 'east':
            choices.remove('south')
        if crossing.direction == 'south':
            choices.remove('west')
        if crossing.direction == 'west':
            choices.remove('north')

        rdir = random.choice(choices)

        for crossing in self.crossings:
            if crossing.direction == rdir:
                return crossing

    def set_exits(self, map):
        if map[self.top_left.pos_x, self.top_left.pos_y - 1].get_type() == constants.ROAD:
            self.top_left.set_exit(self.top_left.pos_x, self.top_left.pos_y - 1)
            self.top_left.set_direction('west')
            self.exits.append('west')

        if map[self.top_right.pos_x - 1, self.top_right.pos_y].get_type() == constants.ROAD:
            self.top_right.set_exit(self.top_right.pos_x - 1, self.top_right.pos_y)
            self.top_right.set_direction('north')
            self.exits.append('north')

        if map[self.bottom_right.pos_x, self.bottom_right.pos_y + 1].get_type() == constants.ROAD:
            self.bottom_right.set_exit(self.bottom_right.pos_x, self.bottom_right.pos_y + 1)
            self.bottom_right.set_direction('east')
            self.exits.append('east')

        if map[self.bottom_left.pos_x + 1, self.bottom_left.pos_y].get_type() == constants.ROAD:
            self.bottom_left.set_exit(self.bottom_left.pos_x + 1, self.bottom_left.pos_y)
            self.bottom_left.set_direction('south')
            self.exits.append('south')

    def set_entrances(self, map):
        if map[self.top_left.pos_x - 1, self.top_left.pos_y].get_type() == constants.ROAD:
            self.entrances.append('north')
            self.top_left.set_entrance('north')
        if map[self.top_right.pos_x, self.top_right.pos_y + 1].get_type() == constants.ROAD:
            self.entrances.append('east')
            self.top_right.set_entrance('east')
        if map[self.bottom_right.pos_x + 1, self.bottom_right.pos_y].get_type() == constants.ROAD:
            self.entrances.append('south')
            self.bottom_right.set_entrance('south')
        if map[self.bottom_left.pos_x, self.bottom_left.pos_y - 1].get_type() == constants.ROAD:
            self.entrances.append('west')
            self.bottom_left.set_entrance('west')

    def get_crossing(self, x, y):
        for crossing in self.crossings:
            if crossing.pos_x == x and crossing.pos_y == y:
                return crossing

    def all_red(self):
        for crossing in self.crossings:
            crossing.set_light(constants.LIGHT_RED)
