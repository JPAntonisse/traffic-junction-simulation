import os
import constants

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Despawn:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_type(self):
        return constants.DESPAWN
