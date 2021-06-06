import shlex
import subprocess
import os
import pathlib
import sys

from mazikeen.ConsolePrinter import Printer
from mazikeen.Utils import replaceVariables, ensure_dir

class RunBlock:
    def __init__(self, cmd, outputfile = None, inputfile = None, exitcode = None, shell = None):
        self.cmd = cmd
        self.outputfile = outputfile
        self.inputfile = inputfile
        self.exitcode = exitcode
        self.shell = shell
        
    def run(self, workingDir = ".", variables = {}, printer = Printer()):

        printer.verbose("Run:", self.cmd)
        replCmd = replaceVariables(self.cmd, variables)
        printer.verbose("cwd:", os.getcwd())
        printer.verbose("call:", replCmd)
        cmdNArgs = shlex.split(replCmd)

        if self.shell == "powershell": return self.__run_powershell(replCmd, workingDir, variables, printer)
        if self.shell == "cmd": return self.__run_cmd(replCmd, workingDir, variables, printer)
        if self.shell == "sh": return self.__run_sh(replCmd, workingDir, variables, printer)
        elif self.shell != None: 
            printer.error("unknown shell ", self.shell)
            return false;

        inputfileData = None
        if self.inputfile:
            with open(pathlib.PurePath(workingDir).joinpath(replaceVariables(self.inputfile, variables)), "rb") as fh:
                inputfileData = fh.read()
        shell = (sys.platform == "win32")
        subProcessRes = subprocess.run(cmdNArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputfileData, cwd = workingDir, shell = shell)
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

    def __run_powershell(self, replCmd, workingDir = ".", variables = {}, printer = Printer()):
        if self.inputfile:
            printer.error("inputfile not allowed when shell = ", self.shell)
            return false;
        inputData = str.encode(replCmd)
        subProcessRes = subprocess.run(["powershell", "-NonInteractive", "-NoLogo"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputData, cwd = workingDir, shell = False)
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

    def __run_sh(self, replCmd, workingDir = ".", variables = {}, printer = Printer()):
        if self.inputfile:
            printer.error("inputfile not allowed when shell = ", self.shell)
            return false;
        inputData = str.encode(replCmd)
        subProcessRes = subprocess.run(["sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputData, cwd = workingDir, shell = False)
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

    def __run_cmd(self, replCmd, workingDir = ".", variables = {}, printer = Printer()):
        if self.inputfile:
            printer.error("inputfile not allowed when shell = ", self.shell)
            return false;

        if replCmd.endswith("/n"): 
            inputData = str.encode(replCmd)
        else: 
            inputData = str.encode(replCmd + "\n")
        
        subProcessRes = subprocess.run(["cmd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputData, cwd = workingDir, shell = False)
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