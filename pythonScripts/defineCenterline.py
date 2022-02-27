import pandas as pd
from subprocess import call
import os


direct = './diameterTables/'
paths = []
directories = []
directoriespath = []
names = []

for filename in os.scandir(direct):
    if(filename.path.endswith('.csv')) and filename.is_file():
        paths.append(filename.path)
        names.append(filename.name)

direct = './runs/'

for filename in os.scandir(direct):
    if not filename.is_file():
        directories.append(filename.name)
        directoriespath.append(filename.path)

print(paths)
print(directories)

for i in directories:
    for j in names:
        if i[1:8] == j[0:7]:
            df = pd.read_csv(paths[names.index(j)],delimiter=',')
            diam = df['Diameter']
            dist = df['Distance']
            offset = max(diam)/2
            minD = min(diam)
            centery = (offset + (minD/2))/1000
            length = max(dist)/1000
            data = pd.DataFrame({'center':[centery],
                            'length':[length]})
            pd.DataFrame.to_csv(data,f'./runs/{i}/fun.csv',sep=',')

        else:
            continue