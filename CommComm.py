#!/usr/bin/env python
import socket, sys, readline, time, thread
from register import register
from discover import discover
from tcp_server_b import server
"""
DJ Bonner

This project was based off some interest for a easy communication program across a network.
Started from github tcp_server : https://github.com/donaldbonner/tcp_connect_python

This new project will take advantage of using bonjour

"""	
global username
global connections
connections = []

# Check if network connection established
# Dependencies: import socket, sys
def isOnline():
    try:
        socket.gethostbyname(socket.gethostname())
    except socket.error as msg:
        print "Not connected to the network"
        sys.exit(1)
    if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        print "Not connected to the network"
        sys.exit(1)

def connectQ():
	while True:
		(host, name) = discover('_commcomm._tcp', 1)
		name = name.replace('._commcomm._tcp.local.', '')
		name = name.encode('ascii', 'ignore') # turn unicode to ascii
		host = host.encode('ascii', 'ignore') # turn unicode to ascii
		host = host[:-1]
		if (host, name) not in connections and name != username:
			connections.append((host, name))
			print 'Connection incoming from', name
			print connections
			time.sleep(1)
		time.sleep(2)

def recieveQ():
	sys.exit(0)	

def main():
	print 'Enter a username'
	global username
	username = sys.stdin.readline().strip()
	thread.start_new_thread(register, (username, '_commcomm._tcp', 9999, ))
	connectQ()

	while True:
		print 'Thread Started'
		time.sleep(2)

if __name__ == '__main__':
	isOnline()
	main()
    