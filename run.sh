#!/bin/bash


cd ./runs/

for dir in */
do
    echo ${dir}
    cd ./${dir}
    checkMesh >meshstat
    simpleFoam >log
    touch test.foam
    pvpython ../../pythonScripts/pvw.py
    cd -
done