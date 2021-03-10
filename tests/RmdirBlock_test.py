import unittest
import os
from RmdirBlock import RmdirBlock
from ConsolePrinter import Printer
from Utils import ensure_dir
import pathlib

class RmdirsBlockTest(unittest.TestCase):
    def test_basic(self):
        printer = Printer();
        testPath = pathlib.Path('TestFiles/RmdirBlockTest/Output/TestDir1')
        if not os.path.exists(testPath):
            os.makedirs(testPath)
        self.assertTrue(testPath.is_dir())
        block = RmdirBlock('RmdirBlockTest/Output')
        res = block.run(workingDir = "TestFiles")
        self.assertEqual(res, True)
        self.assertFalse(pathlib.Path('TestFiles/Output').is_dir())
    
    def test_basic_withTailoringSlash(self):
        printer = Printer();
        testPath = pathlib.Path('TestFiles/RmdirBlockTest/Output/TestDir1/')
        if not os.path.exists(testPath):
            os.makedirs(testPath)
        self.assertTrue(testPath.is_dir())
        block = RmdirBlock('RmdirBlockTest/Output')
        res = block.run(workingDir = "TestFiles")
        self.assertEqual(res, True)
        self.assertFalse(pathlib.Path('TestFiles/RmdirBlockTest/Output').is_dir())

if __name__ == '__main__':
    unittest.main()

