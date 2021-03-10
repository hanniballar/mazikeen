from mazikeen.RmdirBlock import RmdirBlock
from mazikeen.GeneratorException import GeneratorException
from mazikeen.ConsolePrinter import Printer, BufferedPrinter

def generateRmdir(data):
    if not isinstance(data, str):
        raise GeneratorException(f"'rmdirs' block not recognized")
    return RmdirBlock(data)