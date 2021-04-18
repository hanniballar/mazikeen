import re
import os
import shutil
import stat
import pathlib
from enum import Enum

from mazikeen.ConsolePrinter import Printer
from mazikeen.GeneratorException import GeneratorException

replaceVariablesExp = re.compile(r'(?<!\\)\${.*?}')
def replaceVariables(line, dictReplVar, printer = Printer()):
    if line == None: return (True, line)
    searchStart = 0
    while (True):
        m = re.search(r'(?<!\\)\${.*?}', line[searchStart:]) #ToDo: optimize
        if not m: 
            break
        foundVar = m.group()[2:-1]
        replaceVal = dictReplVar.get(foundVar)
        if (replaceVal):
            strReplaceVal = str(replaceVal)
            line = line[:searchStart + m.start()] + strReplaceVal + line[searchStart + m.end():]
            searchStart += m.start() + len(strReplaceVal)
        else:
            raise GeneratorException("Variable " + str(m.group()) + " does not exist")
    line = line.replace(r'\$', "$")
    return line

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if (directory) and (not os.path.exists(directory)):
        os.makedirs(directory)

def rmtree(path, printer = Printer()):
    try:
        def remove_readonly(fn, path, excinfo):
            os.chmod(path, stat.S_IWRITE)
            fn(path)
        if os.path.exists(path):
            shutil.rmtree(path, onerror=remove_readonly, ignore_errors = False)
        return True
    except Exception as e:
        printer.error("rmtree:", e)
        return False

class diffStrategy(Enum):
   IgnoreLeftOrphans = 0
   IgnoreRightOrphans = 1
   IgnoreOrphans = 2
   All = 3

def __listAllFilesWithoutRoot(path):
    allFilesWithRoot = [pathlib.Path(dp) / f for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn + dn]
    rootMathLen = len(pathlib.Path(path).parts)
    filesWithoutRoot = [pathlib.Path(*f.parts[rootMathLen:]) for f in allFilesWithRoot]
    return filesWithoutRoot
    
def __getCompareLine(line, fh, compiledIgnoreLines):
    repeate = True
    while(repeate):
        if not line: return line
        repeate = False
        try:
            strLine = line.decode('utf-8')
        except:
            return line
        for ignoreLine in compiledIgnoreLines:
            if ignoreLine.match(strLine):
                line = fh.readline()
                repeate = True
                break
    return line

def normalizeEOL(line):
    # Todo: can be optimized
    if len(line) >=2 and line[-2:] == bytes('\r\n', 'utf-8'): 
        line = line[:-2] + bytes('\n', 'utf-8')
    elif len(line) >=1 and line[-1] == bytes('\r', 'utf-8'): 
        line = line[:-1] + bytes('\n', 'utf-8')
    return line

def diffFiles(fileL, fileR, compiledIgnoreLines = [], binaryCompare = False):
    with open(fileL, "rb") as fhL:
        with open(fileR, "rb") as fhR:
            while True:
                lineL = fhL.readline()
                lineR = fhR.readline()
                if (binaryCompare == False):
                    lineL = normalizeEOL(lineL)
                    lineR = normalizeEOL(lineR)
                if (not lineL and not lineR): break
                if lineL != lineR:
                    lineL = __getCompareLine(lineL, fhL, compiledIgnoreLines)
                    lineR = __getCompareLine(lineR, fhR, compiledIgnoreLines)
                    if (binaryCompare == False):
                        lineL = normalizeEOL(lineL)
                        lineR = normalizeEOL(lineR)
                    if lineL != lineR:
                        return False
    return True

def diff(pathL, pathR, binaryCompare = False, diffStrategy = diffStrategy.All, ignoreLines = [], printer = Printer(verbose = True)):
    rootM = pathlib.Path(pathL)
    rootS = pathlib.Path(pathR)
    compiledIgnoreLines = list(map(lambda x: re.compile(x), ignoreLines))
    if (rootM.is_file() and rootS.is_file()):
        if (not diffFiles(rootM, rootS, compiledIgnoreLines = compiledIgnoreLines, binaryCompare = binaryCompare)):
            printer.error(f"diff failed: '{rootM}' != '{rootS}'")
            return False
        return True

    for file in [rootM, rootS]:
        if not file.exists():
            printer.error(f"diff failed: '{file}' doesn't exist")
            return False

    filesM = set(__listAllFilesWithoutRoot(pathL))
    filesS = set(__listAllFilesWithoutRoot(pathR))
    
    if diffStrategy == diffStrategy.IgnoreLeftOrphans:
        filesM, filesS = filesS, filesS
        rootM, rootS = rootS, rootM
    
    if diffStrategy != diffStrategy.IgnoreOrphans:
        for file in (filesM - filesS):
            printer.error(f"diff failed: '{str(rootM/file)}' not in '{rootS / file.parent}'")
            return False
    
    if diffStrategy == diffStrategy.All:
        for file in (filesS - filesM):
            printer.error(f"diff failed: '{str(rootS/file)}' not in '{rootM / file.parent}'")
            return False
    
    comPaths =[(rootM/path, rootS/path) for path in (filesM & filesS)]
    
    for pathM, pathS in comPaths:
        if (pathM.is_file() != pathS.is_file()):
            printer.error(f"diff failed: '{pathM}' != '{pathS}'")
            return False
    

    comFiles = [(pathM, pathS) for pathM, pathS in comPaths if pathM.is_file()]
    for fileM, fileS in comFiles:
        if (not diffFiles(fileM, fileS, binaryCompare = binaryCompare, compiledIgnoreLines = compiledIgnoreLines)):
            printer.error(f"diff failed: '{fileM}' != '{fileS}'")
            return False
    return True

