import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

import sys
import os

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
resources_dir = os.path.join(parent_dir, "Resources")
sys.path.append(parent_dir)

from utils.glfw_render import Renderer
from utils.ObjectTexture_Loader import ObjLoader

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

texture_dir = os.path.join(resources_dir, r"texture 1.png")
obj_dir = os.path.join(resources_dir, r"plane_1.obj")

plane = ObjLoader(obj_dir, texture_path=texture_dir, all_objects=True)
plane = plane.load_model()
plane["Plane"]["init_pos"] = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))

def rotation(plane):
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, plane["Plane"]["init_pos"])
    return model

renderer = Renderer()
renderer.render(plane, function=rotation)