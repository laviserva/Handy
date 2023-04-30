from utils.Camera import Camera
from utils.Config import GUI_config
from utils.glfw_render import Renderer
from utils.Keys import Keys_input
from utils.ObjectTexture_Loader import ObjLoader

from typing import List

import pyrr

from OpenGL.GL import glUniformMatrix4fv, GL_FALSE

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

        self.renderer = Renderer(width = self.width, height =self.height, title = self.title, width_initpos = self.width_initpos,
                            height_initpos=self.height_initpos, fovy = self.fovy, z_near = self.z_near, far = self.far,
                            eye = self.eye, target = self.target, up = self.up,
                            )

        # Camera Properties
        self.mouse_sensitivity:float = 0.25
        self.jaw:int = -90
        self.pitch:int = 0
        self.constrain_value:int = 90
        self.velocity:float = 0.05
        self.position: list[float] = [0.0, 0.0, 10.0]

        # Keys
        self.gui = GUI_config.GLFW
        self.keys_inputs = Keys_input(self.gui)
        self.renderer.keys_inputs = self.keys_inputs

        # Camera
        self.cam = Camera()

        # 3D Model
        self.obj_model = None

    def _camera_update_from_keys(self):
        commands = self.keys_inputs.do_movement()
        [self.cam.process_keyboard(com) for com in commands if com is not []]
        
        self.view = self.cam.get_view_matrix()
        glUniformMatrix4fv(self.renderer._view_loc, 1, GL_FALSE, self.view)

    
    def load_model(self, obj_dir, texture_dir, all_objects = True, initial_position = [0, 0, 0]):
        self.obj_model = ObjLoader(obj_dir, texture_path=texture_dir, all_objects=all_objects)
        self.obj_model = self.obj_model.load_model()
        self.obj_model["Plane"]["init_pos"] = pyrr.matrix44.create_from_translation(pyrr.Vector3(initial_position))
    
    def run(self, function=None):
        functions = self._to_refresh_loop()
        self.renderer._load_functions(functions)
        self.renderer.render(self.obj_model, function=function)

    def _to_refresh_loop(self):
        functions = [
            self._camera_update_from_keys
            ]
        return functions