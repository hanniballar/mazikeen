from mazikeen.GeneratorUtils import getYamlString, getYamlInt, getYamlIntOrNone
from mazikeen.RunBlock import RunBlock
from mazikeen.GeneratorException import GeneratorException

def generateRunBlock(data):
    if isinstance(data, str):
        return RunBlock(cmd = data)
    if not isinstance(data, dict):
        raise GeneratorException(f"'run' block not recognized")
    args = {}
    key = ""
    knownkeys = {'cmd': lambda _data: getYamlString(_data, data['__line__'], key), 
                 'outputfile': lambda _data: getYamlString(_data, data['__line__'], key),
                 'inputfile': lambda _data: getYamlString(_data, data['__line__'], key),
                 'exitcode': lambda _data: getYamlIntOrNone(_data, data['__line__'], key)}
    for key in data:
        if key == "__line__": continue
        if not key.lower() in knownkeys.keys():
            raise GeneratorException(f"Only one of the following keys are allowed: {[*knownkeys.keys()]} at line {data['__line__']}")
        args[key.lower()] = knownkeys[key.lower()](data[key])
    return RunBlock(**args)