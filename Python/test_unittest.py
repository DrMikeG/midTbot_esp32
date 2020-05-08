import unittest
import loadFile
import parseSVGasXML
import writeNewXML
import bez
import os

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestReadFileMethods(unittest.TestCase):

    def test_canSeeFile(self):
        self.assertTrue(loadFile.checkPathExists(".\\testFiles\\round_church_two_paths_140x140.svg"))

    def test_FileContains28291Lines(self):
        self.assertEqual(loadFile.countLinesInFile(".\\testFiles\\round_church_two_paths_140x140.svg"),23226,"could not count lines in file")

    def test_FileContains28291LinesContainingZ(self):
        self.assertEqual(loadFile.countLinesInFileContaining(".\\testFiles\\round_church_two_paths_140x140.svg"," z\""),5774)

    def test_FileContains2InkscapeLabels(self):
        self.assertEqual(loadFile.countLinesInFileContaining(".\\testFiles\\round_church_two_paths_140x140.svg","inkscape:label"),2)

class TestReadFileAsXMLMethods(unittest.TestCase):

    def test_canReadAllPaths(self):
        self.assertEqual(len(parseSVGasXML.getPaths(".\\testFiles\\round_church_two_paths_140x140.svg")),5778)

    def test_canReadGroupLabelsAndTheirPaths(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        self.assertEqual(len(outgroups),2)
        self.assertEqual(outgroups[1]["label"],"GreenLayer")
        self.assertEqual(outgroups[0]["label"],"RedLayer")
        self.assertEqual(len(outgroups[1]["paths"]),2889)
        self.assertEqual(len(outgroups[0]["paths"]),2889)

        self.assertTrue("id" in outgroups[1]["paths"][0])
        

    def test_canCountClosedPathsInRedGroup(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])),2576)

    def test_canCountPolyBezPathsInRedGroup(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        self.assertEqual(len(parseSVGasXML.countAllThePolyBezPathsInThisGroup(outgroups[0])),2888)


    def test_splitPathIntoPolyCurves(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        allBezPaths = parseSVGasXML.countAllThePolyBezPathsInThisGroup(outgroups[0])
        #allBezPaths = ["m 4644.4095,-2548.3896 c 0,-3.5888 5.4618,-17.2226 12.1128,-30.2972 16.7193,-32.8657 19.9951,-59.5102 8.5584,-69.6047 -13.504,-11.9192 -53.5095,-18.6102 -83.053,-13.8908 -28.3172,4.5236 -30.4106,3.9963 -26.3313,-6.6333 2.1808,-5.684 10.6209,-7.3367 37.4652,-7.3367 38.9853,0 61.8412,5.1796 73.2651,16.6034 7.1663,7.1665 8.4357,6.2244 16.8068,-12.4727 8.8095,-19.6765 33.7221,-53.1188 52.8358,-70.926 10.1483,-9.4546 39.2933,-24.6833 50.9526,-26.6237 28.2093,-4.6946 40.3298,-3.7252 38.5725,3.0851 -1.0117,3.9224 -2.2978,10.3409 -2.8578,14.2633 -0.5601,3.9224 -2.5303,14.6198 -4.3793,23.7721 -1.8485,9.1522 -3.8882,20.3226 -4.5319,24.823 -1.9417,13.5655 -7.1421,15.0562 -10.1878,2.9204 -1.5756,-6.2776 -0.7303,-20.9135 1.8785,-32.5243 2.6087,-11.6108 4.1434,-21.7105 3.4103,-22.4436 -0.7331,-0.7332 -11.8451,0.1022 -24.6935,1.8561 -16.9475,2.3136 -26.8206,6.886 -35.9652,16.6559 -6.9329,7.4068 -14.5038,13.4669 -16.8244,13.4669 -10.009,0 -34.8409,51.7177 -42.2316,87.9566 -4.2666,20.9194 -13.2477,48.2348 -19.9581,60.7007 -13.6166,25.2942 -24.877,37.373 -24.8441,26.6495 z"]
        #allBezPaths = ["m 3716.0903,-2493.8711 c -17.0812,-8.9972 -16.243,-15.98 3.4222,-28.5037 18.7785,-11.9589 24.9398,-9.7919 11.2062,3.9416 l -9.5402,9.54 10.7649,11.4587 c 12.2764,13.0675 5.2075,14.6564 -15.8531,3.5634 z"]
        #allBezPaths = ["m -371.51656,-270.07963 c 0,-6.37016 12.83925,-18.26451 23.29886,-21.58428 9.12943,-2.89758 13.92378,-22.41496 10.83997,-44.12851 -1.28735,-9.06453 -4.43225,-10.69743 -20.60244,-10.69743 -13.15351,0 -18.46766,-1.84666 -17.1022,-5.94302 1.22664,-3.67996 10.88233,-5.94301 25.35686,-5.94301 h 23.37588 v 37.51712 c 0,28.69231 -1.6775,38.30397 -7.13162,40.86218 -3.92239,1.83977 -11.91641,5.81703 -17.76453,8.83836 -12.84595,6.63673 -20.27078,7.03178 -20.27078,1.07859 z"]

        # Paths with L V and H in
        # many numbers before first c?
        # m 913.62133,-751.23528 15.19415,-14.8835 -15.30826,10.3505 c -15.13472,10.2334 -23.6456,19.41655 -17.99545,19.41655 1.60366,0 9.7532,-6.69759 18.10956,-14.88355 z

        for path in allBezPaths :
            parseSVGasXML.hasExpectedNumberOfTerms(path)

    def test_allPolyBezPathsHave3NPlus1NumbersInRedGroup(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        allBezPaths = parseSVGasXML.countAllThePolyBezPathsInThisGroup(outgroups[0])
        for path in allBezPaths :
            
            numbers = parseSVGasXML.numbersInPath(path)
            nNumbers = len(numbers)
            
            if parseSVGasXML.isClosedPath(path) :
                self.assertTrue((nNumbers-1) % 3 == 0, path)
            else:
                self.assertTrue(nNumbers % 3 == 1, path)



    def test_canGetXSYS(self):
        numbers = parseSVGasXML.numbersInPath("m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z")
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),len(xsys[1]))

    def test_canGetPolygonArea1(self):
        xs = [4.0,  4.0,  8.0,  8.0, -4.0,-4.0]
        ys = [6.0, -4.0, -4.0, -8.0, -8.0, 6.0]
        self.assertEqual(parseSVGasXML.polygonArea(xs,ys),128.0)

    def test_canGetPolygonArea(self):
        #       id="path17286" />
        path17286 = "m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z"
        numbers = parseSVGasXML.numbersInPath(path17286)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertTrue(parseSVGasXML.polygonArea(xsys[0],xsys[1]) > 1558)



    # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
    # this is the problem I am not yet calculating the area of a bezier


    def test_canFindPathsWithLessThanFArea(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        paths = parseSVGasXML.countAllThePolyBezPathsInThisGroup(outgroups[0])
        self.assertEqual(len(paths),2576)
        if True:
            print(len(parseSVGasXML.removePathsWithAreaLessThanF(paths,100)))
            print(len(parseSVGasXML.removePathsWithAreaLessThanF(paths,1000)))
            print(len(parseSVGasXML.removePathsWithAreaLessThanF(paths,2500)))
            
            #self.assertEqual(len(parseSVGasXML.removePathsWithAreaLessThanF(paths,400)),1040)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,150)),166)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,75)),535)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,50)),179)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,25)),23)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,10)),8)
            #self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,5)),1)

    def test_writeNewXML(self):
        if loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"):
            os.remove(".\\testFiles\\tmp_round_church_two_paths_140x140.svg")

        self.assertTrue(loadFile.checkPathExists(".\\testFiles\\round_church_two_paths_140x140.svg"))
        self.assertFalse(loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"))

        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        
        redLines = parseSVGasXML.countAllThePolyBezPathsInThisGroup(outgroups[0])
        
        redLinesToSkip = parseSVGasXML.removePathsWithAreaLessThanF(redLines,2500)
        writeNewXML.copyFileLineByLine(".\\testFiles\\round_church_two_paths_140x140.svg",".\\testFiles\\tmp_round_church_two_paths_140x140.svg",redLinesToSkip)
        self.assertTrue(loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"))

    def test_bez01(self):
        path19986 = "m 4316.3854,-2232.4071 c 0.047,-2.1791 7.8804,-11.4502 17.4501,-20.6024 10.8015,-10.3303 16.1911,-13.3379 14.2128,-7.9314 -1.7529,4.79 -3.1869,11.4938 -3.1869,14.8973 0,3.4036 -3.7441,7.5089 -8.3202,9.123 -4.5761,1.6142 -10.9946,4.1815 -14.2632,5.7052 -3.2687,1.5237 -5.9202,0.9874 -5.8926,-1.1917 z"
        numbers = parseSVGasXML.numbersInPath(path19986)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        xsys[0] =parseSVGasXML.turnMovementsIntoPositions(xsys[0])
        xsys[1] = parseSVGasXML.turnMovementsIntoPositions(xsys[1])

        self.assertEqual(len(xsys[1]),19)
        self.assertEqual(len(xsys[0]),19)

        # 4316.3854,-2232.4071 
        # #c 
        # 0.047,-2.1791
        # 7.8804,-11.4502
        # 17.4501,-20.6024

        self.assertEqual(xsys[0][0],4316.3854)
        self.assertEqual(xsys[1][0],-2232.4071)

        self.assertEqual(xsys[0][1],4316.4324)
        self.assertEqual(xsys[1][1],-2234.5861999999997)

        self.assertEqual(xsys[0][2],4324.3128)
        self.assertEqual(xsys[1][2],-2246.0364)
        # end position
        self.assertEqual(xsys[0][3],4341.7629)
        self.assertEqual(xsys[1][3],-2266.6388)

        # Confirms this slice does what I thought...
        self.assertEqual([4316.3854,4316.4324,4324.3128,4341.7629],xsys[0][0:4:])
        self.assertEqual([-2232.4071,-2234.5861999999997,-2246.0364,-2266.6388],xsys[1][0:4:])

        Ts = bez.getTValues()
        self.assertEqual(len(Ts),11)

        # This is returning P0
        vs = bez.tenStepsCubic(xsys[0][0:4:],xsys[1][0:4:])

        self.assertEqual(len(vs),2,"two sub lists, xs and ys") 
        self.assertEqual(len(vs[0]),11,"ten x positions")
        self.assertEqual(len(vs[1]),11, "ten y positions")

        p0 = [4316.3854, -2232.4071]
        p1 = [4316.4324, -2234.5861999999997]
        p2 = [4324.3128, -2246.0364]
        p3 = [4341.7629, -2266.6388]
        
        pAtT0 = bez.pointInLine(p0,p1,0)
        self.assertEqual(len(pAtT0),2,"x and y") 
        self.assertEqual(pAtT0,p0)
        pAtT1 = bez.pointInLine(p0,p1,1)
        self.assertEqual(pAtT1,p1)

        iAtT0 = bez.interpCubic(p0,p1,p2,p3,0)
        self.assertEqual(iAtT0,p0)
        
        iAtT1 = bez.interpCubic(p0,p1,p2,p3,1)
        self.assertEqual(iAtT1,p3)

    def test_bez_wierc_cubic_index_use(self):
        path19986 = "m 4316.3854,-2232.4071 c 0.047,-2.1791 7.8804,-11.4502 17.4501,-20.6024 10.8015,-10.3303 16.1911,-13.3379 14.2128,-7.9314 -1.7529,4.79 -3.1869,11.4938 -3.1869,14.8973 0,3.4036 -3.7441,7.5089 -8.3202,9.123 -4.5761,1.6142 -10.9946,4.1815 -14.2632,5.7052 -3.2687,1.5237 -5.9202,0.9874 -5.8926,-1.1917 z"
        parseSVGasXML.isClosedPath(path19986)
        numbers = parseSVGasXML.numbersInPath(path19986)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),19)
        self.assertEqual(len(xsys[1]),19)
        
        ind = bez.getCubicTupleIndices(xsys)
        self.assertEqual(len(ind),6)

        self.assertEqual(ind[0],[0,1,2,3])
        self.assertEqual(ind[1],[3,4,5,6])
        self.assertEqual(ind[2],[6,7,8,9])
        self.assertEqual(ind[3],[9,10,11,12])
        self.assertEqual(ind[4],[12,13,14,15])
        self.assertEqual(ind[5],[15,16,17,18])

    def test_bez_area_path_9517(self):
        path19986 = "m 4316.3854,-2232.4071 c 0.047,-2.1791 7.8804,-11.4502 17.4501,-20.6024 10.8015,-10.3303 16.1911,-13.3379 14.2128,-7.9314 -1.7529,4.79 -3.1869,11.4938 -3.1869,14.8973 0,3.4036 -3.7441,7.5089 -8.3202,9.123 -4.5761,1.6142 -10.9946,4.1815 -14.2632,5.7052 -3.2687,1.5237 -5.9202,0.9874 -5.8926,-1.1917 z"
        parseSVGasXML.isClosedPath(path19986)
        numbers = parseSVGasXML.numbersInPath(path19986)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),19)
        self.assertEqual(len(xsys[1]),19)
        # This makes all the interpolations points...
        intXsYS = bez.tenStepsOnPolyCubic(xsys)
        self.assertEqual(len(intXsYS),2)
        self.assertEqual(len(intXsYS[0]),55)
        self.assertEqual(len(intXsYS[1]),55)
        area = parseSVGasXML.polygonArea(intXsYS[0],intXsYS[1])
        self.assertEqual(area,6445)

    def test_bez_area_path_20026(self):
         #       d="m 4644.4095,-2548.3896 c 0,-3.5888 5.4618,-17.2226 12.1128,-30.2972 16.7193,-32.8657 19.9951,-59.5102 8.5584,-69.6047 -13.504,-11.9192 -53.5095,-18.6102 -83.053,-13.8908 -28.3172,4.5236 -30.4106,3.9963 -26.3313,-6.6333 2.1808,-5.684 10.6209,-7.3367 37.4652,-7.3367 38.9853,0 61.8412,5.1796 73.2651,16.6034 7.1663,7.1665 8.4357,6.2244 16.8068,-12.4727 8.8095,-19.6765 33.7221,-53.1188 52.8358,-70.926 10.1483,-9.4546 39.2933,-24.6833 50.9526,-26.6237 28.2093,-4.6946 40.3298,-3.7252 38.5725,3.0851 -1.0117,3.9224 -2.2978,10.3409 -2.8578,14.2633 -0.5601,3.9224 -2.5303,14.6198 -4.3793,23.7721 -1.8485,9.1522 -3.8882,20.3226 -4.5319,24.823 -1.9417,13.5655 -7.1421,15.0562 -10.1878,2.9204 -1.5756,-6.2776 -0.7303,-20.9135 1.8785,-32.5243 2.6087,-11.6108 4.1434,-21.7105 3.4103,-22.4436 -0.7331,-0.7332 -11.8451,0.1022 -24.6935,1.8561 -16.9475,2.3136 -26.8206,6.886 -35.9652,16.6559 -6.9329,7.4068 -14.5038,13.4669 -16.8244,13.4669 -10.009,0 -34.8409,51.7177 -42.2316,87.9566 -4.2666,20.9194 -13.2477,48.2348 -19.9581,60.7007 -13.6166,25.2942 -24.877,37.373 -24.8441,26.6495 z"
    #       id="path20026" />
        path20026 = "m 4644.4095,-2548.3896 c 0,-3.5888 5.4618,-17.2226 12.1128,-30.2972 16.7193,-32.8657 19.9951,-59.5102 8.5584,-69.6047 -13.504,-11.9192 -53.5095,-18.6102 -83.053,-13.8908 -28.3172,4.5236 -30.4106,3.9963 -26.3313,-6.6333 2.1808,-5.684 10.6209,-7.3367 37.4652,-7.3367 38.9853,0 61.8412,5.1796 73.2651,16.6034 7.1663,7.1665 8.4357,6.2244 16.8068,-12.4727 8.8095,-19.6765 33.7221,-53.1188 52.8358,-70.926 10.1483,-9.4546 39.2933,-24.6833 50.9526,-26.6237 28.2093,-4.6946 40.3298,-3.7252 38.5725,3.0851 -1.0117,3.9224 -2.2978,10.3409 -2.8578,14.2633 -0.5601,3.9224 -2.5303,14.6198 -4.3793,23.7721 -1.8485,9.1522 -3.8882,20.3226 -4.5319,24.823 -1.9417,13.5655 -7.1421,15.0562 -10.1878,2.9204 -1.5756,-6.2776 -0.7303,-20.9135 1.8785,-32.5243 2.6087,-11.6108 4.1434,-21.7105 3.4103,-22.4436 -0.7331,-0.7332 -11.8451,0.1022 -24.6935,1.8561 -16.9475,2.3136 -26.8206,6.886 -35.9652,16.6559 -6.9329,7.4068 -14.5038,13.4669 -16.8244,13.4669 -10.009,0 -34.8409,51.7177 -42.2316,87.9566 -4.2666,20.9194 -13.2477,48.2348 -19.9581,60.7007 -13.6166,25.2942 -24.877,37.373 -24.8441,26.6495 z"
        parseSVGasXML.isClosedPath(path20026)
        numbers = parseSVGasXML.numbersInPath(path20026)

        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),67)
        self.assertEqual(len(xsys[1]),67)
        # This makes all the interpolations points...
        intXsYS = bez.tenStepsOnPolyCubic(xsys)
        self.assertEqual(len(intXsYS),2)
        self.assertEqual(len(intXsYS[0]),242)
        self.assertEqual(len(intXsYS[1]),242)
        area = parseSVGasXML.polygonArea(intXsYS[0],intXsYS[1])
        self.assertEqual(area,51742)

    def test_bez_area_path_17286(self):
        path17286 = "m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z"
        self.assertFalse(parseSVGasXML.isClosedPath(path17286))
        
        numbers = parseSVGasXML.numbersInPath(path17286)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        intXsYS = bez.tenStepsOnPolyCubic(xsys)
        area = parseSVGasXML.polygonArea(intXsYS[0],intXsYS[1])
        self.assertEqual(area,53276)


if __name__ == '__main__':
    unittest.main()