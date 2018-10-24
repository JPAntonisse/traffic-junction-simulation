import os, csv, random
import numpy as np
import objects.factory
from objects import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def csv_to_map(file='map.csv'):
    map = []
    file = open(PACKAGE_ROOT + '\\' + file, 'r')
    with file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            y = []
            for idy, char in enumerate(row[0]):
                y.append(objects.factory.create_object(char, idx, idy))
            map.append(y)

    return np.array(map)


def find_objects(map, type):
    arr = []
    for x in np.arange(map.shape[0]):
        for y in np.arange(map.shape[1]):
            if map[x, y].get_type() == type:
                arr.append(map[x, y])

    return arr


def get_nearby_object(map, x, y, type):
    if map[x - 1, y].get_type() == type:
        return map[x - 1, y]
    if map[x + 1, y].get_type() == type:
        return map[x + 1, y]
    if map[x, y - 1].get_type() == type:
        return map[x, y - 1]
    if map[x, y + 1].get_type() == type:
        return map[x, y + 1]
    return False


def road_occupied(cars, x, y):
    for car in cars:
        if car.is_position(x, y):
            return True
    return False


def is_object(map, type, x, y):
    return map[x, y].get_type() == type


def find_neighbouring(array, x, y):
    neighbouring = []
    for item in array:
        if abs(x - item.pos_x) <= 1 and abs(y - item.pos_y) <= 1:
            neighbouring.append(item)
    return neighbouring


def direction(from_x, from_y, to_x, to_y):
    x = from_x - to_x
    y = from_y - to_y
    if x > 0:
        return 'north'
    if x < 0:
        return 'south'
    if y > 0:
        return 'west'
    if y < 0:
        return 'east'


def combine_crossings(map, crossings, cars):
    crossings = crossings.copy()
    clusters = []
    while len(crossings) is not 0:
        cross = [crossings.pop(0)]
        neighbours = find_neighbouring(crossings, cross[0].pos_x, cross[0].pos_y)
        for neighbour in neighbours:
            cross.append(neighbour)
            crossings.remove(neighbour)
        clusters.append(CombinedCrossing(cross, map, cars))
    return clusters
