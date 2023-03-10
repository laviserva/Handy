# Object and Texture Loader

A nice way to ilustrate what Object Loader do is with the next image.
![[resources/Object Loader mentalmap.png]]
# File Obj
## Preparing data
An obj extension is grouped by objects, groups, vertices, normal vertices, texture vertices face, materials etc. In `Resources folder` in root there is `plane_1.obj` it looks like this:

```obj
# Blender 3.4.1
# www.blender.org
mtllib plano_1.mtl
o Plane
v -1.000000 0.000000 1.000000
v 1.000000 0.000000 1.000000
v -1.000000 0.000000 -1.000000
v 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000
vt 1.000000 0.000000
vt 0.000000 1.000000
vt 1.000000 1.000000
s 0
f 2/2/1 3/3/1 1/1/1
f 2/2/1 4/4/1 3/3/1
```

There are extra information that is not useful in this context, _#, mtllib_ and _s_. in a few words

```obj
o Plane
v -1.000000 0.000000 1.000000
v 1.000000 0.000000 1.000000
v -1.000000 0.000000 -1.000000
v 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000
vt 1.000000 0.000000
vt 0.000000 1.000000
vt 1.000000 1.000000
f 2/2/1 3/3/1 1/1/1
f 2/2/1 4/4/1 3/3/1
```

We want to group from prefixes and store all prefixes by objects

```obj
o Plane
v -1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 -1.000000 0.000000 -1.000000 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 1.000000 1.000000
f 2/2/1 3/3/1 1/1/1 2/2/1 4/4/1 3/3/1
```

## indices
with all this information we will get indices (face - 1) and buffers.

```
i 1 1 0 2 2 0 0 0 0 1 1 0 3 3 0 2 2 0
```

## Faces
Face start to count from 1, but python starts from 0, so we need to substract 1 for all operations in faces. If we have face 2/2/1 in index would be 1/1/0. Let's suppose we have a 3/2/1 face.

- 3rd vertice (grouped by 3): -1.000000 0.000000 -1.000000
- 2nd texture vertice (grouped by 2):  1.000000 0.000000
- 1st normal texture (unique in this case, grouped by 3): -0.0000 1.0000 -0.0000

## Building buffers
There is 2 options to calculate buffers
1. See faces `2/2/1` means that you will use for `vertices[2-1]`, `texture vertices[2-1]`, `normal vertice[1-1]`
2. Indices `vertices[1]`, `texture vertices[1]`, `normal vertice[0]`

```
b 1.0, 0.0, 1.0, 1.0, 0.0, -0.0, 1.0, -0.0, -1.0, 0.0, -1.0, 0.0, 1.0, -0.0, 1.0, -0.0, -1.0, 0.0, 1.0, 0.0, 0.0, -0.0, 1.0, -0.0, 1.0, 0.0, 1.0, 1.0, 0.0, -0.0, 1.0, -0.0, 1.0, 0.0, -1.0, 1.0, 1.0, -0.0, 1.0, -0.0, -1.0, 0.0, -1.0, 0.0, 1.0, -0.0, 1.0, -0.0
```

# Multiple objects
If you want to separate 2 objects from 1 file like `plane_both_objects.obj` you will find that the format is the next

```plane_both_objects.obj
o Plane 
v -1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 -1.000000 0.000000 -1.000000 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 1.000000 1.000000
f 2/2/1 3/3/1 1/1/1 2/2/1 4/4/1 3/3/1

o Plane.001
v -0.998391 0.281908 0.575339 1.001609 0.281908 0.575339 -0.998391 0.281908 -1.424661 1.001609 0.281908 -1.424661
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 1.000000 1.000000
f 6/6/2 7/7/2 5/5/2 6/6/2 8/8/2 7/7/2
```

For `Plane` we need to have the faces indices separated, 4/4/1, 4 in v, 4 in vt, 1 in vn. In Plane.001 object, the minimum indice is 5/5/2 having now

```
o Plane 
v -1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 -1.000000 0.000000 -1.000000 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 1.000000 1.000000
f 2/2/1 3/3/1 1/1/1 2/2/1 4/4/1 3/3/1

o Plane.001
v -0.998391 0.281908 0.575339 1.001609 0.281908 0.575339 -0.998391 0.281908 -1.424661 1.001609 0.281908 -1.424661
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000 1.000000 0.000000 0.000000 1.000000 1.000000 1.000000
f 2/2/1 5/5/1 1/1/1 2/2/1 4/4/1 3/3/1
```

And finally just add indices and buffers
