import socket
from string import rstrip
from threading import Thread
import re
import time
from uidTableModule import getTable, uidTable, uid

VALIDATE_REGEX = "^validate \d{3}$"
PAIR_REGEX = "^pair \d{3}$"
KNOCK_REGEX = "^knock \d{3}$"
UID_REGEX = "\d{3}"

port = 1335

pairUid = 127

# Get UID for the doorbell
def pair(c):
    table = getTable()
    pairUid = table.requestUid()
    if pairUid:
        c.send("Stat: Y" + chr(pairUid))
        print("Doorbell paired with UID " + str(pairUid))
    else:
        c.send("Stat: N")
        print("Out of UIDs")

# Doorbell knock received    
def knock(uid, c):
    table = getTable()
    
    if (table.validate(uid)):
        print "Knocking"
        table.sendEmail(uid, "Knock Knock")
        c.send("Stat: Y")
    else:
        c.send("Stat: N")
   

def handleInput(comm, ip, c):
    try:
        table = getTable()
        
        # Get UID from command
        uid = int(re.search(UID_REGEX, comm).group(0))

        # Validate command
        if(re.match(VALIDATE_REGEX, comm)):        
            print "Validating UID", uid
            if(table.validate(uid)):
                c.send("Stat: Y")
            else:
                c.send("Stat: N")

        # Pair command        
        elif(re.match(PAIR_REGEX, comm)):
            print ("Pair initiated")
            if(uid != 255):
                table.release(uid)
            pair(c)

        # Knock command
        elif(re.match(KNOCK_REGEX, comm)):
            knock(uid, c)

        # Invalid commands
        else:
            print "Ill formed command"
    except AttributeError:
        print("Transmission error")
        c.send("Stat: E")

# Thrad that handles individual connections
class ClientThread(Thread):

    def __init__(self, c, ip):
        Thread.__init__(self)
        self.ip = ip
        self.c = c
        print("New thread started for " + str(ip))

    def run(self):
        self.c.settimeout(5.0)
        try:
            (self.c.recv(1024)) # RX initial empty payload on connect
            self.c.send("Proceed\n")
            cmd = self.c.recv(1024)
            print repr(cmd)
            handleInput(cmd, self.ip, self.c)
        except socket.timeout:
            print 'Receive timed out'
        self.c.close()
        print "Connection closed"  

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostbyname(socket.gethostname() + ".local")

s.bind((host,port))
print 'Socket bound'

while True:

    s.listen(5)

    c, addr = s.accept()
    ip = addr[0]
    newthread = ClientThread(c, ip)
    newthread.start()   

    
s.shutdown(socket.SHUT_RDWR)
s.close()
print "Socket closed"
