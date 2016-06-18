from threading import Thread
import time
import psutil
import Queue
import zmq
import json


class Param(Thread):
    def __init__(self, name, fct, interval=1, ind=0):
        super(Param, self).__init__()
        self._name = name
        self._fct = fct
        self._interval = interval
        self._index = ind
	self._q = Queue.Queue()
	self._run = True

    def __str__(self):
        return "%s" % (self.__class__.__name__)

    def run(self):
        while self._run:
            result = self._fct()[self._index] if self._index else self._fct()
            # print "%s: %s" % (self._name, result)
	    self._q.put((self._name, result))
            time.sleep(self._interval)

class ClientNode(dict):
    def __init__(self, port=5563):
        super(ClientNode, self).__init__()
	self._context = zmq.Context()
	self._socket = self._context.socket(zmq.PUB)
	self._socket.bind("tcp://127.0.0.1:%d" % port)

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

    def _allParamToJSON(self):
	d = {}
	for k in self:
	    if not self[k]._q.empty():
	    	d[k] = self[k]._q.get()
	if not d:
	    return None
	return json.dumps(d)

    def start(self):
	try:
	    while True:
		jstring = self._allParamToJSON()
		if jstring:
		     self._socket.send_json(jstring)
		     print "sending: ", jstring
	    	time.sleep(0.01)	
	except KeyboardInterrupt:
	    self._context.destroy() # maybe something more ... soft
	    print "Context Destroyed"
	    for k in self:
		self[k]._run = False
	    print "All threads stopped"

if __name__ == '__main__':
    c = ClientNode()
    c.addParam("CPU", psutil.cpu_percent, interval=1)
    c.addParam("Memory", psutil.virtual_memory, interval=0.1, ind=2)
    c.start()

