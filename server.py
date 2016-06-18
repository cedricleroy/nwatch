import zmq

context = zmq.Context()

socket = context.socket(zmq.SUB)

socket.connect("tcp://localhost:5563")
socket.setsockopt(zmq.SUBSCRIBE, '')

try:
    while True:
	string = socket.recv_json()
	print string
except KeyboardInterrupt:
    print "Closed."
