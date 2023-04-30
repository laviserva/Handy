from utils.Camera import Camera
from utils.Config import GUI_config
from utils.glfw_render import Renderer
from utils.Keys import Keys_input
from utils.ObjectTexture_Loader import ObjLoader

from typing import List

import pyrr

class RendOs:
    GUI_ = GUI_config

    def __init__(self, ) -> None:
        # render properties
        self.width: int=1280
        self.height: int=720
        self.title: str = "default name"
        self.width_initpos: int = 400
        self.height_initpos: int =200
        self.fovy: int = 45
        self.z_near: float = 0.1
        self.far: int = 100
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

        # Camera
        self.cam = Camera()

        # 3D Model
        self.obj_model = None
    
    def load_model(self, obj_dir, texture_dir, all_objects = True, initial_position = [0, 0, 0]):
        self.obj_model = ObjLoader(obj_dir, texture_path=texture_dir, all_objects=all_objects)
        self.obj_model = self.obj_model.load_model()
        self.obj_model["Plane"]["init_pos"] = pyrr.matrix44.create_from_translation(pyrr.Vector3(initial_position))
    
    def run(self, function=None):
        renderer = Renderer(width = self.width, height =self.height, title = self.title, width_initpos = self.width_initpos,
                            height_initpos=self.height_initpos, fovy = self.fovy, z_near = self.z_near, far = self.far,
                            eye = self.eye, target = self.target, up = self.up,
                            )
        renderer.render(self.obj_model, function=function)