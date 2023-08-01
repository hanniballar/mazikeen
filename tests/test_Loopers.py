import unittest
import time
from concurrent.futures import ThreadPoolExecutor
from mazikeen.ConsolePrinter import Printer, BufferedPrinter
from mazikeen.Loopers import Serial, Parallel

class SerialTest(unittest.TestCase):
    def test_basic(self):
        class MockExecuter:
            def run(self, workingDir, variables = {}, printer = Printer()):
                self.executed = True
                self.workingDir = workingDir
                self.printer = printer
                return True
        
        mockExecuter = MockExecuter()
        loop = Serial([mockExecuter])
        self.assertTrue(loop.run(workingDir = ".", printer = "Dummy Printer"))
        self.assertTrue(hasattr(mockExecuter, 'executed'))
        self.assertTrue(mockExecuter.workingDir == ".")
        self.assertTrue(mockExecuter.printer == "Dummy Printer")

    def test_failfast(self):
        class MockExecuter:
            def __init__(self, res):
                self.res = res

            def run(self, workingDir = ".", variables = {}, printer = Printer()):
                self.executed = True
                return self.res

        mockExecuters = [MockExecuter(True), MockExecuter(False), MockExecuter(True)]
        loop = Serial(mockExecuters, failfast = True)
        self.assertFalse(loop.run(workingDir = ".", printer = Printer()))
        self.assertTrue(hasattr(mockExecuters[0], 'executed'))
        self.assertTrue(hasattr(mockExecuters[1], 'executed'))
        self.assertFalse(hasattr(mockExecuters[2], 'executed'))

        mockExecuters = [MockExecuter(True), MockExecuter(False), MockExecuter(True)]
        loop = Serial(mockExecuters, failfast = False)
        self.assertFalse(loop.run())
        self.assertTrue(hasattr(mockExecuters[0], 'executed'))
        self.assertTrue(hasattr(mockExecuters[1], 'executed'))
        self.assertTrue(hasattr(mockExecuters[2], 'executed'))

    def test_entries(self):
        class MockExecuter:
            def __init__(self):
                self.variables = []

            def run(self, workingDir, variables, printer = Printer()):
                self.variables.append(variables)
                self.workingDir = workingDir
                self.printer = printer
                return True
        
        mockExecuter = MockExecuter()
        loop = Serial([mockExecuter], entries = [{"var1" : "val1"}, {"var2" : "val2"}])
        loop.run(workingDir = ".", printer = "Dummy printer")
        self.assertTrue(mockExecuter.variables == [{"var1" : "val1"}, {"var2" : "val2"}])
        self.assertTrue(mockExecuter.workingDir == ".")
        self.assertTrue(mockExecuter.printer == "Dummy printer")

    def test_VariablesOverwrite(self):
        class MockExecuter:
            def run(self, workingDir, variables, printer = Printer()):
                self.variables = variables
                self.workingDir = workingDir
                return True
        
        mockExecuter = MockExecuter()
        loop = Serial([mockExecuter], entries = [{"var1" : "val1", "var2" : "val2"}])
        loop.run(workingDir = ".", variables = {"var1" : "overwriteVal1", "var3": "val3"})
        self.assertTrue(mockExecuter.variables == {"var1" : "val1", "var2" : "val2",  "var3": "val3"})
        self.assertTrue(mockExecuter.workingDir == ".")

class ParallelTest(unittest.TestCase):
    def test_basic(self):
        class MockExecuter:
            def run(self, workingDir, variables = {}, printer = Printer()):
                self.executed = True
                self.workingDir = workingDir
                self.printer = printer
                return True
        
        mockExecuter = MockExecuter()
        loop = Parallel([mockExecuter], max_workers=4)
        self.assertTrue(loop.run(".", printer = Printer()))
        self.assertTrue(hasattr(mockExecuter, 'executed'))
        self.assertTrue(mockExecuter.workingDir, '.')
        self.assertTrue(isinstance(mockExecuter.printer, BufferedPrinter))

    def test_failfast(self):
        class MockExecuter:
            def __init__(self, res):
                self.res = res

            def run(self, workingDir, variables = {}, printer = Printer()):
                self.executed = True
                return self.res
        
        mockExecuters = [MockExecuter(True), MockExecuter(False), MockExecuter(True)]
        loop = Parallel(mockExecuters, failfast = True, max_workers = 1)
        self.assertFalse(loop.run("."))
        self.assertTrue(hasattr(mockExecuters[0], 'executed'))
        self.assertTrue(hasattr(mockExecuters[1], 'executed'))
        self.assertFalse(hasattr(mockExecuters[2], 'executed'))

        mockExecuters = [MockExecuter(True), MockExecuter(False), MockExecuter(True)]
        loop = Parallel(mockExecuters, failfast = False, max_workers = 1)
        self.assertFalse(loop.run("."))
        self.assertTrue(hasattr(mockExecuters[0], 'executed'))
        self.assertTrue(hasattr(mockExecuters[1], 'executed'))
        self.assertTrue(hasattr(mockExecuters[2], 'executed'))

    def test_entries(self):
        class MockExecuter:
            def __init__(self):
                self.variables = []

            def run(self, workingDir, variables, printer = Printer()):
                self.variables.append(variables)
                self.workingDir = workingDir
                self.printer = printer
                return True
        
        mockExecuter = MockExecuter()
        loop = Parallel([mockExecuter], entries = [{"var1" : "val1"}, {"var2" : "val2"}])
        self.assertTrue(loop.run(".", printer = Printer()))
        self.assertTrue(mockExecuter.variables == [{"var1" : "val1"}, {"var2" : "val2"}])
        self.assertTrue(mockExecuter.workingDir == ".")
        self.assertTrue(isinstance(mockExecuter.printer, BufferedPrinter))

    def test_VariablesOverwrite(self):
        class MockExecuter:
            def run(self, workingDir, variables, printer = Printer()):
                self.variables = variables
                self.workingDir = workingDir
                return True
        
        mockExecuter = MockExecuter()
        loop = Parallel([mockExecuter], entries = [{"var1" : "val1", "var2" : "val2"}])
        loop.run(workingDir = ".", variables = {"var1" : "overwriteVal1", "var3": "val3"})
        self.assertTrue(mockExecuter.variables == {"var1" : "val1", "var2" : "val2",  "var3": "val3"})
        self.assertTrue(mockExecuter.workingDir == ".")

if __name__ == '__main__':
    unittest.main()
