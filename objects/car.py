import os
import constants
import helpers

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Car:

    passed_crossing = False

    def __init__(self, pos_x, pos_y, direction='north'):
        self.direction = direction
        self.waiting_time = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        # print('spawning car on: ' + str(pos_x) + ' ' + str(pos_y) + ', facing: ' + direction)
        return

    def get_type(self):
        return constants.CAR

    def is_position(self, x, y):
        return self.pos_x == x and self.pos_y == y

    def do_step(self, map, cars):
        self.passed_crossing = False
        next_x = self.pos_x
        next_y = self.pos_y
        if self.direction == 'north':
            next_x -= 1
        if self.direction == 'south':
            next_x += 1
        if self.direction == 'west':
            next_y -= 1
        if self.direction == 'east':
            next_y += 1

        # Check for Despawns
        if helpers.is_object(map, constants.DESPAWN, next_x, next_y):
            return cars.remove(self)

        # Check for cars
        if helpers.road_occupied(cars, next_x, next_y):
            self.waiting_time += 1
            return

        # Check for lights
        if helpers.is_object(map, constants.CROSSING, next_x, next_y):
            if map[next_x, next_y].status is constants.LIGHT_GREEN:
                crossing = map[next_x, next_y].get_random_crossing()
                [next_x, next_y] = crossing.get_exit_coordinates()
                if helpers.road_occupied(cars, next_x, next_y):
                    self.waiting_time += 1
                    return
                self.direction = crossing.get_direction()
                self.passed_crossing = True
            else:
                self.waiting_time += 1
                return

        # Move the fuck
        self.pos_x = next_x
        self.pos_y = next_y
        self.waiting_time = 0
