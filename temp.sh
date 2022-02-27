#!/bin/bash


for DIR in */
do
	cd ${DIR}
	cp -r ~/pythonCFDproject/pvwtemp.py ./
	source ~/pythonCFDproject/pvwenv/bin/activate
	pvpython pvwtemp.py

