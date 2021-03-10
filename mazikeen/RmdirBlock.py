import pathlib

from mazikeen.Utils import replaceVariables, rmtree
from mazikeen.ConsolePrinter import Printer

class RmdirBlock:
    def __init__(self, dir):
        self.dir = dir

    def run(self, workingDir = "", variables = {}, printer = Printer()):
        _dir = replaceVariables(self.dir, variables, printer)
        return rmtree(str(pathlib.PurePath(workingDir).joinpath(_dir)), printer)