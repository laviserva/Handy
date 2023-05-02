# How camera is implemented

in the path utils.Camera.py exist all the code for camera behavior. In the inizialization of the class, exists some arguments that are more important than others, like:

- __Mouse sensibility__: determines how much the camera should move with you move the mouse, if you decrease the number, it could be innestable and hard to deal with.
- __Position__: Where will be the camera
- __jaw__: Control x axis in degres 360° (it is needed to cast in radians)
- __pitch__: Control y axis in degres 360° (it is needed to cast to radians)
- __front__: Show in _(x, y, z)_ 

# Camera
## Process Keyboard
The function **«process_keyboard»** process how the camera position will change when you have pressed a key from keyboard, if we want to create a motion described by
$$
x = sin(t)
$$
when you press a key, then the code will be

```python
class Camera:
    def __init__(*args):
        self.forw_pressed_key = False

    def process_keyboard(*args) -> None:
        """Camera method for movement"""
        if direction == Keys_config.JUSTFORWARD and not self.forw_pressed_key:
            self.forw_pressed_key = True
        if self.forw_pressed_key:
            self.camera_pos[0] +=self.velocity * sin(glfw.get_time())
```

## Process Camera
The function **process_mouse_movement** process how the camera angular position will change when you move the mouse, if you want to create a script for a cinematic, given by
$$
y = cos(t)
$$
remember that __jaw__ and __pitch__ control $x$ and $y$ angles axis in degres 360°
when you press a key, then the code will be

```python
class Camera:
    def __init__(*args):
        self.camera_script = False

    def process_keyboard(*args) -> None:
        """Camera method for movement"""
        if event and not camera_script:
            self.camera_script = True
        if self.camera_script:
            self.pitch +=self.velocity * cos(glfw.get_time()) # y movement
            #self.jaw +=self.velocity * cos(glfw.get_time()) # x movement
            self.update_camera_vectors()
```