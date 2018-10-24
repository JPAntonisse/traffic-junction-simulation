import os
import constants

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Crossing:
    combined_crossing = None
    exit_x, exit_y = None, None
    cars = []
    direction = ''
    entrance = ''

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.status = constants.LIGHT_RED

    def has_waiting_vehicles(self):
        if self.entrance is '':
            return False
        for car in self.cars:
            if self.entrance is 'north':
                if self.pos_x - 1 is car.pos_x and self.pos_y is car.pos_y:
                    return True
            if self.entrance is 'east':
                if self.pos_x is car.pos_x and self.pos_y + 1 is car.pos_y:
                    return True
            if self.entrance is 'south':
                if self.pos_x + 1 is car.pos_x and self.pos_y is car.pos_y:
                    return True
            if self.entrance is 'west':
                if self.pos_x is car.pos_x and self.pos_y - 1 is car.pos_y:
                    return True
        return False

    # GETTERS
    def get_type(self):
        return constants.CROSSING

    def get_direction(self):
        return self.direction

    def get_exit_coordinates(self):
        return [self.exit_x, self.exit_y]

    def get_random_crossing(self):
        return self.combined_crossing.random_crossing(self.pos_x, self.pos_y)

    # SETTERS
    def set_cars(self, cars):
        self.cars = cars

    def set_light(self, status):
        self.status = status

    def set_exit(self, x, y):
        self.exit_x = x
        self.exit_y = y

    def set_direction(self, direction):
        self.direction = direction

    def set_entrance(self, entrance):
        self.entrance = entrance

    def set_combined(self, combined_crossing):
        self.combined_crossing = combined_crossing
