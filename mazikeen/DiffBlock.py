import pathlib

from mazikeen.Utils import replaceVariables, ensure_dir, diffStrategy, diff
from mazikeen.ConsolePrinter import Printer, BufferedPrinter


class DiffBlock:
    def __init__(self, leftpath, rightpath, binarycompare  = False, strategy = diffStrategy.All, ignorelines = []):
        self.leftpath = leftpath
        self.rightpath = rightpath
        self.binarycompare = binarycompare
        self.strategy = strategy
        self.ignorelines = ignorelines

    def run(self, workingDir ="", variables = {}, printer = Printer()):
        _leftpath = replaceVariables(self.leftpath, variables, printer)
        _rightpath = replaceVariables(self.rightpath, variables, printer)
        _ignorelines = []
        for ignoreLine in self.ignorelines:
            _ignoreline = replaceVariables(ignoreLine, variables, printer)
            _ignorelines.append(_ignoreline)
        workingDirPath = pathlib.Path(workingDir)
        return diff(workingDirPath.joinpath(_leftpath), workingDirPath.joinpath(_rightpath), self.binarycompare, self.strategy, _ignorelines, printer)
