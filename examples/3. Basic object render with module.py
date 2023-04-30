import glfw
import pyrr

import sys
import os

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
resources_dir = os.path.join(parent_dir, "Resources")
sys.path.append(parent_dir)

from utils.RendOs import RendOs

texture_dir = os.path.join(resources_dir, r"texture 1.png")
obj_dir = os.path.join(resources_dir, r"plane_1.obj")

def rotation(plane):
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, plane["Plane"]["init_pos"])
    return model

render = RendOs()
render.load_model(obj_dir, texture_dir, initial_position=[0, -5, -10])
render.run(function=rotation)