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


def numbersInPath(path):
    l = []
    for t in re.split(',| ',path):
        try:
            l.append(abs(float(t)))
        except ValueError:
            pass
    return l

def pathHasNonMoveAbsValueOfGreaterThanF(path,f):
    numbers = numbersInPath(path)
    numbers.pop(0) # remove first move position
    numbers.pop(0) # remove second move position
    return max(numbers) > f