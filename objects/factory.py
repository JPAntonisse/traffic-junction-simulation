import os
import constants
from objects import *

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def create_object(char, pos_x, pos_y):
    switcher = {
        constants.BLANK: Blank(pos_x, pos_y),
        constants.CAR: Car(pos_x, pos_y),
        constants.CROSSING: Crossing(pos_x, pos_y),
        constants.DESPAWN: Despawn(pos_x, pos_y),
        constants.SPAWN: Spawn(pos_x, pos_y),
        constants.ROAD: Road(pos_x, pos_y),
    }
    return switcher.get(char)
