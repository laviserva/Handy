from utils.Camera import Camera
from utils.Config import GUI_config
from utils.glfw_render import Renderer
from utils.Keys import Keys_input

from typing import List

class RendOs:
    GUI_ = GUI_config
    RENDER = Renderer

    def __init__(self) -> None:
        # render properties
        self.width: int=1280
        self.height: int=720
        self.title: str = "default name"
        self.width_initpos: int = 400
        self.height_initpos: int =200
        self.fovy: int = 45,
        self.z_near: float = 0.1
        self.far: int = 100,
        self.eye: List = [0, 0, 8]
        self.target: List = [0, 0, 0]
        self.up: List = [0, 1, 0]

        # Camera Properties
        self.mouse_sensitivity:float = 0.25
        self.jaw:int = -90
        self.pitch:int = 0
        self.constrain_value:int = 90
        self.velocity:float = 0.05
        self.position: list[float] = [0.0, 0.0, 10.0]

        # Keys
        self.gui = GUI_config.GLFW