import pathlib

from mazikeen.Utils import replaceVariables, ensure_dir, diffStrategy, diff
from mazikeen.ConsolePrinter import Printer, BufferedPrinter


class DiffBlock:
    def __init__(self, paths, binarycompare  = False, strategy = diffStrategy.All, ignorelines = []):
        assert len(paths) == 2
        self.paths = paths
        self.binarycompare = binarycompare
        self.strategy = strategy
        self.ignorelines = ignorelines

    def run(self, workingDir ="", variables = {}, printer = Printer()):
        printer.verbose("Diff:", self.paths)
        _leftpath = replaceVariables(self.paths[0], variables, printer)
        _rightpath = replaceVariables(self.paths[1], variables, printer)
        _ignorelines = []
        for ignoreLine in self.ignorelines:
            _ignoreline = replaceVariables(ignoreLine, variables, printer)
            _ignorelines.append(_ignoreline)
        workingDirPath = pathlib.Path(workingDir)
        return diff(workingDirPath.joinpath(_leftpath), workingDirPath.joinpath(_rightpath), self.binarycompare, self.strategy, _ignorelines, printer)
