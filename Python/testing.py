import unittest
import loadFile
import parseSVGasXML
import writeNewXML
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

    def test_canFindPathsWithLessThanNCommmas(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        paths = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        self.assertEqual(len(paths),2576)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(paths,12)),958)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(paths,11)),956)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(paths,10)),23)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(paths,9)),8)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(paths,8)),1)

    def test_canGetNumbersFromPath(self):
        numbers = parseSVGasXML.numbersInPath("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z")
        self.assertEqual([3622.1906,2417.0368,2.7613,7.2626,3.9509,14.2745,2.6434,15.582,1.3074,1.3075,4.6365,3.5649,7.3978,10.8276,2.7614,7.2627,3.951,14.2746,2.6435,15.582,1.3075,1.3075,4.6365,3.5649,7.3979,10.8276],numbers)
        numbers.pop(0) # remove first move position
        numbers.pop(0) # remove second move position
        self.assertEqual([2.7613,7.2626,3.9509,14.2745,2.6434,15.582,1.3074,1.3075,4.6365,3.5649,7.3978,10.8276,2.7614,7.2627,3.951,14.2746,2.6435,15.582,1.3075,1.3075,4.6365,3.5649,7.3979,10.8276],numbers)
        self.assertEqual(max(numbers),15.582)
        self.assertTrue(parseSVGasXML.pathHasNonMoveAbsValueOfGreaterThanF("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z",15))
        self.assertFalse(parseSVGasXML.pathHasNonMoveAbsValueOfGreaterThanF("m 3622.1906,-2417.0368 c -2.7613,-7.2626 -3.9509,-14.2745 -2.6434,-15.582 1.3074,-1.3075 4.6365,3.5649 7.3978,10.8276 2.7614,7.2627 3.951,14.2746 2.6435,15.582 -1.3075,1.3075 -4.6365,-3.5649 -7.3979,-10.8276 z",16))

    def test_canFindPathsWithLessThanFDist(self):
        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        paths = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        self.assertEqual(len(paths),2576)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,30)),1483)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,20)),1146)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,7)),204)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,5)),47)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,3)),0)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,2)),0)
        self.assertEqual(len(parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(paths,1)),0)

    def test_writeNewXML(self):
        if loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"):
            os.remove(".\\testFiles\\tmp_round_church_two_paths_140x140.svg")

        self.assertTrue(loadFile.checkPathExists(".\\testFiles\\round_church_two_paths_140x140.svg"))
        self.assertFalse(loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"))

        outgroups = parseSVGasXML.getGroups(".\\testFiles\\round_church_two_paths_140x140.svg")
        redLines = parseSVGasXML.countAllTheClosedPathsInThisGroup(outgroups[0])
        #redLinesToSkip = parseSVGasXML.countAllTheClosedPathsWithFewerThanNCommas(redLines,1112)
        redLinesToSkip = parseSVGasXML.countAllTheClosedPathsWithMaxDistLessThanF(redLines,50)
        writeNewXML.copyFileLineByLine(".\\testFiles\\round_church_two_paths_140x140.svg",".\\testFiles\\tmp_round_church_two_paths_140x140.svg",redLinesToSkip)
        self.assertTrue(loadFile.checkPathExists(".\\testFiles\\tmp_round_church_two_paths_140x140.svg"))

if __name__ == '__main__':
    unittest.main()