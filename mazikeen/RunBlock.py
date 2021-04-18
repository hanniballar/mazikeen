import shlex
import subprocess
import os
import pathlib

from mazikeen.ConsolePrinter import Printer
from mazikeen.Utils import replaceVariables, ensure_dir

class RunBlock:
    def __init__(self, cmd, outputfile = None, inputfile = None, exitcode = None):
        self.cmd = cmd
        self.outputfile = outputfile
        self.inputfile = inputfile
        self.exitcode = exitcode

    def run(self, workingDir = ".", variables = {}, printer = Printer()):
        printer.verbose("Run:", self.cmd)
        replCmd = replaceVariables(self.cmd, variables)
        cmdNArgs = shlex.split(replCmd)
        printer.verbose("cwd:", os.getcwd())
        printer.verbose("call:", replCmd)
        inputfileData = None
        if self.inputfile:
            with open(pathlib.PurePath(workingDir).joinpath(replaceVariables(self.inputfile, variables)), "rb") as fh:
                inputfileData = fh.read()
        subProcessRes = subprocess.run(cmdNArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputfileData, cwd = workingDir, shell = False)
        if self.outputfile:
            outputfileFullPath = str(pathlib.PurePath(workingDir).joinpath(replaceVariables(self.outputfile, variables)))
            ensure_dir(outputfileFullPath)
            with open(outputfileFullPath, "wb") as fh:
                fh.write(subProcessRes.stdout)
        
        res = True
        if (self.exitcode != None):
            res = subProcessRes.returncode == self.exitcode
            if not res:
                printer.error("different exitcode received:", subProcessRes.returncode, "!=", self.exitcode, "for command '"+ str(replCmd) +"'")
        return res
     