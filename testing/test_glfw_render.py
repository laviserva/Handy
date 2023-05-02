import os
import sys

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.Render_lib.glfw_render import GLFW_Renderer
import unittest

class Test_glfw_render(unittest.TestCase):
    print("\n")
    print("----------------------------------------------------------------------")
    print("Testing GLFW render")
    
    def test_init(self):

        self.assertRaises(ValueError, GLFW_Renderer, width="12")
        self.assertRaises(ValueError, GLFW_Renderer, width=0)
        self.assertRaises(ValueError, GLFW_Renderer, width=-8)

        self.assertRaises(ValueError, GLFW_Renderer, height="12")
        self.assertRaises(ValueError, GLFW_Renderer, height=0)
        self.assertRaises(ValueError, GLFW_Renderer, height=-8)

        self.assertRaises(ValueError, GLFW_Renderer, title="12")
        self.assertRaises(ValueError, GLFW_Renderer, title="1234567890123456789012345678901") # 31 characters
        self.assertRaises(ValueError, GLFW_Renderer, title=0)
        self.assertRaises(ValueError, GLFW_Renderer, title=-8)

        self.assertRaises(ValueError, GLFW_Renderer, width_initpos="12")
        self.assertRaises(ValueError, GLFW_Renderer, width_initpos=-8)

        self.assertRaises(ValueError, GLFW_Renderer, height_initpos="12")
        self.assertRaises(ValueError, GLFW_Renderer, height_initpos=-8)