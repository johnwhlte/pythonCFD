import artery2Dpy as a2d
import os

set_path = input('What is the path? \n')
print(set_path)


listpoints,frontcube,backcube,back,top,bottom,inlet,outlet = a2d.outputPointsFromDiameterTable_straightTube(set_path)
a2d.writeBlockMeshDict(listpoints,frontcube,backcube,back,top,bottom,inlet,outlet)
        