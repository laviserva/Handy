from OpenGL.GL import glBlendFunc, glUseProgram, glClearColor, glEnable, \
                    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_FALSE, GL_DEPTH_TEST, GL_BLEND, \
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glBindVertexArray, \
                    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_ARRAY_BUFFER, GL_STATIC_DRAW, glGenVertexArrays, \
                    glGenBuffers, glEnableVertexAttribArray, glVertexAttribPointer, GL_FLOAT, ctypes, glGenTextures \

from OpenGL.GL.shaders import compileProgram, compileShader

import sys
import os

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.Load_src import load_src
from utils.ObjectTexture_Loader import load_texture

class Shader:
    def __init__(self) -> None:
        self._vertex_src = load_src(os.path.join(parent_dir, "cpp", "vertex_src.c"))
        self._fragment_src = load_src(os.path.join(parent_dir, "cpp", "fragment_src.c"))
        self._shader = compileProgram(compileShader(self._vertex_src, GL_VERTEX_SHADER),
                                      compileShader(self._fragment_src, GL_FRAGMENT_SHADER))
        
        glUseProgram(self._shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class Object_parser:
    def __init__(self, objects: dict) -> None:
        self._objects = objects
        self._indices = []
        self._buffers = []
        self._VAOs = []
        self._VBOs = []
        
        for key in objects:
            self._indices.append(objects[key]["i"])
            self._buffers.append(objects[key]["b"])

    def _load_vertex(self):
        for obj in self._buffers:
            VAO = glGenVertexArrays(1)
            VBO = glGenBuffers(1)

            # bind VAO
            glBindVertexArray(VAO)

            # bind VBO
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferData(GL_ARRAY_BUFFER, obj.nbytes, obj, GL_STATIC_DRAW)

            # set attribute pointers
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj.itemsize * 8, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj.itemsize * 8, ctypes.c_void_p(12))

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj.itemsize * 8, ctypes.c_void_p(20))

            # unbind VBO and VAO
            # Uncomment to make sure that the object is invisible
            #glBindBuffer(GL_ARRAY_BUFFER, 0)
            #glBindVertexArray(0)

            # append VAO and VBO to their lists
            self._VAOs.append(VAO)
            self._VBOs.append(VBO)
    
    def _load_textures(self):
        for key in self._objects:
            textures = glGenTextures(1)
            load_texture(self._objects[key]["t"], textures)