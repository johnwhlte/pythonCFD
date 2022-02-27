activate_this = './pvwenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from paraview.simple import *
import pandas as pd

points = pd.read_csv('fun.csv')
middle = points['Halfway'][0]
length = points['Length'][0]

print(middle)
print(length)
testfoam = OpenDataFile("test.foam")

plotOverLine1 = PlotOverLine(Input=testfoam,
    Source='High Resolution Line Source')

plotOverLine1.Source.Point1 = [0.0, middle, 4.999999987376214e-07]
plotOverLine1.Source.Point2 = [length, middle, 4.999999987376214e-07]

SaveData('./data.csv', proxy=plotOverLine1)
