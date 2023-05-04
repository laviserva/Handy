from enum import Enum, auto
import glfw

from utils.Config import GUI_config
from utils.Config import Keys_config # Used in "do_movement" (eval) 

class Keys_input:
    def __init__(self,gui):
        self.gui = gui
        self.flag_GLFW = GUI_config.GLFW

        self.all_keys = {}
        
        import os
        import sys

        file_dir = __file__
        current_dir = os.path.dirname(file_dir)
        parentdir = os.path.dirname(current_dir)
        sys.path.append(parentdir)
        
        if self.gui == self.flag_GLFW:
            file = "keys.conf"
        else:
            file = "keys.conf"
            
        self.config_file = os.path.join(parentdir, "config", file)
        
        with open(self.config_file) as config_file:
            for line in config_file:
                split = line.split()
                if len(split) != 3:
                    raise Exception("file {} invalid".format(self.config_file))
                split[0] = split[0].split()[0]
                split[1] = split[1].split()[0]
                split[2] = split[2].split()[0]
            
                if self.gui == self.flag_GLFW:
                    name = "KEY_"
                else:
                    raise(Exception(ValueError("Invalid GUI, please use GLFW")))
                self.all_keys[int(split[1])] = [name + split[0], False, split[2]]

    def keys_inputs(self, *args):
        """
        Keyboard input callback
        """
        if self.gui == self.flag_GLFW:
            self.glfw_keys(*args)
    
    def glfw_keys(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        name = "glfw."
        try:
            self.conf_key_pressed = eval(str(name + self.all_keys[key][0]))
        except:
            self.conf_key_pressed = None
        
        if key == self.conf_key_pressed and action == glfw.PRESS:
            self.all_keys[key][1] = True
        elif key == self.conf_key_pressed and action == glfw.RELEASE:
            self.all_keys[key][1] = False
            
    def do_movement(self) -> None:
        """
        Do the movement, call this function in the main loop
        """
        coms = []
        
        for key in self.all_keys:
            if self.all_keys[key][1]:
                # Keys -> Variable name
                command = eval(str("Keys_config."+self.all_keys[key][2].upper())) # When key is pressed, select predesigned variable from Key_config
                coms.append(command) # In this way is possible to do more than 2 movements at the same time
        return coms