#!/usr/bin/python

import socket,sys,select,string

socketObject = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

nrArg = len(sys.argv)
if (nrArg < 3 and nrArg > 4):
    print ("Wrong Input")
    print ("please ENTER: python <FILENAME> localhost:<PORT> <USER>")
    sys.exit()

array = sys.argv[1].split(':')
host = array[0]
port = int(array[1])
user = sys.argv[2]
socketObject.settimeout(10)
socketObject.connect((host,port))
print("Connection established to server")
socketObject.send(user)
string =''

while True :
    sockList = [sys.stdin,socketObject]
    readList,writeList,errorList = select.select(sockList,[], [])
    for i in readList:
        if i == socketObject:
            rcvdMsg = i.recv(1024)
            if not rcvdMsg:
                print("DISCONNECTED")
                sys.exit()
            else:
                if rcvdMsg != 'MSG '+user+' '+string :
                    sys.stdout.write(rcvdMsg.strip('MSG '))
                    sys.stdout.flush()
                else:
                    continue
        else:
            string = ''
            msg = sys.stdin.readline()
            string += msg
            fullmsg ='MSG ' + msg
            socketObject.send(fullmsg.encode('utf-8'))
            #sys.stdout.write("You : ")
            #sys.stdout.write(msg)
            sys.stdout.flush()
socketObject.close()
            
