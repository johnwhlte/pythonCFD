#!/bin/bash


cd ./runs/

for dir in */
do
    echo ${dir}
    cd ./${dir}
    checkMesh >meshstat
    decomposePar >decomplog
    mpirun -np 4 simpleFoam -parallel >runlog
    reconstructPar
    touch test.foam
    pvpython ../../pythonScripts/pvw.py
    cd -
done