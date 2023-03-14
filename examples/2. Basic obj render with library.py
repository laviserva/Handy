import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

import sys
import os

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.glfw_render import Renderer
from utils.ObjectTexture_Loader import ObjLoader

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
plane_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
texture = r"D:\Proyectos\Handy\Resources\texture 1.png"
plane = ObjLoader(r"D:\Proyectos\Handy\Resources\plane_1.obj", texture_path=texture, all_objects=True)
plane = plane.load_model()

renderer = Renderer()
rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
model = pyrr.matrix44.multiply(rot_y, plane_pos)
renderer.render(plane, model=model)