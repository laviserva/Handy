from abc import ABC, abstractclassmethod

class Renderer(ABC):

    @abstractclassmethod
    def _comprobe_ic(self):
        ...

    @abstractclassmethod
    def _create_window(self):
        ...

    @abstractclassmethod
    def _get_monitor_shape(self):
        ...

    @abstractclassmethod
    def _load_shader(self):
        ...

    @abstractclassmethod
    def _mouse_clb(self):
        ...

    @abstractclassmethod
    def _mouse_look_clb(self):
        ...

    @abstractclassmethod
    def _refresh_object(self):
        ...

    @abstractclassmethod
    def _refresh_functions(self):
        ...

    @abstractclassmethod
    def render(self):
        ...

    @abstractclassmethod
    def _load_functions(self):
        ...

    @abstractclassmethod
    def _while_loop(self):
        ...

    @abstractclassmethod
    def _window_resize(self):
        ...

class GLFW_Renderer(Renderer):
    def __init__(self):
        super().__init__()