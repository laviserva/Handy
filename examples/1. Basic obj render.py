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

from utils.load_src import load_src
from utils.obj_loader import *

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))

vertex_src = load_src(os.path.join(parent_dir, "cpp", "vertex_src.c"))
fragment_src = load_src(os.path.join(parent_dir, "cpp", "fragment_src.c"))

# load here the 3d meshes
chibi_indices, chibi_buffer = ObjLoader.load_model(r"D:\Proyectos\Handy\Resources\plane_1.obj")
monkey_indices, monkey_buffer = ObjLoader.load_model(r"D:\Proyectos\Handy\Resources\cubo.obj")

# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# VAO and VBO
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
# EBO = glGenBuffers(1)

# Chibi VAO
glBindVertexArray(VAO)
# Chibi Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, chibi_buffer.nbytes, chibi_buffer, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, chibi_indices.nbytes, chibi_indices, GL_STATIC_DRAW)

# chibi vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(0))
# chibi textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(12))
# chibi normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

textures = glGenTextures(1)
load_texture(r"D:\Proyectos\Handy\Resources\texture 1.png", textures)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, chibi_pos)

    # draw the chibi character
    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, textures)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(chibi_indices))
    # glDrawElements(GL_TRIANGLES, len(chibi_indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()