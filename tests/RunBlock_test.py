import unittest
import os
import io
import sys
from RunBlock import RunBlock
from ConsolePrinter import Printer
from Utils import rmtree

class RunBlockTest(unittest.TestCase):
    def test_basic(self):
        cmdExe = RunBlock('echo "Hello World"')
        res = cmdExe.run()
        self.assertEqual(res, True)
        
    def test_basicVerbose(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        printer = Printer(verbose = True);
        cmdString = 'echo "Hello World"'
        cmdExe = RunBlock(cmdString)
        res = cmdExe.run(printer = printer)
        sys.stdout = sys.__stdout__
        expectedResult = "cwd: " + os.getcwd() + "\n" + 'call: '+ cmdString + "\n";
        
        self.assertEqual(res, True)
        self.assertEqual(expectedResult, capturedOutput.getvalue())
    
    def test_unexpectedExitCodeVerbose(self):
        printer = Printer(verbose = True);
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        cmdString = 'exit 1'
        cmdExe = RunBlock(cmdString)
        res = cmdExe.run(printer = printer)
        sys.stdout = sys.__stdout__
        expectedResult = "cwd: " + os.getcwd() + "\n" + 'call: '+ cmdString + "\n" + 'Error: different exitcode received: 1 != 0 for command \'exit 1\'' + "\n";
        
        self.assertEqual(res, False)
        resStr = capturedOutput.getvalue()
        self.assertEqual(expectedResult, capturedOutput.getvalue())
        
    def test_inputfileNoutputfile(self):
        rmtree("Output")
        printer = Printer(verbose = True)
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        cmdExe = RunBlock("python RunBlock_test/stdinTostdout.py", inputfile="RunBlock_test/stdinTostdout.py", outputfile="RunBlock_test/Output/inputfileNoutputfile.txt")
        res = cmdExe.run(workingDir = "TestFiles",printer = printer)
        sys.stdout = sys.__stdout__
        
        self.assertEqual(res, True)
        with open("TestFiles/RunBlock_test/stdinTostdout.py", "r") as fh1:
            with open("TestFiles/RunBlock_test/Output/inputfileNoutputfile.txt", "r") as fh2:
                self.assertEqual(fh1.read(), fh2.read())
        rmtree("TestFiles/RunBlock_test/Output")

if __name__ == '__main__':
    unittest.main()

