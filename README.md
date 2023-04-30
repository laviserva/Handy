# Handy
3D environment for rendering

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