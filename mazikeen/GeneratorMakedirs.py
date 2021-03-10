from mazikeen.MakedirsBlock import MakedirsBlock
from mazikeen.GeneratorException import GeneratorException

def generateMakedirs(data):
    if not isinstance(data, str):
        raise GeneratorException("'makedirs' block not recognized")
    return MakedirsBlock(data)