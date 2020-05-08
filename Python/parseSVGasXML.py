from xml.dom import minidom
import re
import bez

def getPaths(pathToFile):
    doc = minidom.parse(pathToFile)  # parseString also exists
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()
    return path_strings

def getGroups(pathToFile):
    doc = minidom.parse(pathToFile)  # parseString also exists
    
    outgroups = []

    for group in doc.getElementsByTagName('g'):
        group_label = group.getAttribute('inkscape:label')
        group_path_strings = []
        for path in group.getElementsByTagName('path'):
            group_path_strings.append({
                "id" : path.getAttribute('id'),
                "d" : path.getAttribute('d')
            })
        
        outgroup = {}
        outgroup["label"] = group_label
        outgroup["paths"] = group_path_strings
        outgroups.append(outgroup)

    doc.unlink()
    return outgroups

def countAllThePolyBezPathsInThisGroup(outgroup):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in outgroup["paths"]:
        if (isPolyBezPath(path["d"]) ) :
            if (hasExpectedNumberOfTerms(path["d"])) :
                allClosedPaths.append(path["d"])
    return allClosedPaths


def countAllTheClosedPathsInThisGroup(outgroup):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in outgroup["paths"]:
        if (isClosedPath(path["d"]) ) :
                allClosedPaths.append(path["d"])
    return allClosedPaths

def isClosedPath(path):
    if path.endswith(" z") or path.endswith(" Z"):
            if (path.count(" c ") + path.count(" C ")) > 0 :
                return True
    return False

def isPolyBezPath(path):
    if (path.count(" c ")) > 0 :
        if (path.count(" l ")) == 0 :
            if (path.count(" h ")) == 0 :
                if (path.count(" v ")) == 0 :
                    return True
    return False

def hasExpectedNumberOfTerms(path): 
    curves = splitPathIntoPolyCurves(path)
    # curves should be at least m section (2 numbers) followed by 1 or more c section (3*n)
    if (len(curves) > 1):
        mNumbers = numbersInPath(curves[0])
        if (len(mNumbers) == 2):
            allThrees = True
            for curve in curves[1::] :
                cNumbers = numbersInPath(curve)
                if (len(cNumbers) % 3 != 0):
                    allThrees = False
                    break
            if (allThrees):
                return True
    return False


def countAllTheClosedPathsWithFewerThanNCommas(paths,n):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in paths:
        commaCount = path.count(",")
        if (commaCount < n):
            allClosedPaths.append(path)
    return allClosedPaths

def removePathsWithAreaLessThanF(paths,f):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in paths:
        if (False == pathHasAreaAbsValueOfGreaterThanF(path,f)):
            allClosedPaths.append(path)
    return allClosedPaths



def pathCountPolyBezSection(path):
    return path.count(" c ")

def splitPathIntoPolyCurves(path):
    l = []
    for t in re.split(' c | l ',path):
        try:
            l.append(t)
        except ValueError:
            pass
    return l

def numbersInPath(path):
    l = []
    for t in re.split(',| ',path):
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

def makeXsYs(numbers):

    xs = []
    ys = []
    i=0
    nNumbers = len(numbers)

    if (nNumbers % 2 == 1):
        #print("uneven number of numbers ")
        #print("skipping last one ")
        nNumbers -=1


    while i < nNumbers:
        xs.append(numbers[i])
        ys.append(numbers[i+1])
        i+=2
    return [xs,ys]



def pathPolyGoneArea(path):
    assert isClosedPath(path) 
    numbers = numbersInPath(path)
    xsys =  makeXsYs(numbers)
    xsys[0] =turnMovementsIntoPositions(xsys[0])
    xsys[1] = turnMovementsIntoPositions(xsys[1])
    intXsYS = bez.tenStepsOnPolyCubic(xsys)
    return polygonArea(intXsYS[0],intXsYS[1])
    
def turnMovementsIntoPositions(xs):
    newXs = []
    position = 0.0
    nPositions = len(xs)
    i=0
    while i < nPositions:
        position += xs[i]
        newXs.append(position)
        i+=1

    assert len(newXs) == len(xs), "output area should be the same length as input"
    return newXs


def pathHasAreaAbsValueOfGreaterThanF(path,f):
    return pathPolyGoneArea(path) > f

def polygonArea(Xs,Ys):
    area = 0   # Accumulates area 
    numPoints = len(Xs)
    j = numPoints-1
    i = 0
    while i < numPoints:
        area +=  (Xs[j]+Xs[i]) * (Ys[j]-Ys[i])
        j = i #j is previous vertex to i
        i += 1
    return round(abs(area/2.0))