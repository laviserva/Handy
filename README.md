# Handy
Produce a 3D waifu who traslate a message from voice or text into sign language

## Table of contents
* [Setting Environment with Conda](#setting-environment-with-conda)
* [Setting Environment](#setting-environment-with-pip)
* [Basic Example](#example)
* [Utils](#utils)

## Setting Environment with Conda
Pay attention to the _os.path_ and the enviroment _(Handy)_.
If you use _*conda install --yes --file requirements.txt*_ you'll have troubles because some of the libraries are not in anaconda's list. We suggest you follow the next sequence of instructions and avoid use _conda install_
```
(base) C:\User> cd path\Handy
(base) C:\User\path\Handy> conda create -n Handy python=3.9.7
(base) C:\User\path\Handy> conda activate Handy
(Handy) C:\User\path\Handy> pip install -r requirements.txt
```

## Setting Environment with pip
Before create the enviroment please check _os.path,_ requirements.txt and make sure you are using **_python==3.9.7_**

```
pip install -r requirements.txt
```

## Example
inside _\Examples\_ are some examples where is the code of some basic examples and theirs interactions. Here are the examples we suggest you to try.


* _Example 05 - Perspective Projection with View Matrix_
* _Example 06 - Ortographic Projection with View Matrix_
* _Example 08 - Basic 3D Render_: Load .OBJ files _(from */Resources/*)_, separate in smaller objects _(use ObjLoader(.obj, all_objects = True)_, load textures, and interact with the windows like FPS game

## Utils
obj_file = ObjLoader(.obj, all_objects = True) will bring us a list -> [names, indices, buffers] len(names) == len(indices) == len(buffers)