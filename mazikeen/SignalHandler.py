import signal

__signal_received__ = None

def failFast():
    global __signal_received__
    return __signal_received__ != None

def init(): 
    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGBREAK, signalHandler)

def signalName():
    global __signal_received__
    if __signal_received__ == None: return __signal_received__
    return str(signal.Signals(__signal_received__).name)

def signalHandler(signal_received, frame):
    global __signal_received__
    if (__signal_received__ == None):
        print(str(signal.Signals(signal_received).name) + " received fail fast enabled. Send signal again to force exit")
        __signal_received__ = signal_received
    else:
        exit(1)
    