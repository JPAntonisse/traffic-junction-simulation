import os, time
import numpy as np
import constants
from helpers import *
from screen import Screen
from statistics import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Board:
    map = None
    cars = []
    spawns = []
    despawns = []
    crossings = []
    combined_crossings = []

    def __init__(self, show_screen=True):
        self.show_screen = show_screen
        if self.show_screen:
            self.screen = Screen()
        # self.dimension = dimension
        # self.map = np.zeros((dimension, dimension), dtype=object)

    def main_loop(self, steps=100):
        statistics = []
        for x in np.arange(steps):
            # Do the step
            self.do_step()
            # Update the screen
            if self.show_screen:
                self.screen.set_text(self.to_string())
            # Update statistics
            statistics.append(
                update_statistics(self.map, self.cars, self.spawns, self.crossings, self.combined_crossings)
            )
            # Sleep if the simulation has to run slow
            if constants.SLEEP_TIME is not 0:
                time.sleep(constants.SLEEP_TIME)

        # self.screen.get_mouse()
        # Show Graphs
        return statistics

    def to_string(self):
        text = ''
        for x in np.arange(self.map.shape[0]):
            for y in np.arange(self.map.shape[1]):
                if road_occupied(self.cars, x, y):
                    text += constants.CAR
                elif self.map[x, y].get_type() is constants.CROSSING:
                    text += str(self.map[x, y].status)
                else:
                    text += self.map[x, y].get_type()
            text += '\n'
        return text

    # def initialize_blank_map(self):
    #     for x in np.arange(self.dimension):
    #         for y in np.arange(self.dimension):
    #             self.map[x, y] = Blank()
    #     return

    def read_map(self):
        self.map = csv_to_map('map.csv')
        self.spawns = find_objects(self.map, constants.SPAWN)
        self.despawns = find_objects(self.map, constants.DESPAWN)
        self.cars = find_objects(self.map, constants.CAR)
        self.crossings = find_objects(self.map, constants.CROSSING)
        self.combined_crossings = combine_crossings(self.map, self.crossings, self.cars)

    def do_step(self):
        # print('Do Step: Moving the Cars')
        self.move_cars()
        # print('Do Step: Spawning the Cars')
        self.spawn_cars()
        # print('Do Step: Setting Traffic Lights')
        self.do_crossings()

    def move_cars(self):
        for car in self.cars:
            car.do_step(self.map, self.cars)
        return

    def spawn_cars(self):
        for spawn in self.spawns:
            spawn.do_step(self.map, self.cars, self.despawns)

    def do_crossings(self):
        for combined_crossing in self.combined_crossings:
            combined_crossing.do_step(self.map)


def ten_fold_cycle():
    temperatures = np.arange(0.1, 1.1, 0.1)
    average_waiting_time = []
    average_vehicle_count = []
    average_vehicle_crossed = []

    for temp in temperatures:
        constants.SPAWN_CHANCE = temp
        waiting_time = []
        vehicle_count = []
        vehicle_crossed = []

        for i in np.arange(10):
            statistics = one_loop()
            waiting_time.append(np.average([item[0] for item in statistics]))
            vehicle_count.append(np.average([item[1] for item in statistics]))
            vehicle_crossed.append(np.average([item[2] for item in statistics]))

        average_waiting_time.append(np.average(waiting_time))
        average_vehicle_count.append(np.average(vehicle_count))
        average_vehicle_crossed.append(np.average(vehicle_crossed))

    return [average_waiting_time, average_vehicle_count, average_vehicle_crossed]


def ten_fold_spawn_decrease():
    constants.CROSSING_MODE = 'clock'
    clock_stat = ten_fold_cycle()

    constants.CROSSING_MODE = 'plate'
    plate_stat = ten_fold_cycle()

    show_ten_fold_graph(clock_stat, plate_stat)


def one_time():
    print('Starting simulation with Spawn Chance: ' + str(constants.SPAWN_CHANCE))
    a = Board(True)
    a.read_map()
    statistics = a.main_loop()

    show_graph(statistics)


def one_loop():
    print('initialiazing...')
    a = Board(False)
    print('Reading map...')
    a.read_map()
    print('Starting main loop...')
    return a.main_loop()


if __name__ == "__main__":
    ten_fold_spawn_decrease()