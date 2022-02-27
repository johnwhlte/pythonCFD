# Initialization of all functions involved in a artery2Dpy project
# includes multiple ways to create blockMesh from point values as well as; 
# writing bondary conditions, collecting data, and interpreting data


import numpy as np
import pandas as pd
import math


def output_Profiles(path):
    
    df = pd.read_csv(path,delimiter=',')
    
    d = np.asarray(df['Diameter'])
    p = np.asarray(df['Distance'])
    
    maxD = max(d)
    
    x = p
    
    yB = []
    yT = []
    
    for i in d:
        
        delta = maxD - i
        
        yB.append(delta/2)
        yT.append(i + (delta/2))

    yTu = []
    yBu = []
    xu = []

    divider= math.floor(len(yT)/100)

    for i in range(0,100):
        yTc = i*divider
        yBc = i*divider
        xc = i*divider
        yTu.append(yT[yTc])
        yBu.append(yB[yBc])
        xu.append(x[xc])
        
    yB = yBu
    yT = yTu
    x = xu
    
    
    
    return x, yT, yB


def outputPointsFromDiameterTable_straightTube(path):
    x, yT, yB = output_Profiles(path)
    deltaZ = 0.001

    topPointsBack = []
    topPointsFront = []
    bottomPointsBack = []
    bottomPointsFront = []


    for i in range(0,len(x)):
        adder = []
        adder.append(x[i])
        adder.append(yT[i])
        adder.append(0)
        topPointsBack.append(adder)
        adder = []
        adder.append(x[i])
        adder.append(yT[i])
        adder.append(deltaZ)
        topPointsFront.append(adder)
        adder = []
        adder.append(x[i])
        adder.append(yB[i])
        adder.append(0)
        bottomPointsBack.append(adder)
        adder = []
        adder.append(x[i])
        adder.append(yB[i])
        adder.append(deltaZ)
        bottomPointsFront.append(adder)
        
        
        
        
    listpoints = []
        
    for i in range(1,len(topPointsBack)):
            
        if i == 1:
            listpoints.append(bottomPointsBack[i-1])
            listpoints.append(bottomPointsBack[i])
            listpoints.append(topPointsBack[i])
            listpoints.append(topPointsBack[i-1])
            listpoints.append(bottomPointsFront[i-1])
            listpoints.append(bottomPointsFront[i])
            listpoints.append(topPointsFront[i])
            listpoints.append(topPointsFront[i-1])
        else:
            listpoints.append(bottomPointsBack[i])
            listpoints.append(topPointsBack[i])
            listpoints.append(bottomPointsFront[i])
            listpoints.append(topPointsFront[i])
        
    frontcube = []
    backcube = []
    top = []
    bottom = []


    highPointValue = 4*len(bottomPointsBack) - 1

    point = 0
    count = 0

    while point < highPointValue:
    
        if point == 0:
            adder=[]
            adder.append(0)
            adder.append(1)
            adder.append(2)
            adder.append(3)
            backcube.append(adder)
            adder=[]
            adder.append(4)
            adder.append(5)
            adder.append(6)
            adder.append(7)
            frontcube.append(adder)
            point = point + 1
        
        else:
            adder = []
        
            if count == 0:
            
                po = frontcube[count][3]
                adder.append(backcube[count][1])
                adder.append(po + 1)
                adder.append(po + 2)
                adder.append(backcube[count][2])
                backcube.append(adder)
                adder = []
                adder.append(frontcube[count][1])
                adder.append(po + 3)
                adder.append(po + 4)
                adder.append(frontcube[count][2])
                frontcube.append(adder)
                point = frontcube[count][2]
                count = count + 1
            
            else:
                po = frontcube[count][2]
                adder.append(backcube[count][1])
                adder.append(po + 1)
                adder.append(po + 2)
                adder.append(backcube[count][2])
                backcube.append(adder)
                adder = []
                adder.append(frontcube[count][1])
                adder.append(po + 3)
                adder.append(po + 4)
                adder.append(frontcube[count][2])
                frontcube.append(adder)
                point = frontcube[count][2]
                count = count + 1
            
            
        adder = []
        adder.append(frontcube[count][3])
        adder.append(frontcube[count][2])
        adder.append(backcube[count][2])
        adder.append(backcube[count][3])
        top.append(adder)
        adder = []
        adder.append(backcube[count][0])
        adder.append(backcube[count][1])
        adder.append(frontcube[count][1])
        adder.append(frontcube[count][0])
        bottom.append(adder)
    
    
    back = []

    for i in backcube:
        
        flip1 = i[1]
        flip2 = i[3]
        
        adder = []
        
        adder.append(i[0])
        adder.append(flip2)
        adder.append(i[2])
        adder.append(flip1)
        back.append(adder)
    
    inlet = []

    inlet.append(frontcube[0][0])
    inlet.append(frontcube[0][3])
    inlet.append(backcube[0][3])
    inlet.append(backcube[0][0])

    outlet = []

    outlet.append(backcube[len(backcube)-2][1])
    outlet.append(backcube[len(frontcube)-2][2])
    outlet.append(frontcube[len(frontcube)-2][2])
    outlet.append(frontcube[len(frontcube)-2][1])
    

    return listpoints,frontcube,backcube,back,top,bottom,inlet,outlet

