import shlex

from mazikeen.GeneratorUtils import getYamlString, getYamlInt, getYamlBool
from mazikeen.GeneratorException import GeneratorException
from mazikeen.DiffBlock import DiffBlock
from mazikeen.Utils import diffStrategy
from mazikeen.GeneratorUtils import getYamlString, getYamlList
from mazikeen.ConsolePrinter import Printer, BufferedPrinter

def _parseStrategy(data, line, field):
    strStrat = getYamlString(data, line, field)
    if not any(x for x in diffStrategy if x.name == strStrat):
        raise GeneratorException(f"Invalid value '{strStrat}' for field '{field}' at line {line}")
    
    return diffStrategy[data]

def _parseIgnorelines(data, line, field):
    listIgnorelines = getYamlList(data, line, field)
    for ignoreline in listIgnorelines:
        if (not isinstance(ignoreline, str)):
            raise GeneratorException(f"Field '{field}' expects a list of strings at line {line}")
    return listIgnorelines

def getYamlPaths(data, line = None, field = None):
    if isinstance(data, str):
        dirs = shlex.split(data)
        if (len(dirs) == 2): 
            return dirs
    if (line and field):
        raise GeneratorException(f"Field '{field}' expects two paths at line {line}")
    else:
        raise GeneratorException(f"'diff' block not recognized")

def generateDiffBlock(data):
    if isinstance(data, str):
        return DiffBlock(paths = getYamlPaths(data))
    if not isinstance(data, dict):
        raise DiffBlock(f"'diff' block not recognized")
    args = {}
    key = ""
    knownkeys = {'paths': lambda _data: getYamlPaths(_data, data['__line__'], key),
                 'binarycompare': lambda _data: getYamlBool(_data, data['__line__'], key),
                 'strategy': lambda _data: _parseStrategy(_data, data['__line__'], key),
                 'ignorelines': lambda _data: _parseIgnorelines(_data, data['__line__'], key)}
    for key in data:
        if key == "__line__": continue
        if not key.lower() in knownkeys.keys():
            raise GeneratorException(f"Only one of the following keys are allowed: {[*knownkeys.keys()]} at line {data['__line__']}")
        args[key.lower()] = knownkeys[key.lower()](data[key])
    return DiffBlock(**args)