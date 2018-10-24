import os, csv, random
import matplotlib.pyplot as plt
import numpy as np
import constants
import objects.factory
from objects import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def normalized_waiting_time(cars):
    total_waiting_time = 0
    if len(cars) is 0:
        return 0
    for car in cars:
        total_waiting_time += car.waiting_time
    return total_waiting_time / len(cars)


def cars_passed_crossing(cars):
    passed = 0
    for car in cars:
        if car.passed_crossing:
            passed += 1
    return passed


def update_statistics(map, cars, spawns, crossings, combined_crossings):
    return [
        normalized_waiting_time(cars),
        len(cars),
        cars_passed_crossing(cars)
    ]


def show_graph(statistics):
    plt.figure()
    plt.title('Spawn Rate: ' + str(constants.SPAWN_CHANCE) + ', mode: ' + str(constants.CROSSING_MODE))
    plt.plot(np.arange(len(statistics)), [item[0] for item in statistics], label='Average Waiting Time in steps')
    plt.xlabel('Steps')
    plt.ylabel('Average Vehicle Waiting Time')
    plt.legend()

    plt.figure()
    plt.title('Spawn Rate: ' + str(constants.SPAWN_CHANCE) + ', mode: ' + str(constants.CROSSING_MODE))
    plt.plot(np.arange(len(statistics)), [item[1] for item in statistics], label='Amount of Vehicles')
    plt.xlabel('Steps')
    plt.ylabel('Amount of Vehicles')
    plt.legend()

    plt.figure()
    plt.title('Spawn Rate: ' + str(constants.SPAWN_CHANCE) + ', mode: ' + str(constants.CROSSING_MODE))
    plt.plot(np.arange(len(statistics)), [item[2] for item in statistics], label='Cars passed a crossing')
    plt.xlabel('Steps')
    plt.ylabel('Cars')
    plt.legend()

    plt.show()


def show_ten_fold_graph(clock_stat, plate_stat):
    plt.figure()
    plt.plot(np.arange(0.1, 1.1, 0.1), clock_stat[0], label='Clock Mode')
    plt.plot(np.arange(0.1, 1.1, 0.1), plate_stat[0], label='Plate Mode')
    plt.xlabel('Vehicle Spawn Rate')
    plt.ylabel('Ten Fold Average Vehicle Waiting Time')
    plt.legend()

    plt.figure()
    plt.plot(np.arange(0.1, 1.1, 0.1), clock_stat[1], label='Clock Mode')
    plt.plot(np.arange(0.1, 1.1, 0.1), plate_stat[1], label='Plate Mode')
    plt.xlabel('Vehicle Spawn Rate')
    plt.ylabel('Ten Fold Average Amount of Vehicles')
    plt.legend()

    plt.figure()
    plt.plot(np.arange(0.1, 1.1, 0.1), clock_stat[2], label='Clock Mode')
    plt.plot(np.arange(0.1, 1.1, 0.1), plate_stat[2], label='Plate Mode')
    plt.xlabel('Vehicle Spawn Rate')
    plt.ylabel('Ten Fold Average Vehicle Crossed')
    plt.legend()

    plt.show()
