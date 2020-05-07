import os.path
from os import path

def checkPathExists(path):
    return os.path.isfile(path)

def countLinesInFile(pathToFile):
    count = 0
    with open(pathToFile, 'r') as f:
        for line in f:
            count += 1
    return count


def countLinesInFileContaining(pathToFile,contains):
    count = 0
    with open(pathToFile, 'r') as f:
        for line in f:
            if contains in line:
                count += 1
    return count