import unittest
import io
import os
import sys
import pathlib
from Utils import replaceVariables, diff, diffStrategy
from GeneratorException import GeneratorException

class replaceVariables_Test(unittest.TestCase):
    def test_basic(self):
        line = replaceVariables("Replace ${repl1} ${repl2} ${repl3} \${esc}", {'repl1' : '${repl2}', 'repl2' : '${repl3}', 'repl3' : '${repl1}'})
        self.assertEqual(line, "Replace ${repl2} ${repl3} ${repl1} ${esc}")
        
    def test_missingVar(self):
        with self.assertRaisesRegex(GeneratorException, "Variable .*") as e:
            line = replaceVariables("Replace ${repl1} ${repl2} ${repl3} ${repl4}", {'repl1' : '${repl2}', 'repl2' : '${repl3}', 'repl3' : '${repl1}'})

class diff_Test(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(diff("TestFiles/diff_Test/test_basic/cmp1", "TestFiles/diff_Test/test_basic/cmp2"))

    def test_basicFileOnly(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.assertTrue(diff("TestFiles/diff_Test/test_basicFileOny/valid1.txt", "TestFiles/diff_Test/test_basicFileOny/valid1.txt"))
        self.assertFalse(diff("TestFiles/diff_Test/test_basicFileOny/invalid1.txt", "TestFiles/diff_Test/test_basicFileOny/invalid2.txt"))
        sys.stdout = sys.__stdout__
        str = capturedOutput.getvalue()
        self.assertEqual(r"diff failed: 'TestFiles\diff_Test\test_basicFileOny\invalid1.txt' != 'TestFiles\diff_Test\test_basicFileOny\invalid2.txt'"+"\n", capturedOutput.getvalue())

    def test_LinuxNWindowsEOL(self):
        self.assertTrue(diff("TestFiles/diff_Test/test_LinuxNWindowsEOL/cmp1", "TestFiles/diff_Test/test_LinuxNWindowsEOL/cmp2"))

    def test_LinuxNWindowsEOLBinary(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.assertFalse(diff("TestFiles/diff_Test/test_LinuxNWindowsEOL/cmp1", "TestFiles/diff_Test/test_LinuxNWindowsEOL/cmp2", binaryCompare = True))
        sys.stdout = sys.__stdout__
        expectedPath0 = pathlib.Path(r"TestFiles\diff_Test\test_LinuxNWindowsEOL\cmp1\file1.txt")
        expectedPath1 = pathlib.Path(r"TestFiles\diff_Test\test_LinuxNWindowsEOL\cmp2\file1.txt")
        self.assertEqual(f"diff failed: '{expectedPath0}' != '{expectedPath1}'\n", capturedOutput.getvalue())

    def test_IgnoreLeftOrphans(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        self.assertFalse(diff("TestFiles/diff_Test/test_LeftOrphans/cmp1", "TestFiles/diff_Test/test_LeftOrphans/cmp2"))
        self.assertTrue(diff("TestFiles/diff_Test/test_LeftOrphans/cmp1", "TestFiles/diff_Test/test_LeftOrphans/cmp2", diffStrategy = diffStrategy.IgnoreLeftOrphans))
        
        sys.stdout = sys.__stdout__
        
        expectedPath0 = pathlib.Path(r"TestFiles\diff_Test\test_LeftOrphans\cmp1\f2\file3.txt")
        expectedPath1 = pathlib.Path(r"TestFiles\diff_Test\test_LeftOrphans\cmp2\f2")
        self.assertEqual(f"diff failed: '{expectedPath0}' not in '{expectedPath1}'\n", capturedOutput.getvalue())

    def test_IgnoreRightOrphans(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        self.assertFalse(diff("TestFiles/diff_Test/test_RightOrphans/cmp1", "TestFiles/diff_Test/test_RightOrphans/cmp2"))
        self.assertTrue(diff("TestFiles/diff_Test/test_RightOrphans/cmp1", "TestFiles/diff_Test/test_RightOrphans/cmp2", diffStrategy = diffStrategy.IgnoreRightOrphans))
        
        sys.stdout = sys.__stdout__
        
        expectedPath0 = pathlib.Path(r"TestFiles\diff_Test\test_RightOrphans\cmp2\f1\file3.txt")
        expectedPath1 = pathlib.Path(r"TestFiles\diff_Test\test_RightOrphans\cmp1\f1")
        self.assertEqual(f"diff failed: '{expectedPath0}' not in '{expectedPath1}'\n", capturedOutput.getvalue())

    def test_IgnoreOrphans(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        self.assertTrue(diff("TestFiles/diff_Test/test_LeftNRightOrphans/cmp1", "TestFiles/diff_Test/test_LeftNRightOrphans/cmp2", diffStrategy = diffStrategy.IgnoreOrphans))

        sys.stdout = sys.__stdout__
        self.assertEqual("", capturedOutput.getvalue())

    def test_fileAsDirectory(self):
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        expectedPath0 = pathlib.Path(r"TestFiles\diff_Test\test_fileAsDirectory\cmp1\f2\file3.txt")
        expectedPath1 = pathlib.Path(r"TestFiles\diff_Test\test_fileAsDirectory\cmp2\f2\file3.txt")
        if not os.path.exists(expectedPath0):
            os.makedirs(expectedPath0)
        self.assertFalse(diff("TestFiles/diff_Test/test_fileAsDirectory/cmp1", "TestFiles/diff_Test/test_fileAsDirectory/cmp2"))

        sys.stdout = sys.__stdout__
        self.assertEqual(f"diff failed: '{expectedPath0}' != '{expectedPath1}'\n", capturedOutput.getvalue())

    def test_InvalidPath(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        self.assertFalse(diff("invalidPath1", "invalidPath2"))

        sys.stdout = sys.__stdout__
        expectedPath0 = pathlib.Path(r"TestFiles\diff_Test\test_fileAsDirectory\cmp1\f2\file3.txt")
        expectedPath1 = pathlib.Path(r"TestFiles\diff_Test\test_fileAsDirectory\cmp2\f2\file3.txt")
        self.assertEqual(f"diff failed: 'invalidPath1' doesn't exist\n", capturedOutput.getvalue())

    def test_IgnoreLine(self):
        self.assertTrue(diff("TestFiles/diff_Test/test_IgnoreLines/cmp1", "TestFiles/diff_Test/test_IgnoreLines/cmp2", ignoreLines = ["ignoreLine1", "ignoreLine2", "ignoreLine3", "ignoreLinePattern.*"]))

if __name__ == '__main__':
    unittest.main()
