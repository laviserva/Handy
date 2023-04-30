from enum import Enum, auto

class GUI(Enum):
    GLFW = auto()

class Keys(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()