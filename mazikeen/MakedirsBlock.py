import pathlib

from mazikeen.Utils import replaceVariables, ensure_dir
from mazikeen.ConsolePrinter import Printer

class MakedirsBlock:
    def __init__(self, dir):
        self.dir = dir

    def run(self, workingDir = "", variables = {}, printer = Printer()):
        printer.verbose("Makedirs:", self.dir)
        _dir = replaceVariables(self.dir, variables, printer)
        _dir = str(pathlib.PurePath(workingDir).joinpath(_dir)) + "/" 
        ensure_dir(_dir)
        return True