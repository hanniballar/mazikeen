import unittest
import subprocess
import os
import re
import platform
from mazikeen.Utils import diff, rmtree, diffStrategy
from xmldiff import main
from distutils.dir_util import copy_tree

class Blackbox(unittest.TestCase):
    def test_simple(self):
        testDir = "TestFiles/Blackbox_test/simple/"
        outDir = testDir + "TestOutput"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))

    def test_inputFileNoutputFile(self):
        testDir = "TestFiles/Blackbox_test/inputFileNoutputFile/"
        outDir = testDir + "TestOutput"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_blockinBlock(self):
        testDir = "TestFiles/Blackbox_test/blockinBlock/"
        outDir = testDir + "TestOutput"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_testsuitsNtestcases_simple(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases/"
        outDir = testDir + "TestOutput/simple/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
        self.assertTrue(diff(testDir + "TestOutput/simple/mazikenout.txt", testDir + "TestExpected/simple/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_testsuitsNtestcases_report(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases/"
        outDir = testDir + "TestOutput/report"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "-r", "TestOutput/report/report.xml"], stdout=of, stderr=of, cwd = testDir)
        
        with open(outDir + "/report.xml", "r") as ifile:
            with open(outDir + "/report_diff.xml", "w") as ofile:
                for line in ifile:
                    line = re.sub(r"time=\".+?\"", "time=\"\"", line)
                    line = re.sub(r"\\", "/", line)
                    ofile.write(line)
        self.assertEqual(main.diff_files(testDir + "TestOutput/report/report_diff.xml", testDir + "TestExpected/report/report_diff.xml"), [])
        
    def test_testsuitsNtestcases_wait_parallel(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases_wait/"
        outDir = testDir + "TestOutput/parallel/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "-r", "TestOutput/parallel/report.xml", "-j", "2"], stdout=of, stderr=of, cwd = testDir)
        
        with open(outDir + "/report.xml", "r") as ifile:
            with open(outDir + "/report_diff.xml", "w") as ofile:
                for line in ifile:
                    line = re.sub(r"time=\".+?\"", "time=\"\"", line)
                    line = re.sub(r"\\", "/", line)
                    ofile.write(line)
        self.assertEqual(main.diff_files(outDir + "/report_diff.xml", outDir + "/report_diff.xml"), [])
        self.assertTrue(diff(testDir + "TestOutput/parallel/mazikenout.txt", testDir + "TestExpected/parallel/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_testsuitsNtestcases_waitNfail_parallel(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases_waitNfail/"
        outDir = testDir + "TestOutput/parallel/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "-r", "TestOutput/parallel/report.xml", "-j", "2"], stdout=of, stderr=of, cwd = testDir)
        
        with open(outDir + "/report.xml", "r") as ifile:
            with open(outDir + "/report_diff.xml", "w") as ofile:
                for line in ifile:
                    line = re.sub(r"time=\".+?\"", "time=\"\"", line)
                    line = re.sub(r"\\", "/", line)
                    ofile.write(line)
        self.assertEqual(main.diff_files(outDir + "/report_diff.xml", outDir + "/report_diff.xml"), [])
        self.assertTrue(diff(testDir + "TestOutput/parallel/mazikenout.txt", testDir + "TestExpected/parallel/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_testsuitsNtestcases_waitNfail_serial(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases_waitNfail/"
        outDir = testDir + "TestOutput/serial/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "-r", "TestOutput/serial/report.xml", "-j", "2"], stdout=of, stderr=of, cwd = testDir)
        
        with open(outDir + "/report.xml", "r") as ifile:
            with open(outDir + "/report_diff.xml", "w") as ofile:
                for line in ifile:
                    line = re.sub(r"time=\".+?\"", "time=\"\"", line)
                    line = re.sub(r"\\", "/", line)
                    ofile.write(line)
        self.assertEqual(main.diff_files(outDir + "/report_diff.xml", outDir + "/report_diff.xml"), [])
        self.assertTrue(diff(testDir + "TestOutput/serial/mazikenout.txt", testDir + "TestExpected/serial/mazikenout.txt", ignore = ["process time: .*"]))

    def test_testsuitsNtestcases_waitNfail_failFast(self):
        testDir = "TestFiles/Blackbox_test/testsuitsNtestcases_waitNfail/"
        outDir = testDir + "TestOutput/failFast/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "-r", "TestOutput/failFast/report.xml", "-j", "2", "--failfast"], stdout=of, stderr=of, cwd = testDir)
        
        with open(outDir + "/report.xml", "r") as ifile:
            with open(outDir + "/report_diff.xml", "w") as ofile:
                for line in ifile:
                    line = re.sub(r"time=\".+?\"", "time=\"\"", line)
                    line = re.sub(r"\\", "/", line)
                    ofile.write(line)
        self.assertEqual(main.diff_files(outDir + "/report_diff.xml", outDir + "/report_diff.xml"), [])
        self.assertTrue(diff(testDir + "TestOutput/failFast/mazikenout.txt", testDir + "TestExpected/failFast/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_upgradeScriptData1_0_0(self):
        testDir = "TestFiles/Blackbox_test/upgradeScriptData1.0.0/"
        outDir = testDir + "TestOutput/"
        rmtree(outDir)
        os.makedirs(outDir)
        copy_tree(testDir+"TestInput", outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "--upgradeScriptFile"], stdout=of, stderr=of, cwd = outDir)

        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
        self.assertTrue(diff(testDir + "TestOutput/script.yaml", testDir + "TestExpected/script.yaml"))
        
    def test_upgradeScriptData1_1_0(self):
        testDir = "TestFiles/Blackbox_test/upgradeScriptData1.1.0/"
        outDir = testDir + "TestOutput/"
        rmtree(outDir)
        os.makedirs(outDir)
        copy_tree(testDir+"TestInput", outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen", "--upgradeScriptFile"], stdout=of, stderr=of, cwd = outDir)

        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
        self.assertTrue(diff(testDir + "TestOutput/script.yaml", testDir + "TestExpected/script.yaml"))
        
    def test_emptyTest(self):
        testDir = "TestFiles/Blackbox_test/emptyTest/"
        outDir = testDir + "TestOutput/"
        rmtree(outDir)
        os.makedirs(outDir)
        with open(outDir + "/mazikenout.txt", "w") as of:
            subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
        self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
        
    def test_shellWindows(self):
        if (platform.system() == "Windows"):
            testDir = "TestFiles/Blackbox_test/shellWin/"
            outDir = testDir + "TestOutput"
            rmtree(outDir)
            os.makedirs(outDir)
            with open(outDir + "/mazikenout.txt", "w") as of:
                subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
            self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))
            
    def test_shellLinux(self):
        if (platform.system() == "Linux"):
            testDir = "TestFiles/Blackbox_test/shellLinux/"
            outDir = testDir + "TestOutput"
            rmtree(outDir)
            os.makedirs(outDir)
            with open(outDir + "/mazikenout.txt", "w") as of:
                subprocess.run(["mazikeen"], stdout=of, stderr=of, cwd = testDir)
            self.assertTrue(diff(testDir + "TestOutput/mazikenout.txt", testDir + "TestExpected/mazikenout.txt", ignore = ["process time: .*"]))

    
if __name__ == '__main__':
    unittest.main()
