# How to add actions by pressing keyboard

## Defining what key will contain the event
The file `config/keys.conf` contain all keys that are related with an event, the content of the file will look like this:

```
SPACE 32 up
A 65 left
D 68 right
S 83 backward
W 87 forward
LEFT_CONTROL 341 down
```

Each column has his own function.

- _column 1:_ Key in keyboard
- _column 2:_ Code used to interprate in software
- _column 3:_ Event to execute

First you need to create an enumeration to identify what action is needed to perform, for that go to `utils/Config.py` inside is the class `Key_config` let's suppose we want to create an event when we press the key `H`.

```python
class Keys_config(Enum):
    KEYBOARD_H = auto()
```

From now are some options for a desired behavior.

### Moving the camera for a given function
Once we had added to the class, then we need to go to `Camera.py` and find the function `process_keyboard` and add the movement wanted, per example, if we want that the keyboard move the camera.

$$
x = cos(t)
y = sin(t)
$$

```python
 def process_keyboard(self, direction: Keys_config) -> None:
        ...
        if direction == Keys_config.KEYBOARD_H:
            self.camera_pos[0] += math.cos(glfw.get_time()) * self.velocity
            self.camera_pos[1] += math.sin(glfw.get_time()) * self.velocity
```
