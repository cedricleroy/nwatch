from threading import Thread
import time
import psutil


class Param(Thread):
    def __init__(self, name, fct, interval=1, ind=0):
        super(Param, self).__init__()
        self._name = name
        self._fct = fct
        self._interval = interval
        self._index = ind

    def __str__(self):
        return "%s" % (self.__class__.__name__)

    def run(self):
        while True:
            result = self._fct()[self._index] if self._index else self._fct()
            print "%s: %s" % (self._name, result)
            time.sleep(self._interval)

class ClientNode(dict):
    def __init__(self):
        super(ClientNode, self).__init__()

    def __str__(self):
        return "%s" % (self.__class__.__name__)

    def addParam(self, name, fct, interval=1, ind=0):
        p = Param(name, fct, interval, ind)
        self[name] = p
        p.start()

    def removeParam(self, name):
        p = self.get(name, None)
        if p:
            pass # TODO

if __name__ == '__main__':
    c = ClientNode()
    c.addParam("CPU", psutil.cpu_percent)
    c.addParam("Memory", psutil.virtual_memory, interval=1, ind=2)