def writeBlockMeshDict(lp,fc,bc,b,t,btm,inl,o):
    
    with open('../exampleCase/system/blockMeshDict','a') as f:
        f.write('\nvertices\n(\n')
        for i in range(0,len(lp)):
            f.write('\t(' + str(lp[i][0]) + ' ' +  str(lp[i][1]) + ' ' + str(lp[i][2]) + ')\n')
        f.write(');\n')  
        f.write('blocks\n(\n')
        for i in range(0,len(fc)-1):
            f.write('\thex ' + '(' +str(bc[i][0]) + ' '
                    +str(bc[i][1])+ ' '
                    +str(bc[i][2])+ ' '
                    +str(bc[i][3])+ ' '
                    +str(fc[i][0])+ ' '
                    +str(fc[i][1])+ ' '
                    +str(fc[i][2])+ ' '
                    +str(fc[i][3])
                    + ')' + ' ' + '(8 60 1)' + ' ' + 'simpleGrading' + ' ' + '(1 ((0.5 0.5 10) (0.5 0.5 0.1)) 1)\n' )
        
        f.write(');\n\nedges\n(\n);\n\n') 
        f.write('boundary\n(\n\tTop\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n')
        for i in range(0,len(t)-1):
            f.write('\t\t\t(' + str(t[i][0]) + ' '
                    +str(t[i][1])+ ' '
                    +str(t[i][2])+ ' '
                    +str(t[i][3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write('\tBottom\n\t{\n\t\ttype wall;\n\t\tfaces\n\t\t(\n')
        for i in range(0,len(btm)-1):
            f.write('\t\t\t(' + str(btm[i][0]) + ' '
                    +str(btm[i][1])+ ' '
                    +str(btm[i][2])+ ' '
                    +str(btm[i][3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write('\tFront\n\t{\n\t\ttype empty;\n\t\tfaces\n\t\t(\n')
        for i in range(0,len(fc)-1):
            f.write('\t\t\t(' + str(fc[i][0]) + ' '
                    +str(fc[i][1])+ ' '
                    +str(fc[i][2])+ ' '
                    +str(fc[i][3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write('\tBack\n\t{\n\t\ttype empty;\n\t\tfaces\n\t\t(\n')
        for i in range(0,len(b)-1):
            f.write('\t\t\t(' + str(b[i][0]) + ' '
                    +str(b[i][1])+ ' '
                    +str(b[i][2])+ ' '
                    +str(b[i][3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write('\tInlet\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n')
        f.write('\t\t\t(' + str(inl[0]) + ' '
                    +str(inl[1])+ ' '
                    +str(inl[2])+ ' '
                    +str(inl[3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write('\tOutlet\n\t{\n\t\ttype patch;\n\t\tfaces\n\t\t(\n')
        f.write('\t\t\t(' + str(o[0]) + ' '
                    +str(o[1])+ ' '
                    +str(o[2])+ ' '
                    +str(o[3]) + ')\n')
        f.write('\t\t);\n\t}\n')
        f.write(');\n\nmergePatchPairs\n(\n);\n\n// ************************************************************************* //')
        f.close()

    return 0


def writeBCs_Pinlet_velocityOutlet(path,casedir,volFlowRate):

    df = pd.read_csv(path,delimiter=',')

    data = np.asarray(df['Diameter'])
    
    outletD = data[-1]
    outletV = volFlowRate/(np.pi*((outletD/2)**2)) #m/s

    with open(f'./{casedir}/0/U','a') as f:
        f.write('\n{\n\tInlet\n\t{\n\t\ttype\tzeroGradient;\n\t}\n\n')
        f.write('\tOutlet\n\t{\n\t\ttype\tfixedValue;\n\t\tvalue\tuniform (')
        f.write(str(outletV) + ' 0 0);\n\t}\n\n')
        f.write('\tTop\n\t{\n\t\ttype\tnoSlip;\n\t}\n\n')
        f.write('\tBottom\n\t{\n\t\ttype\tnoSlip;\n\t}\n\n')
        f.write('\tFront\n\t{\n\t\ttype\tempty;\n\t}\n\n')
        f.write('\tBack\n\t{\n\t\ttype\tempty;\n\t}\n\n}\n\n// ************************************************************************* //')

def calculateFFR_Pout_Pin(path):

    df = pd.read_csv(path+'/data.csv',delimiter=',')

    p = df['p']
    x = df['Points:0']
    Ux = df['U:0']
    Uy = df['U:1']

    count1 = 0
    count2 = 0
    begin1 = 0
    deltatot = 0

    for k in range(1,len(p)):

        delta = p[k] - p[k-1]
        if delta < 0:
            count1 = count1 + 1
            deltatot = deltatot + delta
        elif delta > 0:
            count1 = 0
            deltatot = 0
        if count1 > 0:
            if abs(deltatot) > count2:
                count2 = abs(deltatot)
                begin1 = k - count1
                end1 = k
        else:
            continue
    xpd = 0
    pref = -1000
    for j in range(end1,len(p)):
        if p[j] > pref:
            xpd = x[j]
            pdstl = p[j]
            pref = pdstl

    begin = [x[begin1]] * 50
    end = [x[end1]] * 50
    pdg = [xpd] * 50

    yb = np.linspace(min(p),max(p),50)

    locate = 0
    add = x[begin1] + 0.02
    for i in range(0,len(p)):
        if not np.isnan(p[i]) and p[i] > 0:
            pendloc = i
        else:
            continue

    pdstl = p[pendloc]

    calc_ffr = pdstl/p[0]

    return calc_ffr


def percentDiameterStenosis(diameter,distance):    
    
    
    for i in range(math.floor(0.25*len(diameter)),math.floor(len(diameter)*0.75)):
        if i == math.floor(0.25*len(diameter)):
            min_D = diameter[i]
            min_loc_key = i
        else:
            if diameter[i] < min_D:
                min_D = diameter[i]
                min_loc = distance[i]
                min_loc_key = i
    
    avg_D1 = sum(diameter[:min_loc_key])/len(diameter[:min_loc_key].tolist())
    avg_D2 = sum(diameter[min_loc_key:])/len(diameter[min_loc_key:].tolist())


    for i in diameter[:min_loc_key]:
        if i > avg_D1:
            point_loc = diameter.tolist().index(i)
            points1 = point_loc
            point2 = distance[point_loc]
        else:
            continue


    for i in diameter[min_loc_key:]:
        if i > avg_D2:
            point_loc = diameter.tolist().index(i)
            points2 = point_loc
            point4 = distance[point_loc]
            break
        else:
            continue
    sumD1 = 0        
    for i in range(0,points1):
        sumD1 = sumD1 + diameter[i]
    dAvgPre = sumD1/points1

    sumD2 = 0        
    for i in range(points2,len(diameter)):
        sumD2 = sumD2 + diameter[i]
    dAvgPost = sumD2/(len(diameter) - points2)

    dAvgNoSten = (sumD1 + sumD2)/(len(diameter)-points2 + points1)
    
    sumD = 0
    for i in range(points1,points2):
        sumD = sumD + diameter[i]
    dAvgSten = sumD/(points2-points1)
    dSten = diameter[min_loc_key]


    return dAvgNoSten/dAvgSten


def checkBestFFRcomparison(path):

    df = pd.read_csv(path,delimiter=',')

    cFFR = df['cFFR']
    mFFR = df['mFFR']
    flowrate = df['FlowRate mL/s']

    counter = 1
    key = 0

    ffr = []
    cFFRclean = []
    cFFRdirty = []
    cFFR2b = []
    ffrAVG = []
    flows = []
    flowgs = []
    flows2b = []
    sD = []
    L = []

    while key < len(cFFR):

        t = []
        flowrates = []

        for i in flowrate:
            if i not in flowrates:
                flowrates.append(i)
        
        for i in range(0,len(flowrates)):
            t.append(cFFR[key + i])

        ffr.append(mFFR[key])
        sD.append(stenD[key])
        L.append(length[key])

        delta = 1000000
        greater = 0
        adder = 0
        piece = 4
        flow = 0

        for i in t:
            
            if abs(i - mFFR[key]) < delta:
                ffr2b = piece
                flow2b = flow
                piece = i
                delta = abs(i - mFFR[key])
                flow = flowrate[key+adder]

            if abs(i - mFFR[key]) > greater:
                pieceg = i
                greater = abs(i - mFFR[key])
                flowg = flowrate[key+adder]

            adder = adder + 1

        cFFRclean.append(piece)
        flows.append(flow)
        counter = counter + 1
        key = counter*12


    return cFFRclean, flows
