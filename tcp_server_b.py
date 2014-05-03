#!/usr/bin/env python
import signal, os, socket, time, sys, subprocess, readline, struct, fcntl, termios, thread
from multiprocessing import Process

global toSend
toSend = "Fail"

# Get local inet_ip address
def getInetIP():
    try:
        socket.gethostbyname(socket.gethostname())
    except socket.error as msg:
        print "Not connected to the interwebs"
        sys.exit(1)
    if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        print "Not connected to the interwebs"
        sys.exit(1)
    return socket.gethostbyname(socket.gethostname())

# http://docs.python.org/2.7/library/socket.html
# returns the connection socket and the address connected to (conn, addr)
def listen_to(host, port):
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print 'could not open connection'
        return None
    conn, addr = s.accept()
    return conn

# Thread waits for incoming message to print
# Byte strings to create color output
# Black : \033[22;30m
# Red : \033[22;31m
def threadPrint(sock, clientName, pid):
    while True:
        data = sock.recv(1024)
        if not data: 
            break
        blank_current_readline()
        print "\033[22;31m" + clientName + ':' + data + "\033[22;30m"
        if readline.get_line_buffer == toSend or readline.get_line_buffer() == toSend + '\n':
            sys.stdout.write('>')
        else:
            sys.stdout.write('>' + readline.get_line_buffer())
        sys.stdout.flush()          # Needed or text doesn't show until a key is pressed
    os.kill(pid,signal.SIGINT)
    sys.exit(0)

# http://stackoverflow.com/questions/2082387/reading-input-from-raw-input-without-having-the-prompt-overwritten-by-other-th
def blank_current_readline():
    # Next line said to be reasonably portable for various Unixes
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    # ANSI escape sequences (All VT100 except ESC[0G)
    sys.stdout.write('\x1b[2K')                         # Clear current line
    sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
    sys.stdout.write('\x1b[0G')                         # Move to start of line

# Modifier for global variable
def setToSend(value):
    global toSend
    toSend = value

def server(hostname, clientName, port):
    conn = listen_to('', port)
    subprocess.call(["clear"])

    print 'Connected to', clientName
    print 'To exit chat, type', repr('.logout') 
    sys.exit(0)

    thread.start_new_thread(threadPrint, (conn, clientName, os.getpid(), ))

    while True: 
        try:
            setToSend(raw_input('>'))
            if toSend == ".logout": 
                blank_current_readline()
                print 'connection with ' + clientName + ' closed'
                break
            conn.sendall(toSend)
        except (KeyboardInterrupt, SystemExit):
            blank_current_readline()
            print 'connection with ' + clientName + ' closed'
            conn.close()
            sys.exit(1)
    conn.close()
    sys.exit(0)
