from OpenGL.GL import glGetUniformLocation, glBlendFunc, glClear, glUseProgram, glClearColor, glEnable, glViewport, \
                    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_DEPTH_BUFFER_BIT, GL_FALSE, GL_DEPTH_TEST, GL_BLEND, \
                    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, glUniformMatrix4fv, glBindVertexArray, \
                    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_ARRAY_BUFFER, GL_STATIC_DRAW, glGenVertexArrays, \
                    glGenBuffers, glEnableVertexAttribArray, glVertexAttribPointer, GL_FLOAT, ctypes, glGenTextures, \
                    glBindTexture, GL_TEXTURE_2D, glDrawArrays, GL_TRIANGLES
from OpenGL.GL.shaders import compileProgram, compileShader

import glfw
import pyrr
import sys
import os

from typing import Tuple, List

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.Load_src import load_src
from utils.ObjectTexture_Loader import load_texture

class Renderer:
    def __init__(self, width: int=1280, height: int=720, title: str = "default name",
                 width_initpos: int = 400, height_initpos: int =200,
                 fovy: int = 45, z_near: float = 0.1, far: int = 100,
                 eye: List = [0, 0, 8], target: List = [0, 0, 0], up: List = [0, 1, 0],
                 cam = None
                 ):
        """Provide information to create a windows for render

        Args:
            width (int, optional): 
                Width size. Defaults to 1280.
            height (int, optional): 
                Height size. Defaults to 720.
            title (str, optional): 
                Title for the window. Defaults to "default name".
            width_initpos (int, optional): 
                Where should start width window. Defaults to 400.
            height_initpos (int, optional): 
                Where should start height window. Defaults to 200.
            fovy (int, optional): 
                Field of view in y direction in degrees. Defaults to 45.
            z_near (float, optional): 
                Distance from the viewer to the near clipping plane (only positive). Defaults to 0.1.
            far (int, optional): 
                Distance from the viewer to the far clipping plane (only positive). Defaults to 100.
            eye (List, optional): 
                Vector that specifies the position of the camera in 3D space.
            target (List, optional): 
                Vector that specifies the point towards which the camera is looking.
            up (List, optional): 
                Vector that specifies the upward direction of the camera.
            cam (Camera, optional): 
                Camera that modify how we see the render
        """
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        self._comprobe_ic(width, height, title, width_initpos, height_initpos)
        self._width  = width
        self._height = height
        self._title = title
        self._width_initpos = width_initpos
        self._height_initpos = height_initpos
        self.fovy = fovy     # field of view in y direction in degrees
        self.z_near = z_near  # distance from the viewer to the near clipping plane (only positive)
        self.far = far     # distance from the viewer to the far clipping plane (only positive)

        self._projection = pyrr.matrix44.create_perspective_projection_matrix(self.fovy, width / height, self.z_near, self.far)
        self._view = pyrr.matrix44.create_look_at(pyrr.Vector3(eye),
                                                  pyrr.Vector3(target),
                                                  pyrr.Vector3(up))
        # Utils for render
        self._window = None
        self._Shader = None

        # loc for Render
        self._model_loc = None
        self._proj_loc = None
        self._view_loc = None

        # functions
        self.functions = None
        self.keys_inputs = None # Key inputs
        self.cam = cam
    
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
        glfw.set_cursor_pos_callback(self._window, self._mouse_clb)
        glfw.set_key_callback(self._window, self.keys_inputs.keys_inputs)
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
    
    def _mouse_clb(self, window: glfw, xpos: float, ypos:float):
        mouse_pos = self._mouse_look_clb(window, xpos, ypos)
        self.cam.process_mouse_movement(mouse_pos[0], mouse_pos[1])
    
    def _mouse_look_clb(self, window: glfw, xpos: float, ypos:float) -> None:
        """
        Mouse position callback function
        """
        if self.cam.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.cam.first_mouse = False
        
        self.xoffset = xpos - self.lastX
        self.yoffset = self.lastY - ypos
        
        self.lastX = xpos
        self.lastY = ypos
        
        return self.xoffset, self.yoffset
    
    def _refresh_object(self, objects, model = None):
        glUniformMatrix4fv(self._model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, objects["Plane"]["len_i"])

    def _refresh_functions(self):
        if self.functions:
            for f in self.functions:
                f()

    def render(self, objects: dict, function: callable = None):
        """Create windows, load shaders and refresh window"""
        self._create_window()
        self._load_shader()

        parser = Object_parser(objects)
        parser._load_vertex()
        parser._load_textures()

        self._while_loop(function, objects=objects)
    
    def _load_functions(self, functions):
        self.functions = functions

    def _while_loop(self, function: callable = None, objects = None):
        """while loop where objects will be refreshed"""
        while not glfw.window_should_close(self._window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._refresh_functions()
            if function:
                model = function(objects)
                self._refresh_object(objects, model = model)
            else:
                self._refresh_object(objects)
            glfw.swap_buffers(self._window)

        # terminate glfw, free up allocated resources
        glfw.terminate()

    def _window_resize(self, window: glfw, width: int, height: int):
        """Resize window callback helper"""
        glViewport(0, 0, width, height)
        self._projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(self._proj_loc, 1, GL_FALSE, self._projection)

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

#r = Renderer()
#r.render()