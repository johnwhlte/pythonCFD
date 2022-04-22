import os
import pandas as pd
from subprocess import call

workdir = './'
entries = []
files = []
ffrValues = []
files_new = []
entries_new = []
for entry in os.scandir(workdir):
    if(entry.path.endswith('.csv')) and entry.is_file():
        files.append(entry.path)
        entries.append(entry.name)

for name in entries:
    for i in range(0,len(name)-3):
        if name[i] == 'F' and name[i+1] == 'F' and name[i+2] == 'R' and name[i+3] == '_':
            try:
                ffr = float(name[(i+4):(i+8)])
                files_new.append(files[entries.index(name)])
                entries_new.append(entries[entries.index(name)])
                ffrValues.append(ffr)
            except ValueError:
                try:
                    ffr = float(name[(i+4):(i+7)])
                    files_new.append(files[i])
                    entries_new.append(entries[i])
                    ffrValues.append(ffr)
                except ValueError:
                    continue

for i in range(0,len(files_new)):
    df = pd.read_csv(files_new[i],delimiter=',')
    diameters = df['0']
    distances = df['1']
    ffrs = [ffrValues[i]]*len(distances)

    tempDataF = pd.DataFrame({'Distance':distances,
                                'Diameter': diameters,
                                'FFR': ffrs})
    tempDataF.to_csv(f'../diameterTables/{entries_new[i]}')
'''        
ffr_files = []
file_names = []

for i in files:
    df = pd.read_csv(i,delimiter=',')
    
    try:
        ffr = df['FFR'][0]
        ffr_files.append(i)
        file_names.append(entries[files.index(i)])
        call(['cp','-i',i,'../diameterTables/'])
    except KeyError:
        continue
'''
