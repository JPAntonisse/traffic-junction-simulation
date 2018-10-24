import os
import constants

PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


class Blank:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        return

    def get_type(self):
        return constants.BLANK
