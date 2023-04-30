import numpy as np

from typing import List

from OpenGL.GL import glBindTexture, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,\
    glTexImage2D, GL_RGBA, GL_UNSIGNED_BYTE

from PIL import Image

def load_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

class ObjLoader:
    def __init__(self, object_path: str, all_objects: bool = False, texture_path: str = None):
        self._all_objects = all_objects
        self.texture = texture_path
        
        self.objects = {}
        self.object_path = object_path
        self.max_f = [0, 0, 0]
        self.__first_time = True

    def _add_texture(self, objects):
        if not self.texture: return objects
        
        for key in objects:
            objects[key]["t"] = self.texture
        return objects
        

    def load_model(self):
        """Return all objects inside a .obj file

        Returns:
            dict: {object_i:
                    "v": space coordinates (vertices)
                    "vn": vertices normal
                    "vt": texture coordinates (vertices textures)
                    "f": how all vertices are connected with each other (faces)
                    "i": indices needed for render
                    "b": buffer needed for render
                    "max_f": maximum indices in faces.
                    "len_i": lenght of indices
                    "init_pos": initial position for rendering, default [0, 0, 0] (x, y, z)
                   
                   object_2:
                    ...
                    }
        """
        assert self.object_path[-4:] == ".obj", "Invalid format, please use *.obj file"

        key_obj = None
        with open(self.object_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if values[0] not in ["o", "g", "v", "vn", "vt", "f"]: continue
                if (values[0] == "o" or values[0] == "g") and self.__first_time:
                    if key_obj != None and len(self.objects) > 0: # Maximum index for previous object
                        self.max_f = self.objects[key_obj]["max_f"]
                        self.objects[key_obj]["len_i"] = len(self.objects[key_obj]["i"])
                    key_obj = values[1]
                    self.objects[values[1]] = {
                        "v": [],
                        "vn": [],
                        "vt": [],
                        "f": [],
                        "i": [],
                        "b": [],
                        "max_f": [0, 0, 0],
                        "len_i": 0,
                        "init_pos": [0, 0, 0],
                    }
                    if not self._all_objects: self.__first_time = False
                    continue
                
                if key_obj == None:
                    continue
                self.objects[key_obj] = self._get_all_objects(values, self.objects[key_obj])
        self.objects = self._vertex_buffers(self.objects)
        self.objects = self._to_numpy(self.objects)
        return self._add_texture(self.objects)

    def _fix_indices(self, faces: str) -> List[int]:
        out = []
        for face in faces:
            out += [int(f) - 1 for f in face.split("/")]
        return out
        
    def _get_all_objects(self, values, objects) -> dict:
        if values[0] == "v": objects["v"] += [float(f) for f in values[1:]]
        if values[0] == "vt": objects["vt"] += [float(f) for f in values[1:]]
        if values[0] == "vn": objects["vn"] += [float(f) for f in values[1:]]
        if values[0] == "f":
            objects["f"] += values[1:]
            objects["i"] += self._fix_indices(values[1:])
            objects["len_i"] += 9
        return objects
    
    @staticmethod
    def _vertex_buffers(objects: dict) -> list:
        """create buffers for rendering.

        Args:
            objects (dict): object with all information
                dict: {object_i:
                        "v": space coordinates (vertices)
                        "vn": vertices normal
                        "vt": texture coordinates (vertices textures)
                        "f": how all vertices are connected with each other (faces)
                        "i": indices needed for render
                        "b": buffer needed for render
                        "max_f": maximum indices in faces.
                        "len_i": lenght of indices
                        "init_pos": initial position for rendering, default [0, 0, 0] (x, y, z)
                    
                    object_2:
                        ...
                        }
        Returns:
            list[int]: buffers ready to render
        """
        for keys in objects:
            buffer = []
            for index, ind in enumerate(objects[keys]["i"]):
                if index % 3 == 0: # sort the vertex coordinates
                    start = int(ind * 3)
                    end = int(start + 3)
                    buffer.extend(objects[keys]["v"][start:end])
                elif index % 3 == 1: # sort the texture coordinates
                    start = int(ind * 2)
                    end = int(start + 2)
                    buffer.extend(objects[keys]["vt"][start:end])
                elif index % 3 == 2: # sort the normal vectors
                    start = int(ind * 3)
                    end = int(start + 3)
                    buffer.extend(objects[keys]["vn"][start:end])
            objects[keys]["b"] = buffer
        return objects
    
    @staticmethod
    def _to_numpy(objects: dict) -> dict:
        for key in objects:
            for subkey in objects[key]:
                if not isinstance(objects[key][subkey], (list, tuple)):
                    continue
                if isinstance(objects[key][subkey][0], float):
                    datatype = np.float32
                elif isinstance(objects[key][subkey][0], int):
                    datatype = np.float32
                else:
                    continue
                objects[key][subkey] = np.array(objects[key][subkey], dtype=datatype)
        return objects