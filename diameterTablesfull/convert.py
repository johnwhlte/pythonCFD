import os
import pandas as pd
from subprocess import call

workdir = './'
entries = []
files = []

for entry in os.scandir(workdir):
    if(entry.path.endswith('.csv')) and entry.is_file():
        files.append(entry.path)
        entries.append(entry.name)
        
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

