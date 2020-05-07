from xml.dom import minidom
import re

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

def countAllTheClosedPathsInThisGroup(outgroup):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in outgroup["paths"]:
        if path["d"].endswith(" z") or path["d"].endswith(" Z"):
            if (path["d"].count(" c ") + path["d"].count(" C ")) == 1 :
                allClosedPaths.append(path["d"])
    return allClosedPaths

def countAllTheClosedPathsWithFewerThanNCommas(paths,n):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in paths:
        commaCount = path.count(",")
        if (commaCount < n):
            allClosedPaths.append(path)
    return allClosedPaths

def countAllTheClosedPathsWithMaxDistLessThanF(paths,f):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in paths:
        if (False == pathHasNonMoveAbsValueOfGreaterThanF(path,f)):
            allClosedPaths.append(path)
    return allClosedPaths

def countAllTheClosedPathsWithAreaLessThanF(paths,f):
    allClosedPaths = []
    # paths is an array of dictionaries
    # each containing id and d
    for path in paths:
        if (False == pathHasAreaAbsValueOfGreaterThanF(path,f)):
            allClosedPaths.append(path)
    return allClosedPaths



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
        print("uneven number of numbers ")
        print("skipping last one ")
        nNumbers -=1


    while i < nNumbers:
        xs.append(numbers[i])
        ys.append(numbers[i+1])
        i+=2
    return [xs,ys]


def pathHasNonMoveAbsValueOfGreaterThanF(path,f):
    numbers = numbersInPath(path)
    numbers.pop(0) # remove first move position
    numbers.pop(0) # remove second move position
    return max(numbers) > f

def pathPolyGoneArea(path):
    numbers = numbersInPath(path)
    numbers.pop(0) # remove first move position
    numbers.pop(0) # remove second move position
    xsys =  makeXsYs(numbers)
    xsys[0] = turnMovementsIntoPositions(xsys[0])
    xsys[1] = turnMovementsIntoPositions(xsys[1])
    return polygonArea(xsys[0],xsys[1])

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
    return abs(area/2.0)