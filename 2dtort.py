import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from vtk.util.numpy_support import vtk_to_numpy
from vtk import vtkXMLPolyDataReader
import math


vtpFile = 'P043_suboptimal_mid_RCA_and_PLV_FFR_0.87.vtp'
vtpDir = './vtpFiles/'
diamFile = 'P043_suboptimal_mid_RCA_and_PLV_FFR_0.87.csv'
diamDir = './diameterTables/'


def grabDataTables(filename):

    df = pd.read_csv(filename)

    diameterData = np.asarray(df['Diameter'])
    distanceData = np.asarray(df['Distance'])
    ffr = df['FFR']

    return diameterData, distanceData, ffr

def normalizeAngle(angle):

    norm = angle/(2*np.pi)
    norm2 = norm - math.floor(norm)

    return 2*np.pi*norm2


def readVTPFiles(path):

    reader = vtkXMLPolyDataReader()
    reader.SetFileName(path)
    reader.Update()
    polyDataOutput = reader.GetOutput()
    points = polyDataOutput.GetPoints()
    array = points.GetData()
    point_coordinates = vtk_to_numpy(array)

    return point_coordinates

def returnCenterPoints(cLinePoints):

    pointsNew = [[0,0]]

    point1 = cLinePoints[0]
    point0 = [point1[0] - 1, point1[1] - 1, point1[2] - 1]
    cLinePoints = cLinePoints.tolist()
    cLinePoints.insert(0,point0)
    cLinePoints = np.asarray(cLinePoints)

    count = 0

    angles = [0]

    for i in range(2,len(cLinePoints)):

        '''pn_calc = [cLinePoints[i][0] - cLinePoints[i-2][0],cLinePoints[i][1] - cLinePoints[i-2][1],cLinePoints[i][2] - cLinePoints[i-2][2]]
        pn1_calc =[cLinePoints[i-1][0] - cLinePoints[i-2][0],cLinePoints[i-1][1] - cLinePoints[i-2][1],cLinePoints[i-1][2] - cLinePoints[i-2][2]]

        pn_Angle = [pn_calc[0] - pn1_calc[0],pn_calc[1] - pn1_calc[1],pn_calc[2] - pn1_calc[2]]'''

        pn1_calc = [cLinePoints[i-1][0] - cLinePoints[i-2][0],cLinePoints[i-1][1] - cLinePoints[i-2][1],cLinePoints[i-1][2] - cLinePoints[i-2][2]]
        pn_Angle = [cLinePoints[i][0] - cLinePoints[i-1][0],cLinePoints[i][1] - cLinePoints[i-1][1],cLinePoints[i][2] - cLinePoints[i-1][2]]

        dotProduct = pn_Angle[0]*pn1_calc[0] + pn_Angle[1]*pn1_calc[1] + pn_Angle[2]*pn1_calc[2]
        magnitudePA = np.sqrt(pn_Angle[0]**2 + pn_Angle[1]**2 + pn_Angle[2]**2)
        magnitudeP1 = np.sqrt(pn1_calc[0]**2 + pn1_calc[1]**2 + pn1_calc[2]**2)
        A1 = math.acos(dotProduct/(magnitudePA*magnitudeP1))
        #print(A1)
        #for i in angles:
            #A1 = A1 + i
        #angles.append(normalizeAngle(A1))
        A = A1
        B = np.sqrt(pn_Angle[0]**2 + pn_Angle[1]**2 + pn_Angle[2]**2)

        print(A)

        pointN_1 = [math.cos(A)*B,math.sin(A)*B]

        pointN_2 = [pointsNew[count][0] + pointN_1[0], pointsNew[count][1] + pointN_1[1]]

        count = count + 1
        print(count)
        print(i)

        pointsNew.append(pointN_2)

    return pointsNew

