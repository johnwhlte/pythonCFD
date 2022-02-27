import artery2Dpy as a2d
import pandas as pd
import os
from subprocess import call

flowrates = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00]

files = []
entries = []
flows = []
names = []

workdir = '../diameterTables/'

for entry in os.scandir(workdir):
    if(entry.path.endswith('.csv')) and entry.is_file():
        files.append(entry.path)
        entries.append(entry.name)

for i in entries:
    adder = []
    names.append([i[0:7]]*len(flowrates))
    flows.append(flowrates)

flat_names = [item for sublist in names for item in sublist]
flat_flows = [item for sublist in flows for item in sublist]

for i in range(0,len(flat_names)):
    flat_names[i] = f"P{flat_names[i]}case"

df = pd.DataFrame({'Patient IDs': flat_names, 'Flowrates mL/s': flat_flows})

namesShort = [f'P{i[0:7]}case' for i in entries]

for i in namesShort:
    for j in flowrates:
        call(['mkdir',f"{i}{j}"])
        call(['cp','-a',f'../patientCases/{i}/.',f'./{i}{j}/'])