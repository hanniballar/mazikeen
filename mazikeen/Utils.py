import re
import os
import shutil
import stat
import pathlib
from enum import Enum

from mazikeen.ConsolePrinter import Printer
from mazikeen.GeneratorException import GeneratorException

__replaceVariablesExp = re.compile(r'(?<!\\)\${.*?}')
def replaceVariables(line, dictReplVar, printer = Printer()):
    global __replaceVariablesExp
    if line == None: return (True, line)
    searchStart = 0
    while (True):
        m = __replaceVariablesExp.search(line[searchStart:])
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
    
def __getCompareLine(line, fh, compiledignore):
    while(True):
        if not line: return line
        try:
            strLine = line.decode('utf-8')
        except:
            return line

        lineMatchesSpan = []
        for ignoreLine in compiledignore:
            itMatch = ignoreLine.finditer(strLine)
            for m in itMatch: lineMatchesSpan.append(m.span())
        lineMatchesSpan.sort()

        def concatenatelineMatches(lineMatchesSpan):
            idx = 0
            while idx < len(lineMatchesSpan) - 1:
                cmpIdx = idx + 1
                while cmpIdx < len(lineMatchesSpan):
                    if lineMatchesSpan[idx][1] > lineMatchesSpan[cmpIdx][0]:
                        lineMatchesSpan[idx] = (lineMatchesSpan[idx][0], max(lineMatchesSpan[idx][1], lineMatchesSpan[cmpIdx][1]))
                        cmpIdx = idx + 1
                        del lineMatchesSpan[cmpIdx]
                    else: cmpIdx += 1
                idx += 1
        concatenatelineMatches(lineMatchesSpan)

        def deleteLineMatchesFromString(strLine, lineMatchesSpan):
            listLine = list(strLine)
            for matchSpan in reversed(lineMatchesSpan):
                del listLine[matchSpan[0]:matchSpan[1]]
            return "".join(listLine)
        newLine = deleteLineMatchesFromString(strLine, lineMatchesSpan)
        if not newLine in ['', '\n', '\r', '\r\n']:
            return str.encode(newLine)
        line = fh.readline()
    return line

def normalizeEOL(line):
    # Todo: can be optimized
    if len(line) >=2 and line[-2:] == bytes('\r\n', 'utf-8'): 
        line = line[:-2] + bytes('\n', 'utf-8')
    elif len(line) >=1 and line[-1] == bytes('\r', 'utf-8'): 
        line = line[:-1] + bytes('\n', 'utf-8')
    return line

def diffFiles(fileL, fileR, compiledignore = [], binaryCompare = False):
    def areLinesIdentical(lineL, lineR, binaryCompare):
        def normalizeEOL(line):
            if len(line) >=2 and line[-2:] == bytes('\r\n', 'utf-8'): 
                line = line[:-2] + bytes('\n', 'utf-8')
            elif len(line) >=1 and line[-1] == bytes('\r', 'utf-8'): 
                line = line[:-1] + bytes('\n', 'utf-8')
            return line

        if lineL == lineR: return True #This is the most likely scenario so it has priority
        if binaryCompare == False:
            return normalizeEOL(lineL) == normalizeEOL(lineR)
        return False

    with open(fileL, "rb") as fhL:
        with open(fileR, "rb") as fhR:
            while True:
                lineL = fhL.readline()
                lineR = fhR.readline()
                if (not lineL and not lineR): break #EOF reached
                if areLinesIdentical(lineL, lineR, binaryCompare) == False:
                    lineL = __getCompareLine(lineL, fhL, compiledignore)
                    lineR = __getCompareLine(lineR, fhR, compiledignore)
                    if areLinesIdentical(lineL, lineR, binaryCompare) == False:
                        return False
    return True

def diff(pathL, pathR, binaryCompare = False, diffStrategy = diffStrategy.All, ignore = [], printer = Printer(verbose = True)):
    rootM = pathlib.Path(pathL)
    rootS = pathlib.Path(pathR)
    compiledignore = list(map(lambda x: re.compile(x), ignore))
    if (rootM.is_file() and rootS.is_file()):
        if (not diffFiles(rootM, rootS, compiledignore = compiledignore, binaryCompare = binaryCompare)):
            printer.error(f"diff failed: '{rootM}' != '{rootS}'")
            return False
        return True

    for file in [rootM, rootS]:
        if not file.exists():
            printer.error(f"diff failed: '{file}' doesn't exist")
            return False

    filesM = set(__listAllFilesWithoutRoot(pathL))
    filesS = set(__listAllFilesWithoutRoot(pathR))
    
    swapFiles = False
    if diffStrategy == diffStrategy.IgnoreLeftOrphans:
        swapFiles = True
        filesM, filesS = filesS, filesM
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
            (pathL_, pathR_) = (pathM, pathS) if not swapFiles else (pathS, pathM)
            printer.error(f"diff failed: '{pathL_}' != '{pathR_}'")
            return False

    comFiles = [(pathM, pathS) for pathM, pathS in comPaths if pathM.is_file()]
    for fileM, fileS in comFiles:
        if (not diffFiles(fileM, fileS, binaryCompare = binaryCompare, compiledignore = compiledignore)):
            (fileL, fileR) = (fileM, fileS) if not swapFiles else (fileS, fileM)
            printer.error(f"diff failed: '{fileL}' != '{fileR}'")
            return False
    return True