def gradCalc(points):

    v = [[0,0]]

    for i in range(1,len(points)):
        dist = np.sqrt((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2 + (points[i][2] - points[i-1][2])**2)

        if abs(points[i][0] - points[i-1][0]) > 0:
            gradxz = points[i][2] - points[i-1][2] / (points[i][0] - points[i-1][0])
        else:
            gradxz = 0
        if abs(points[i][1] - points[i-1][1]) > 0:
            gradyz = points[i][2] - points[i-1][2] / (points[i][1] - points[i-1][1])
        else:
            gradyz = 0
        if abs(points[i][1] - points[i-1][1]) > 0:
            gradyx = points[i][0] - points[i-1][0] / (points[i][1] - points[i-1][1])
        else:
            gradyx = 0
        if abs(points[i][2] - points[i-1][2]) > 0:
            gradzx = points[i][0] - points[i-1][0] / (points[i][2] - points[i-1][2])
        else:
            gradzx = 0
        if abs(points[i][0] - points[i-1][0]) > 0:
            gradxy = points[i][1] - points[i-1][1] / (points[i][0] - points[i-1][0])
        else:
            gradxy = 0
        if abs(points[i][2] - points[i-1][2]) > 0:
            gradzy = points[i][1] - points[i-1][1] / (points[i][2] - points[i-1][2])
        else:
            gradzy = 0

        gradients = [abs(gradxz) , abs(gradxy) ,abs(gradyz) , abs(gradyx) , abs(gradzx) , abs(gradzy)]

        newGrad = min(gradients)

        if newGrad < 0:
            ynew = v[i-1][1] + np.sqrt(((newGrad**2)*(dist**2))/(1+newGrad**2))
        else:
            ynew = v[i-1][1] + np.sqrt(((newGrad**2)*(dist**2))/(1+newGrad**2))
        
        if dist**2 - (ynew - v[i-1][1])**2 >=0:
            xnew = v[i-1][0] + np.sqrt(dist**2 - (ynew - v[i-1][1])**2)
        else:
            xnew = v[i-1][0] + np.sqrt((ynew - v[i-1][1])**2 - dist**2)

        v.append([xnew,ynew])

    return v

def defineTortuosity(points):

    sumVal = 0

    for i in range(1,len(points)):

        p_x = points[i][0]
        p_y = points[i][1]
        p_z = points[i][2]

        p_x2 = points[i-1][0]
        p_y2 = points[i-1][1]
        p_z2 = points[i-1][2]

        distanceRaw = (p_x - p_x2)**2 + (p_y - p_y2)**2 + (p_z - p_z2)**2

        distance = np.sqrt(distanceRaw)

        sumVal = sumVal + distance

    sLineDistRaw = (points[-1][0] - points[0][0])**2 + (points[-1][1] - points[0][1])**2 + (points[-1][2] - points[0][2])**2
    sLineDist = np.sqrt(sLineDistRaw)

    return sLineDist/sumVal

def getCenterLinePaths(points):

    distances = [0]

    sumVal = 0

    for i in range(1,len(points)):

        p_x = points[i][0]
        p_y = points[i][1]
        p_z = points[i][2]

        p_x2 = points[i-1][0]
        p_y2 = points[i-1][1]
        p_z2 = points[i-1][2]

        distanceRaw = (p_x - p_x2)**2 + (p_y - p_y2)**2 + (p_z - p_z2)**2

        distance = np.sqrt(distanceRaw)

        sumVal = sumVal + distance

        distances.append(sumVal)

    return distances

def addTopBottom(line,diameters):

    R = diameters[0]/2

    top = []#[[line[0][0],line[0][1] + R]]
    bottom = []#[[line[0][0],line[0][1] - R]]

    for i in line[1:]:

        D = diameters[line.index(i)]

        p_x = i[0]
        p_y = i[1]

        R = D/2

        magn = np.sqrt(p_x**2 + p_y**2)

        ptop = [p_x + R*(p_y/magn),p_y - R*(p_x/magn)]
        pbot = [p_x - R*(p_y/magn),p_y + R*(p_x/magn)]

        top.append(ptop)
        bottom.append(pbot)

    return top, bottom


def getFiles(dir,fileType):

    files = []
    entries = []
    
    for filename in os.scandir(dir):

        if filename.is_file() and filename.path.endswith(fileType):

            files.append(filename.path)
            entries.append(filename.name)

    return files, entries

diameterFiles, diameterNames = getFiles(diamDir,'.csv')
vtpFiles, vtpNames = getFiles(vtpDir,'.vtp')

tort3D = []
tort2D = []

for i in range(0,len(diameterFiles)):

    for j in range(0,len(vtpFiles)):

        if vtpNames[j][:len(vtpNames[j]) - 4] == diameterNames[i][:len(diameterNames[i]) - 4]:
            diameters, distances, ffrs = grabDataTables(diameterFiles[i])
            centerLinePoints = readVTPFiles(vtpFiles[j])

            x = gradCalc(centerLinePoints)
            t,b = addTopBottom(x,diameters)
            d3 = []
            X = []
            Y = []
            Z = []
            d3 = []
            topx = []
            topy = []
            botx = []
            boty = []

            '''for point in x:

                X.append(point[0])
                Y.append(point[1])'''

            for point in t:

                topx.append(point[0])
                topy.append(point[1])

            for point in b:

                botx.append(point[0])
                boty.append(point[1])

            '''for point in x:
                v = [point[0],point[1],0]
                d3.append(v)

            tort3D.append(defineTortuosity(centerLinePoints))
            tort2D.append(defineTortuosity(d3))

            print(diameterNames[i])

            #plt.plot(Y,X)
            plt.scatter(topy,topx)
            plt.scatter(boty,botx)
            plt.ylim(ymin=-2,ymax=20)
            plt.show()

            print(defineTortuosity(centerLinePoints))
            print(defineTortuosity(d3))

            distance1 = getCenterLinePaths(centerLinePoints)
            distance2 = getCenterLinePaths(d3)

            plt.plot(distance1,distance2)
            plt.show()'''

            paths = pd.DataFrame({'x':boty,
                                    'yt':topx,
                                    'yb':botx})
            paths.to_csv(f'./curvedProfiles/{diameterNames[i]}')
            
        else:
            continue


