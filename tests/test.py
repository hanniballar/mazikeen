import shlex
import subprocess
import os
import pathlib

replCmd = "echo Hello World"
cmdNArgs = shlex.split(replCmd)
inputfileData = None
workingDir = "."

subProcessRes = subprocess.run(cmdNArgs, cwd = workingDir, shell = True)
