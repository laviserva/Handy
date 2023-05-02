import os
import sys

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.Camera import Camera
import unittest

class Test_glfw_render(unittest.TestCase):
    print("\n")
    print("----------------------------------------------------------------------")
    print("Testing Camera")
    
    def test_init(self):

        self.assertRaises(ValueError, Camera, mouse_sensitivity="12")
        self.assertRaises(ValueError, Camera, mouse_sensitivity=0)
        self.assertRaises(ValueError, Camera, mouse_sensitivity=-8)
        self.assertRaises(ValueError, Camera, mouse_sensitivity=None)

        self.assertRaises(ValueError, Camera, jaw="12")
        self.assertRaises(ValueError, Camera, jaw=0.0)
        self.assertRaises(ValueError, Camera, jaw=-8.0)
        self.assertRaises(ValueError, Camera, jaw=None)

        self.assertRaises(ValueError, Camera, pitch="12")
        self.assertRaises(ValueError, Camera, pitch=0)
        self.assertRaises(ValueError, Camera, pitch=-8)
        self.assertRaises(ValueError, Camera, pitch=None)

        self.assertRaises(ValueError, Camera, constrain_value="12")
        self.assertRaises(ValueError, Camera, constrain_value=0)
        self.assertRaises(ValueError, Camera, constrain_value=-8)
        self.assertRaises(ValueError, Camera, constrain_value=None)

        self.assertRaises(ValueError, Camera, velocity="12")
        self.assertRaises(ValueError, Camera, velocity=0)
        self.assertRaises(ValueError, Camera, velocity=None)

        self.assertRaises(ValueError, Camera, position="12")
        self.assertRaises(ValueError, Camera, position=0)
        self.assertRaises(ValueError, Camera, position=[-8])
        self.assertRaises(ValueError, Camera, position=[-8, 1])
        self.assertRaises(ValueError, Camera, position=[-8, 8.3])
        self.assertRaises(ValueError, Camera, position=[-8.9, 1])
        self.assertRaises(ValueError, Camera, position=[-8.1, 8.3])
        self.assertRaises(ValueError, Camera, position=[-8, 1, 9])
        self.assertRaises(ValueError, Camera, position=None)

if __name__ == "__main__":
    unittest.main()