import unittest
from MakedirsBlock import MakedirsBlock
from ConsolePrinter import Printer
from Utils import rmtree
import pathlib

class MakedirsBlockTest(unittest.TestCase):
    def test_basic(self):
        testPath = pathlib.Path('Output/MkdirBlockTest/TestDir1')
        block = MakedirsBlock(str(testPath))
        res = block.run()
        self.assertEqual(res, True)
        self.assertTrue(testPath.is_dir())
        rmtree('Output')

    def test_workingDir(self):
        testPath = pathlib.Path('MkdirBlockTest/TestDir1')
        block = MakedirsBlock(str(testPath))
        testPath = pathlib.Path("Output").joinpath(testPath)
        res = block.run(workingDir = "Output")
        self.assertEqual(res, True)
        self.assertTrue(testPath.is_dir())
        rmtree('Output')
    
    def test_basic_withTailoringSlash(self):
        testPath = pathlib.Path('Output/MkdirBlockTest/TestDir1/')
        block = MakedirsBlock(str(testPath))
        res = block.run()
        self.assertEqual(res, True)
        self.assertTrue(testPath.is_dir())
        rmtree('Output')
if __name__ == '__main__':
    unittest.main()

