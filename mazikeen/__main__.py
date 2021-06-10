import os
import io
import glob
import yaml
import time
import pathlib
import argparse
import multiprocessing
import copy
import re

from pathlib import Path, PurePath
from junit_xml import TestSuite, TestCase

import mazikeen.SignalHandler as SignalHandler
from mazikeen.GeneratorLooper import generateSerialBlock, generateParallelBlock
from mazikeen.Loopers import Serial, Parallel
from mazikeen.ConsolePrinter import Printer, BufferedPrinter
from mazikeen.version import __version__
from mazikeen.Utils import ensure_dir
from mazikeen.ScriptDataProcessor import processScriptData

def getScriptFiles(dir, scriptName, maxLevel=2):
    curLevel = 0
    curLevelDirs = [Path(dir)]
    scriptFiles = []
    while(curLevelDirs and (curLevel <= maxLevel)):
        nextLevelDir = []
        for curDir in curLevelDirs:
            tmpNextLevelDir = []
            dirContent = os.listdir(curDir)
            for curFile in map(lambda path: Path(curDir).joinpath(path),dirContent): 
                if curFile.is_dir(): 
                    tmpNextLevelDir.append(curFile)
                elif Path(curFile).name == scriptName:
                    tmpNextLevelDir.clear()
                    scriptFiles.append(str(curFile))
                    break
            nextLevelDir.extend(tmpNextLevelDir)
        curLevelDirs = nextLevelDir
        curLevel += 1
    scriptFiles.sort()
    return scriptFiles

def createTestSuits(scriptFiles, root):
    lenRootParts = len(Path(root).parts)
    testSuits = []
    for scriptFile in map(Path, scriptFiles):
        tc = TestCase(scriptFile.parent.name, file = scriptFile)
        tsName = scriptFile.parts[-3] if len(scriptFile.parts) - lenRootParts > 2 else ""
        ts = next((testSuit for testSuit in testSuits if testSuit.name == tsName), None)
        if ts == None:
            testSuits.append(TestSuite(tsName, [tc]))
        else:
            ts.test_cases.append(tc)

    return testSuits

def parseArguments():
    parser = argparse.ArgumentParser(description='Mazikeen test enviroment')
     
    parser.add_argument( '-p','--pattern', metavar='PATTERN', type=str,
                        help='Only run tests which match pattern. Does support also negative patterns "-PATTERN"')
    parser.add_argument( '-f','--failfast', action='store_true', 
                        help='stop on first faild test as quickly as possible')
    parser.add_argument( '--upgradeScriptFile', action='store_true', 
                        help='save upgraded script file. Script files are upgraded if their version is lower that latest version')
    parser.add_argument( '--scriptName', metavar='NAME', type=str, default="script.yaml",
                        help='Mazikeen script name (`script.yaml` default)')
    parser.add_argument( '-s','--start-directory', dest='start', metavar='DIR', type=pathlib.Path, default=".",
                         help="Directory to start discovering tests ('.' default)")
    parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                         help='Verbose output')
    parser.add_argument('-j', '--jobs', dest='jobs', type=int, default = None, const = multiprocessing.cpu_count(), nargs='?',
                         help='Specifies the number of jobs to run simultaneously')
    parser.add_argument('-r', '--report', dest='reportfile', type=pathlib.Path,
                         help='Create junit test report')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    return parser.parse_args()

def markTestSkipedByPattern(testSuits, pattern):
    if not isinstance(pattern,str): return
    _pattern = copy.copy(pattern)
    isNegativePatern = _pattern.startswith("-")
    if isNegativePatern: _pattern = _pattern[1:]
    try:
        p = re.compile(_pattern)
    except Exception as e:
        print("Invalid --pattern argument \""+pattern+"\":",str(e))
        exit(1)
    for ts in testSuits: 
        for tc in ts.test_cases:
            if ( (p.match(tc.name) != None) == isNegativePatern):
                tc.add_skipped_info("skipped because of --pattern argumet")

