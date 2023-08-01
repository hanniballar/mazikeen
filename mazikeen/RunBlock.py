import shlex
import subprocess
import os
import pathlib
import sys
import platform
import threading

from mazikeen.ConsolePrinter import Printer
from mazikeen.Utils import replaceVariables, ensure_dir

__pythonPath = None
__pythonPath3 = None
__searchedForPython = False
__searchedForPythonLock = threading.Lock()

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
        printer.verbose("cwd:", os.path.abspath(workingDir))
        printer.verbose("call:", replCmd)
        cmdNArgs = shlex.split(replCmd)

        if self.shell == "powershell": return self.__run_powershell(replCmd, workingDir, variables, printer)
        elif self.shell == "cmd": return self.__run_cmd(replCmd, workingDir, variables, printer)
        elif self.shell == "sh": return self.__run_sh(replCmd, workingDir, variables, printer)
        elif self.shell == "python": return self.__run_pythonX(replCmd, "python", workingDir, variables, printer)
        elif self.shell == "python3": return self.__run_pythonX(replCmd, "python3", workingDir, variables, printer)
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

    def __run_pythonX(self, replCmd, pythonType = "python3", workingDir = ".", variables = {}, printer = Printer()):
        pythonPath = getPythonPath(pythonType)
        if pythonPath == None:
            printer.error(f"{pythonType} could not be found")
            return false;
        if self.inputfile:
            printer.error("inputfile not allowed when shell = ", self.shell)
            return false;
        inputData = str.encode(replCmd)
        subProcessRes = subprocess.run([pythonPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=inputData, cwd = workingDir, shell = False)
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

def getPythonPath(pythonType):
    with __searchedForPythonLock:
        if __searchedForPython == False:
            if platform.system().lower() == "windows":
                process = subprocess.run(["where", "python"], stdout=subprocess.PIPE, shell = False)
                pythonPaths = process.stdout.decode("utf-8").split("\r\n")
                pythonPaths = list(filter (("").__ne__, pythonPaths))
                for pythonPath in pythonPaths:
                    process = subprocess.run([pythonPath, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = False)
                    pythonVersion = process.stdout.decode("utf-8")
                    if pythonVersion.startswith("Python 3"):
                        __pythonPath3 = pythonPath
                    elif pythonVersion.startswith("Python 2"):
                        __pythonPath = pythonPath
            if platform.system().lower() == "linux":
                process = subprocess.run(["which", "python"], stdout=subprocess.PIPE, shell = False)
                pythonPaths = process.stdout.decode("utf-8").split("\n")
                process = subprocess.run(["which", "python3"], stdout=subprocess.PIPE, shell = False)
                pythonPaths.extend(process.stdout.decode("utf-8").split("\n"))
                pythonPaths = list(filter (("").__ne__, pythonPaths))
                for pythonPath in pythonPaths:
                    process = subprocess.run([pythonPath, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = False)
                    pythonVersion = process.stdout.decode("utf-8")
                    if pythonVersion.startswith("Python 3"):
                        __pythonPath3 = pythonPath
                    elif pythonVersion.startswith("Python 2"):
                        __pythonPath = pythonPath
        if pythonType == "python": return __pythonPath
        elif pythonType == "python3": return __pythonPath3
        return None