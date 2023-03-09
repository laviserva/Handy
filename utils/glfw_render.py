from OpenGL.GL import glGetUniformLocation, glBlendFunc, glClear, glUseProgram, glClearColor, glEnable, glViewport, \
                    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_DEPTH_BUFFER_BIT, GL_FALSE, GL_DEPTH_TEST, GL_BLEND, \
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, glUniformMatrix4fv
from OpenGL.GL.shaders import compileProgram, compileShader

import glfw
import pyrr
import sys
import os

from typing import Tuple

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.load_src import load_src

class Renderer:
    def __init__(self, width: int=1280, height: int=720, title: str = "default name",
                 width_initpos: int = 400, height_initpos: int =200,
                 ):
        """Provide information to create a windows for render

        Args:
            width (int, optional): width size. Defaults to 1280.
            height (int, optional): height size. Defaults to 720.
            title (str, optional): title for the window. Defaults to "default name".
            width_initpos (int, optional): where should start width window. Defaults to 400.
            height_initpos (int, optional): where should start height window. Defaults to 200.
        """
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        self._comprobe_ic(width, height, title, width_initpos, height_initpos)
        self._width  = width
        self._height = height
        self._title = title
        self._width_initpos = width_initpos
        self._height_initpos = height_initpos

        self._projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        self._view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]),
                                                  pyrr.Vector3([0, 0, 0]),
                                                  pyrr.Vector3([0, 1, 0]))
        
        self._window = None
        self._Shader = None

        self._model_loc = None
        self._proj_loc = None
        self._view_loc = None
    
    def _comprobe_ic(self, width, height, title, width_initpos, height_initpos):
        width_pt, height_pt = self._get_monitor_shape()

        if not isinstance(width, int):
            raise ValueError(f"int value expected. {type(width)} given")
        if not isinstance(height, int):
            raise ValueError(f"int value expected. {type(height)} given")
        if not isinstance(title, str):
            raise ValueError(f"str value expected. {type(title)} given")
        if not isinstance(width_initpos, int):
            raise ValueError(f"int value expected. {type(width_initpos)} given")
        if not isinstance(height_initpos, int):
            raise ValueError(f"int value expected. {type(height_initpos)} given")
        
        if width > width_pt:
            raise ValueError("width value greater than monitor width")
        if width < 200:
            raise ValueError("width value lower than minimum width: 200")
        
        if height > height_pt:
            raise ValueError("height value greater than monitor height")
        if height < 200:
            raise ValueError("height value lower than minimum height: 200")
        
        if len(title) > 30:
            raise ValueError("title lenght greater than maximum lenght: 30 characters")
        if len(title) < 3:
            raise ValueError("title lenght lower than minimum lenght: 3 characters")
                
        if width_initpos > width_pt - width:
            raise ValueError(f"width initial position value greater than monitor width reduce it")
        if width_initpos < 0:
            raise ValueError("width value lower than minimum width: 0")
        
        if height_initpos > height_pt - height:
            raise ValueError(f"height initial position value greater than monitor height reduce it")
        if height_initpos < 0:
            raise ValueError("height value lower than minimum height: 0")

        
    def _create_window(self):
        """From initial conditions, create window."""
        self._window = glfw.create_window(self._width, self._height, self._title, None, None)

        if not self._window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(self._window, self._width_initpos, self._height_initpos)
        glfw.set_window_size_callback(self._window, self._window_resize)
        glfw.make_context_current(self._window)
    
    def _get_monitor_shape(self) -> Tuple[int]:
        monitor = glfw.get_primary_monitor()
        width_pt, height_pt = glfw.get_monitor_workarea(monitor)[2:4]
        return width_pt, height_pt

    def _load_shader(self):
        """Load Shader"""
        self._Shader = Shader()

        self._model_loc = glGetUniformLocation(self._Shader._shader, "model")
        self._proj_loc = glGetUniformLocation(self._Shader._shader, "projection")
        self._view_loc = glGetUniformLocation(self._Shader._shader, "view")

        glUniformMatrix4fv(self._proj_loc, 1, GL_FALSE, self._projection)
        glUniformMatrix4fv(self._view_loc, 1, GL_FALSE, self._view)
    
    def render(self):
        """Create windows, load shaders and refresh window"""
        self._create_window()
        self._load_shader()
        self._while_loop()

    def _while_loop(self):
        """while loop where objects will be refreshed"""
        while not glfw.window_should_close(self._window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glfw.swap_buffers(self._window)

        # terminate glfw, free up allocated resources
        glfw.terminate()

    @staticmethod
    def _window_resize(window: glfw, width: int, height: int):
        """Resize window callback helper"""
        glViewport(0, 0, width, height)
        Renderer._projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(Renderer._proj_loc, 1, GL_FALSE, Renderer._projection)

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

#r = Renderer()
#r.render()