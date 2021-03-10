import unittest
import os
import io
import sys
from ConsolePrinter import Printer, BufferedPrinter

class ConsolePrinterTest(unittest.TestCase):
    def test_basic(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = Printer()
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("Hello World\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = Printer(verbose=True)
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("Hello World\nHow do you do?\n", capturedOutput.getvalue())
        
        sys.stdout = sys.__stdout__

    def test_basicBufferedPrinter(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = BufferedPrinter()
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("", capturedOutput.getvalue())
        
        printer.flush()
        self.assertEqual("Hello World\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = BufferedPrinter(verbose=True)
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("", capturedOutput.getvalue())
        
        printer.flush()
        self.assertEqual("Hello World\nHow do you do?\n", capturedOutput.getvalue())
        
        sys.stdout = sys.__stdout__
        
    def test_getBufferedPrinter(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = Printer(verbose = True)
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("Hello World\nHow do you do?\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = printer.getBufferedPrinter()
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("", capturedOutput.getvalue())
        
        printer.flush()
        self.assertEqual("Hello World\nHow do you do?\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = printer.getBufferedPrinter()
        printer.print("Hello World")
        printer.verbose("How do you do?")
        
        self.assertEqual("", capturedOutput.getvalue())
        
        printer.flush()
        self.assertEqual("Hello World\nHow do you do?\n", capturedOutput.getvalue())
        
        sys.stdout = sys.__stdout__

    def test_printSeparator(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = Printer(verbose = True)
        printer.print("Hello", "World", sep = ",")
        printer.verbose("How", "do", "you", "do?", sep = ",")
        
        self.assertEqual("Hello,World\nHow,do,you,do?\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = printer.getBufferedPrinter()
        printer.print("Hello", "World", sep = ",")
        printer.verbose("How", "do", "you", "do?", sep = ",")
        printer.flush()
        self.assertEqual("Hello,World\nHow,do,you,do?\n", capturedOutput.getvalue())
        sys.stdout = sys.__stdout__
        
    def test_basicError(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = Printer()
        printer.error("Test error")
        
        self.assertEqual("Error: Test error\n", capturedOutput.getvalue())
        
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        
        printer = BufferedPrinter()
        printer.error("Test error")
        
        self.assertEqual("", capturedOutput.getvalue())
        printer.flush()
        
        self.assertEqual("Error: Test error\n", capturedOutput.getvalue())
        sys.stdout = sys.__stdout__
        
if __name__ == '__main__':
    unittest.main()

