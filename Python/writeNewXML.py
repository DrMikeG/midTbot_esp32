import os

def copyFileLineByLine(pathToInputFile,pathToOutputFile,skipLineContaining):
    reader = open(pathToInputFile)
    fileOut = open(pathToOutputFile, 'w')
    try:
        # Further file processing goes here
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            shouldSkipLine = False
            for skips in skipLineContaining:
                if (line.find(skips) > -1) :
                    shouldSkipLine = True
                    break
            if(False == shouldSkipLine):
                fileOut.write(line)
            line = reader.readline()
            
    finally:
        reader.close()
        fileOut.close()