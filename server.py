#!/usr/bin/python

import socket,sys, re
from threading import Thread

socketObject = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

nrArg = len(sys.argv)
if (nrArg < 2 and nrArg > 3):
    print ("Wrong Input")
    print ("please ENTER: python filename hostname:port")
    sys.exit()

array = sys.argv[1].split(':')
host = array[0]
port = int(array[1])
clients = {}
clientList = []
socketObject.bind((host,port))

# Function to show the client connection
# Shows the chatstatus to clients
def clientAcceptance() :
    while True :
        ip,addr = socketObject.accept()
        print("%s:%s has connected" % addr)
        ip.send("Welcome to Kiran chat System \n")
        clientList.append(ip)
        Thread(target= handlingClients, args=(ip,addr)).start()

# Function to validate the message size
# Client connection status
def handlingClients(ip,addr) :

    length = ip.recv(1024)
    userName = length.strip("NICK ")
    if len(userName)<13 and re.match("^[A-Za-z0-9\_]+$",userName) is not None:
        ip.send("OK \n")
    else :
        ip.send(" ERROR: Nickname is not valid \n")
        name = 'unkwown'
    msg = "%s has joined the chat \n"% userName
    broadcast(msg,ip)
    clients[ip] = userName

    while True :
        m = ip.recv(1024).decode('utf-8')
        msg = m.strip("MSG ")
        if not msg:
            ip.close()
            del clients[ip]
            left = "%s has left the chat \n"% userName
            print ("%s:%s has disconnected." % addr)
            broadcast(left,ip)
            break
        else :
            if len(msg) > 255 and re.match("^[^\x00-\x7F]*$",msg) is None:
                ip.send("ERROR: Message should be less than 255 characters")
                msg_snd = "MSG "+userName +" "
            else:
                msg_snd = "MSG "+userName +" "+ msg
            broadcast(msg_snd,ip)

def broadcast(msg, clientConnection):
    for i in clientList:
        if i != socketObject and i != clientConnection :
            try:
                i.send(msg.encode('utf-8'))
            except:
                pass

while True:
    socketObject.listen(100)
    print("Waiting for clients to connect...")
    connection = Thread(target=clientAcceptance)
    connection.start()
    connection.join()
    socketObject.close()
