import io
import threading

class Printer():
    printerCnt = 0
    printLock = threading.Lock()
    errorLock = threading.Lock()
    def __init__(self, verbose = False):
        self._verbose = verbose
        self.__printerCnt = Printer.printerCnt
        Printer.printerCnt += 1
        self.errorOutput = ""

    def __repr__(self):
        return f"{self.__class__.__name__} {self.__printerCnt}"

    def __str__(self):
        return self.__repr__()

    def verbose(self, *args, **kwargs):
        if self._verbose:
            self.print(*args, **kwargs, flush = True)
    
    def getBufferedPrinter(self):
        bp = BufferedPrinter(verbose = self._verbose)
        bp.errorOutput = self.errorOutput
        return bp
    
    def print(self, *args, **kwargs):
        with Printer.printLock:
            print(*args, **kwargs)
    
    def debug(self, *args, **kwargs):
        self.print("debug: ", end ="", flush = False) 
        self.print(*args, **kwargs, flush = True)

    def error(self, *args, **kwargs):
        with Printer.errorLock:
            with io.StringIO() as _errorMsg:
                print("Error: ", file=_errorMsg, end = "", flush = False)
                print(*args, **kwargs, file=_errorMsg, flush = True)
                self.errorOutput +=_errorMsg.getvalue()
            self.print("Error: ", end = "", flush = False)
            self.print(*args, **kwargs, flush = True)
        
    def flush(self):
        return
        
    def isVerbose(self):
        return self._verbose
        
class BufferedPrinter(Printer):
    def __init__(self, verbose = False):
        super().__init__(verbose)
        self.__buffer = None
        
    def print(self, *args, **kwargs):
        output = io.StringIO()
        print(*args, file=output, **kwargs)
        outputStr = output.getvalue()
        if not self.__buffer:
            self.__buffer = outputStr
        else :
            self.__buffer += outputStr
        
    def verbose(self, *args, **kwargs):
        if self._verbose:
            self.print(*args, **kwargs, flush = True)

    def flush(self):
        if self.__buffer:
            super().print(self.__buffer, end="", flush = True)
        self.__buffer = None
        
    def getBufferedPrinter(self):
        return self
    
    def __del__(self):
        self.flush()
