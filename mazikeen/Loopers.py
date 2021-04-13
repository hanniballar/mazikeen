from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import threading

import mazikeen.SignalHandler as SignalHandler
from mazikeen.ConsolePrinter import Printer, BufferedPrinter

class Looper:
    def __init__(self, steps = [], entries = [], failfast = True):
        self.entries = entries
        self.steps = steps
        self.failfast = failfast

class Serial(Looper):
    def __init__(self, steps = [], entries = [], failfast = True):
        super().__init__(steps, entries, failfast)
        
    def _runEntry(self, workingDir, variables, printer):
        res = True
        for executor in self.steps:
            executorRes = executor.run(workingDir = workingDir, variables = variables, printer = printer)
            if (SignalHandler.failFast()): 
                printer.error(SignalHandler.signalName() + " received.")
                return False
            if (executorRes == False):
                if (self.failfast): return False
                else: res = False
        return res
    
    def run(self, workingDir = "", variables = {}, printer = Printer()):
        res = True
        if self.entries:
            for loopEntry in self.entries:
                if (SignalHandler.failFast()): 
                    printer.error(SignalHandler.signalName() + " received.")
                    return False
                callVariables = variables.copy()
                callVariables.update(loopEntry)
                if (not self._runEntry(workingDir, callVariables, printer)): 
                    if (self.failfast): return False
                    else: res = False
        else:
            return self._runEntry(workingDir, variables, printer)
        return res

class Parallel(Looper):
    def __init__(self, steps = [], entries = [], failfast = True, max_workers = multiprocessing.cpu_count()):
        super().__init__(steps, entries, failfast)
        self.max_workers = max_workers
        self.listFutures = []
        self.addFutureLock = threading.Lock()
        self.foundFailure = False
    
    def _runStep(self, step, workingDir, variables, printer):
        overridePrinter = (not isinstance(printer, BufferedPrinter)) and (self.max_workers > 1)
        if overridePrinter:
            printer = printer.getBufferedPrinter()
        res = step.run(workingDir = workingDir, variables = variables, printer = printer)
        if (SignalHandler.failFast()): 
            printer.error(SignalHandler.signalName() + " received.")
            res = False
        if overridePrinter: 
            printer.flush() #step printer was created so that messages are not mixed up
        if res == False and self.foundFailure == False:
            with self.addFutureLock:
                self.foundFailure = True
                if (self.failfast):
                    for future in self.listFutures: future.cancel()
        return res

    def _runEntry(self, poolExecutor, workingDir, variables, printer):
        for step in self.steps:
            with self.addFutureLock:
                if ((self.foundFailure and self.failfast) or SignalHandler.failFast()): return
                self.listFutures.append(poolExecutor.submit(self._runStep, step, workingDir = workingDir, variables = variables, printer = printer))
    
    def run(self, workingDir = "", variables = {}, printer = Printer()):
        self.listFutures = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as poolExecutor:
            if self.entries:
                for loopEntry in self.entries:
                    callVariables = variables.copy()
                    callVariables.update(loopEntry)
                    self._runEntry(poolExecutor, workingDir = workingDir, variables = callVariables, printer = printer)
            else:
                self._runEntry(poolExecutor, workingDir = workingDir, variables = variables, printer = printer)
            poolExecutor.shutdown(wait=True)
        for future in self.listFutures:
            if future.cancelled() or future.result() == False: return False
        return True