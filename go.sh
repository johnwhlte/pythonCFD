#!/bin/bash


source a2d/bin/activate

bash meshsetup.sh
bash flowrategen.sh
bash writebcs.sh
python3 ./pythonScripts/defineCenterline.py
bash run.sh

deactivate