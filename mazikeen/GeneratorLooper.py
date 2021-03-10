import itertools

from mazikeen.Loopers import Serial, Parallel
from mazikeen.GeneratorException import GeneratorException
from mazikeen.GeneratorRunBlock import generateRunBlock
from mazikeen.GeneratorMakedirs import generateMakedirs
from mazikeen.GeneratorRmdir import generateRmdir
from mazikeen.GeneratorDiffBlock import generateDiffBlock
from mazikeen.GeneratorUtils import getYamlInt, getYamlBool
from mazikeen.ConsolePrinter import Printer, BufferedPrinter

def _getVariables(data):
    dictVar = {}
    for key in data:
        if key == "__line__": continue
        dictVar[key] = data[key]
    return dictVar
def _dict_product(dicts):
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))
def __dict_zip_longest(dicts):
    return (dict(zip(dicts, x)) for x in itertools.zip_longest(*dicts.values()))
def _dict_zip(dicts):
    return (dict(zip(dicts, x)) for x in zip(*dicts.values()))
def _parseProduct(data):
    dictVar = _getVariables(data)
    return _dict_product(dictVar)
def _parseZip(data):
    dictVar = _getVariables(data)
    for curDic in __dict_zip_longest(dictVar):
        yield { k:v for k, v in curDic.items() if v }
def _parseEntries(data):
    knownkeys = {'product':_parseProduct, 'zip':_parseZip}
    entries = []
    for key in data:
        if key == "__line__": continue
        if not key.lower() in knownkeys.keys():
            raise GeneratorException(f"Only one of the following keys are allowed: {[*knownkeys.keys()]} at line {data['__line__']}")
        entries.extend(knownkeys[key](data[key]))
    return entries
def _parseSteps(data, line):
    steps = list()
    knownkeys = {'serial':generateSerialBlock, 
                 'parallel':generateParallelBlock, 
                 'run':generateRunBlock,
                 'diff':generateDiffBlock,
                 'makedirs':generateMakedirs,
                 'rmdir':generateRmdir}
    for yamlSteps in data:
        for key in yamlSteps:
            if key == "__line__": continue
            if not key.lower() in knownkeys.keys():
                if (isinstance(data, dict)):
                    raise GeneratorException(f"Error: Key '{key}' not allowed. Only one of the following keys are allowed :{[*knownkeys.keys()]} at line {data['__line__']}")
                else:
                    raise GeneratorException(f"Error: Key '{key}' not allowed. Only one of the following keys are allowed :{[*knownkeys.keys()]} at line {line}")
            steps.append(knownkeys[key.lower()](yamlSteps[key]))
    return steps
def generateSerialBlock(data):
    args = {}
    knownkeys = {'entries': lambda data: list(_parseEntries(data)),
                 'failfast': lambda _data: getYamlBool(_data, data['__line__'], key),
                 'steps': lambda _data: list(_parseSteps(_data, data['__line__']))}
    for key in data:
        if key == "__line__": continue
        if not key.lower() in knownkeys.keys():
            raise GeneratorException(f"Only one of the following keys are allowed: {[*knownkeys.keys()]} at line {data['__line__']}")
        args[key.lower()] = knownkeys[key.lower()](data[key])
    return Serial(**args)

def generateParallelBlock(data):
    args = {}
    key = ""
    knownkeys = {'entries': lambda data: list(_parseEntries(data)), 
                 'steps': lambda _data: list(_parseSteps(_data, data['__line__'])),
                 'failfast': lambda _data: getYamlBool(_data, data['__line__'], key),
                 'max_workers': lambda _data: getYamlInt(_data, data['__line__'], key)}
    for key in data:
        if key == "__line__": continue
        if not key.lower() in knownkeys.keys():
            raise GeneratorException(f"Only one of the following keys are allowed: {[*knownkeys.keys()]} at line {data['__line__']}")
        args[key.lower()] = knownkeys[key.lower()](data[key])
    return Parallel(**args)