def getReport(testSuits, processTime, executionTime):
    tcPassed = 0
    tcSkipped = 0
    tcFailed = 0 
    tcError = 0
    reportTxt = io.StringIO()

    for ts in testSuits:
        for tc in ts.test_cases:
            if tc.is_error(): tcError += 1
            elif tc.is_failure(): tcFailed += 1
            elif tc.is_skipped(): tcSkipped += 1
            else: tcPassed += 1

    print("----------------------------------------------------------------", file = reportTxt)
    print("Total test cases:", tcPassed + tcSkipped + tcError + tcFailed, "passed:", tcPassed, "skipped:", tcSkipped, "error:", tcError, "failed:", tcFailed, file = reportTxt)
    if (tcSkipped > 0):
        print("----------------------------------------------------------------", file = reportTxt)
        print("Skipped:", file = reportTxt)
        for ts in testSuits:
            for tc in ts.test_cases:
                if tc.is_skipped(): print("\t"+ts.name+("/" if ts.name != "" else "")+tc.name, file = reportTxt)

    if (tcError > 0):
        print("----------------------------------------------------------------", file = reportTxt)
        print("Error:", file = reportTxt)
        for ts in testSuits:
            for tc in ts.test_cases:
                if tc.is_error(): print("\t"+ts.name+("/" if ts.name != "" else "")+tc.name, file = reportTxt)

    if (tcFailed > 0):
        print("----------------------------------------------------------------", file = reportTxt)
        print("Failed:", file = reportTxt)
        for ts in testSuits:
            for tc in ts.test_cases:
                if tc.is_failure(): print("\t"+ts.name+("/" if ts.name != "" else "") +tc.name, file = reportTxt)

    print("----------------------------------------------------------------", file = reportTxt)
    print("process time:",  '%.2f' % processTime, "execution time:",  '%.2f' % executionTime, file = reportTxt)

    return {"text" : reportTxt.getvalue(), "passed" : tcPassed, "skipped" : tcSkipped, "error" : tcError, "failed" : tcFailed }

class TestExecuter:
    def __init__(self, testSuite, testCase, upgradeScriptFile):
        self.testSuite = testSuite
        self.testCase = testCase
        self.upgradeScriptFile = upgradeScriptFile

    def run(self, workingDir, variables = {}, printer = Printer()):
        curDir = os.getcwd()
        printer.print("["+"RUN".ljust(10) + "] ---", self.testSuite.name + ("/" if self.testSuite.name != "" else "") + self.testCase.name)
        try:
            startTime = time.time()
            processStartTime = time.process_time()
            data = processScriptData(self.testCase.file, saveUpgradedScript = self.upgradeScriptFile, printer = printer)
            block = generateSerialBlock(data)
            if block == None: return
            res = block.run(workingDir = str(PurePath(self.testCase.file).parent), printer = printer)
            if (not res):
                self.testCase.add_failure_info(printer.errorOutput or "failed")
        except Exception as e:
            self.testCase.add_error_info(str(e))
            printer.print(str(e))
        finally:
            self.testCase.elapsed_sec = time.time() - startTime
            testResStr = "PASSED"
            if self.testCase.is_error(): 
                testResStr = "ERROR"
            elif self.testCase.is_failure(): 
                testResStr = "FAILED"
            printStr = "["+testResStr.rjust(10) + "] --- " + self.testSuite.name + ("/" if self.testSuite.name != "" else "") + self.testCase.name
            if (printer.isVerbose()): 
                printStr += " --- process time: "+  '%.2f' % (time.process_time() - processStartTime) + " execution time: "+  '%.2f' % (time.time() - startTime)
            printer.print(printStr)
        return testResStr == "PASSED"

def main():
    SignalHandler.init()
    args = parseArguments()
    scriptFiles = getScriptFiles(args.start, args.scriptName)
    testSuits = createTestSuits(scriptFiles, args.start)
    markTestSkipedByPattern(testSuits, args.pattern)
    genTestExecuter = [TestExecuter(ts, tc, args.upgradeScriptFile) for ts in testSuits for tc in ts.test_cases if not tc.is_skipped()]
    if (args.jobs == None): 
        runner = Serial(genTestExecuter, failfast=args.failfast)
    else: 
        runner = Parallel(genTestExecuter, failfast=args.failfast, max_workers = args.jobs)
    startTime = time.time()
    processStartTime = time.process_time()
    res = runner.run(".", printer = Printer(args.verbose != None))
    processTime = time.process_time() - processStartTime
    executionTime = time.time() - startTime
    if (args.failfast and res == False) or SignalHandler.failFast(): 
        for ts in testSuits: 
            for tc in ts.test_cases:
                if tc.elapsed_sec == None:
                    if (SignalHandler.failFast()):
                        tc.add_skipped_info("skipped due to " + SignalHandler.signalName())
                    else:
                        tc.add_skipped_info("skipped due to --failfast argument")
    report = getReport(testSuits, processTime, executionTime)
    Printer(args.verbose != None).print(report["text"])
    if (args.reportfile):
        ensure_dir(args.reportfile)
        with open(args.reportfile, "w") as fw:
            fw.write(TestSuite.to_xml_string(testSuits))
    exit(report["error"] > 0)
    
if __name__ == '__main__':
    main()