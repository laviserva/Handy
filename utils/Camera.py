import numpy as np
from utils.Config import Keys_config
from pyrr import Vector3, vector, vector3, matrix44

class Camera:
    def __init__(self, mouse_sensitivity:float = 0.25, jaw:int = -90,
                pitch:int = 0, constrain_value:int = 90, velocity:float = 0.05,
                position: list[float] = [0.0, 0.0, 10.0]) -> None:
        """
        Args:
            mouse_sensitivity (float, optional):
                Determines how much the camera should move in response to mouse movement. Defaults to 0.25.
            jaw (int, optional):
                Represents the horizontal rotation of the camera, Defaults to -90. 
            pitch (int, optional):
                Represents the vertical rotation of the camera. Defaults to 0.
            constrain_value (int, optional):
                Maximum angle that the camera can rotate vertically. Defaults to 90.
            velocity (float, optional):
                How fast the camera should move in response to keyboard input. Defaults to 0.05.
            position (list[float], optional):
                Initial position of camera. Defaults to [0.0, 0.0, 10.0].
        """
        # Where is the camera
        self.camera_pos = Vector3(position)
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        # Configuration for movility
        self.mouse_sensitivity = mouse_sensitivity
        self.jaw = jaw
        self.pitch = pitch
        self.constrain_value = constrain_value
        self.velocity = velocity

        self.first_mouse = True

    def get_view_matrix(self) -> matrix44:
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset: float, yoffset: float, constrain_pitch=True) -> None:
        """How the camara move from the mouse"""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > self.constrain_value:
                self.pitch = self.constrain_value
            if self.pitch < -self.constrain_value:
                self.pitch = -self.constrain_value

        self.update_camera_vectors()

    def update_camera_vectors(self) -> None:
        front = Vector3([0.0, 0.0, 0.0])
        front.x = np.cos(np.radians(self.jaw)) * np.cos(np.radians(self.pitch))
        front.y = np.sin(np.radians(self.pitch))
        front.z = np.sin(np.radians(self.jaw)) * np.cos(np.radians(self.pitch))
        print(self.jaw, self.pitch, front)

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def process_keyboard(self, direction: Keys_config) -> None:
        """Camera method for movement"""
        if direction == Keys_config.FORWARD:
            self.camera_pos += self.camera_front * self.velocity
            print(self.camera_pos[0])
        if direction == Keys_config.BACKWARD:
            self.camera_pos -= self.camera_front * self.velocity
        if direction == Keys_config.LEFT:
            self.camera_pos -= self.camera_right * self.velocity
        if direction == Keys_config.RIGHT:
            self.camera_pos += self.camera_right * self.velocity
        if direction == Keys_config.UP:
            self.camera_pos += self.camera_up * self.velocity
        if direction == Keys_config.DOWN:
            self.camera_pos -= self.camera_up * self.velocity