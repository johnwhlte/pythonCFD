import artery2Dpy as a2d
import pandas as pd
import os
from subprocess import call

direct = '../diameterTables/'
paths = []
directories = []
directoriespath = []
names = []

for filename in os.scandir(direct):
    if(filename.path.endswith('.csv')) and filename.is_file():
        paths.append(filename.path)
        names.append(filename.name)

direct = './'

for filename in os.scandir(direct):
    if not filename.is_file():
        directories.append(filename.name)
        directoriespath.append(filename.path)

print(paths)
print(directories)

for i in directories:
    for j in names:
        if i[0:9] == j[0:9]:
            a2d.writeBCs_Pinlet_velocityOutlet(paths[names.index(j)],i,float(i[17:21]))
        else:
            continue

