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

  

    def test_canGetNumbersFromPath(self):
        numbers = parseSVGasXML.numbersInPath("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z")
        self.assertEqual([3622.1906,-2417.0368,  -2.7613,-7.2626,-3.9509,-14.2745,-2.6434,-15.582,1.3074,-1.3075,4.6365,3.5649,7.3978,10.8276,2.7614,7.2627,3.951,14.2746,2.6435,15.582,-1.3075,1.3075,-4.6365,-3.5649,-7.3979,-10.8276],numbers)
        numbers.pop(0) # remove first move position
        numbers.pop(0) # remove second move position
        self.assertEqual([-2.7613,-7.2626,-3.9509,-14.2745,-2.6434,-15.582,1.3074,-1.3075,4.6365,3.5649,7.3978,10.8276,2.7614,7.2627,3.951,14.2746,2.6435,15.582,-1.3075,1.3075,-4.6365,-3.5649,-7.3979,-10.8276],numbers)
        self.assertEqual(max(numbers),15.582)
        self.assertTrue(parseSVGasXML.pathHasNonMoveAbsValueOfGreaterThanF("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z",15))
        self.assertFalse(parseSVGasXML.pathHasNonMoveAbsValueOfGreaterThanF("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z",16))

    def test_canFindPathsWithLessThanFDist(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        paths = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        self.assertEqual(len(paths),2576)


    def test_canGetXSYS(self):
        numbers = parseSVGasXML.numbersInPath("m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z")
        numbers.pop(0) # remove first move position
        numbers.pop(0) # remove second move position
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),len(xsys[1]))

    def test_canGetPolygonArea1(self):
        xs = [4.0,  4.0,  8.0,  8.0, -4.0,-4.0]
        ys = [6.0, -4.0, -4.0, -8.0, -8.0, 6.0]
        self.assertEqual(parseSVGasXML.polygonArea(xs,ys),128.0)

    def test_canGetPolygonArea(self):
        numbers = parseSVGasXML.numbersInPath("m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z")
        numbers.pop(0) # remove first move position
        numbers.pop(0) # remove second move position
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertTrue(parseSVGasXML.polygonArea(xsys[0],xsys[1]) > 1558)


    def test_getIndices(self):
        #       id="path17286" />
        path17286 = "m -3787.5625,2736.5536 c -11.2338,-5.1267 -12.2142,-6.5549 -4.6154,-6.7237 5.3063,-0.1189 12.7945,-4.6931 16.6404,-10.1668 22.9073,-32.603 43.7337,-39.4274 74.6859,-24.4729 12.0567,5.8251 24.9031,8.3654 35.093,6.9395 l 16.0741,-2.2493 -12.636,10.1131 c -15.8078,12.652 -29.9422,12.8398 -45.4969,0.6043 -6.6486,-5.2298 -14.9085,-9.5088 -18.3552,-9.5088 -14.8323,0 -30.8181,11.839 -34.3405,25.4323 -4.4423,17.1435 -8.3174,18.5802 -27.0494,10.0323 z"
        self.assertFalse(parseSVGasXML.isClosedPath(path17286))
        numbers = parseSVGasXML.numbersInPath(path17286)
        xsys =  parseSVGasXML.makeXsYs(numbers)
        self.assertEqual(len(xsys),2)
        self.assertEqual(len(xsys[0]),27)
        self.assertEqual(len(xsys[0]),27)
        xsys[0] =parseSVGasXML.turnMovementsIntoPositions(xsys[0])
        xsys[1] = parseSVGasXML.turnMovementsIntoPositions(xsys[1])
        self.assertEqual(len(xsys[0]),27)
        self.assertEqual(len(xsys[0]),27)

        indices = bez.getCubicTupleIndices(xsys)
        self.assertEqual(len(indices),8)
        
    def test_canGetPolygonAreas(self):

        path13749 = "m 3083.7276,1171.4335 c 1.0703,-3.2102 -2.0467,-4.277 -7.9693,-2.7281 -5.3501,1.399 -8.4852,4.5528 -6.9676,7.0085 3.3966,5.4955 12.5531,2.8715 14.9369,-4.2804 z"
        self.assertTrue(parseSVGasXML.isClosedPath(path13749))
        smallPath13749_area = parseSVGasXML.pathPolyGoneArea(path13749)

        path9725 = "m 2725.9837,-759.84238 c -5.2298,-2.12865 -18.5622,-12.40408 -29.6271,-22.83431 -20.4288,-19.25713 -36.8458,-24.82954 -73.4719,-24.93889 -33.4977,-0.10032 -56.1738,-15.18864 -56.1738,-37.37768 0,-7.41993 4.0284,-15.77761 9.5088,-19.72763 5.2298,-3.76949 9.5088,-8.56327 9.5088,-10.65288 0,-6.95028 23.8154,-41.64566 28.5859,-41.64566 7.1226,0 5.6445,6.95918 -3.7878,17.83452 -4.6655,5.37933 -13.6243,20.75781 -19.9082,34.17443 -11.4096,24.3599 -11.412,24.40692 -1.9559,33.86312 6.8653,6.86556 19.8558,10.63415 47.2417,13.70536 20.7749,2.3298 38.6139,3.39427 39.6428,2.36551 1.0288,-1.02876 -0.8358,-5.13139 -4.1435,-9.11697 -3.7664,-4.5379 -4.1202,-7.24653 -0.9466,-7.24653 2.7875,0 8.8794,6.45211 13.5377,14.33802 4.6584,7.88596 14.4321,16.9773 21.7191,20.20298 7.2876,3.22572 14.3655,9.3795 15.7291,13.67512 3.1854,10.03718 16.2872,13.34288 40.1805,10.13812 23.6703,-3.17486 24.4044,1.08248 1.8152,10.52094 -19.157,8.00425 -23.6717,8.3324 -37.4548,2.72243 z"
        self.assertTrue(parseSVGasXML.isClosedPath(path9725))
        bigPath9725_area = parseSVGasXML.pathPolyGoneArea(path9725)
        self.assertTrue(bigPath9725_area > smallPath13749_area)

        path14189 = "m 3439.3844,1808.4479 c -8.1947,-45.7075 -12.1723,-54.5878 -23.1326,-51.6481 -5.7129,1.5318 -12.8117,2.8146 -15.7756,2.8502 -8.2428,0.1 -10.6295,16.224 -3.4009,22.9767 9.2188,8.6117 7.9903,12.8783 -5.4737,19.0129 -6.9724,3.1769 -11.8861,9.389 -11.8861,15.0268 0,8.6754 3.0586,9.6106 31.4329,9.6106 h 31.4328 z"
        self.assertTrue(parseSVGasXML.isClosedPath(path14189))
        anotherBig14189_area=parseSVGasXML.pathPolyGoneArea(path14189)
        self.assertTrue(anotherBig14189_area > smallPath13749_area)

        path9733 = "m 3642.0836,-740.46454 c -4.1887,-2.65614 2.9582,-6.55267 21.6264,-11.7907 22.6619,-6.3586 32.2905,-12.50492 51.4232,-32.82595 12.9472,-13.75138 29.3604,-28.74542 36.4735,-33.32016 18.5736,-11.94541 47.1329,-41.44441 44.4024,-45.86288 -1.2765,-2.06522 -12.5597,-2.07064 -25.0738,-0.0143 -39.2891,6.46325 -95.6051,4.98895 -110.8648,-2.90233 -16.6928,-8.63202 -29.3219,-31.17103 -29.3219,-52.3295 0,-32.52784 31.3772,-83.06684 58.0038,-93.42674 18.0829,-7.0356 48.3015,-0.4945 65.4906,14.17619 18.4386,15.73701 19.2017,19.35246 3.4484,16.34106 -6.5373,-1.2497 -11.886,-3.81879 -11.886,-5.70914 0,-5.61849 -23.1802,-14.47211 -37.8903,-14.47211 -10.5444,0 -18.6739,5.70844 -35.5464,24.96063 -40.713,46.45465 -38.5535,84.90459 5.7875,103.0394 15.0131,6.14008 26.8002,6.00905 109.2503,-1.21428 19.6124,-1.71824 24.9607,-0.71364 24.9607,4.6888 0,12.85432 -14.0693,32.4997 -38.6354,53.94752 -13.4778,11.76717 -36.0346,32.09229 -50.1262,45.16693 -32.6101,30.25684 -64.2478,42.49917 -81.522,31.54529 z"
        self.assertTrue(parseSVGasXML.isClosedPath(path9733))
        anotherBig_9733_area=parseSVGasXML.pathPolyGoneArea(path9733)
        self.assertFalse(anotherBig_9733_area > smallPath13749_area)
        
        path9635 = "m 3325.0398,-1454.2681 c -1.616,-2.6149 -6.2259,-4.7544 -10.2439,-4.7544 -4.0184,0 -12.9847,-3.9069 -19.9257,-8.6819 -7.153,-4.9208 -22.9182,-9.1992 -36.3922,-9.876 -25.0591,-1.2589 -34.0773,-5.742 -28.7827,-14.3088 4.0098,-6.488 29.5881,-6.804 33.5371,-0.4141 1.616,2.6149 7.0912,4.7544 12.1666,4.7544 5.0758,0 9.2283,2.1395 9.2283,4.7544 0,2.615 4.2789,4.7545 9.5088,4.7545 5.2299,0 9.5088,2.1394 9.5088,4.7544 0,2.6149 5.4895,4.7544 12.1984,4.7544 15.2926,0 31.7681,8.5127 28.0668,14.5018 -3.6662,5.932 -15.1462,5.7869 -18.8703,-0.2387 z"
        self.assertTrue(parseSVGasXML.isClosedPath(path9635))
        anotherBig_9635_area=parseSVGasXML.pathPolyGoneArea(path9635)
        self.assertFalse(anotherBig_9733_area > anotherBig_9635_area)

    # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
    # this is the problem I am not yet calculating the area of a bezier


    def test_canFindPathsWithLessThanFArea(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        paths = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        self.assertEqual(len(paths),2576)
        if True:
            self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,1600)),1691)
            self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(paths,400)),1040)
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
        redLines = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        #redLinesToSkip = parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(redLines,1112)
        #redLinesToSkip = parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(redLines,50)
        redLinesToSkip = parseSVGasXML.countAllTheClosedPathsWithAreaLessThanF(redLines,1600)
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