import numpy as np
from utils.Config import Keys
from pyrr import Vector3, vector, vector3, matrix44

class Camera:
    def __init__(self, position: list[float] = [0.0, 0.0, 10.0]) -> None:
        # Where is the camera
        self.camera_pos = Vector3(position)
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        # Configuration for movility
        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0
        self.constrain_value = 90
        self.velocity = 0.05

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

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def process_keyboard(self, direction: Keys) -> None:
        """Camera method for the WASD movement"""
        if direction == Keys.FORWARD:
            self.camera_pos += self.camera_front * self.velocity
        if direction == Keys.BACKWARD:
            self.camera_pos -= self.camera_front * self.velocity
        if direction == Keys.LEFT:
            self.camera_pos -= self.camera_right * self.velocity
        if direction == Keys.RIGHT:
            self.camera_pos += self.camera_right * self.velocity
        if direction == Keys.UP:
            self.camera_pos += self.camera_up * self.velocity
        if direction == Keys.DOWN:
            self.camera_pos -= self.camera_up * self.velocity