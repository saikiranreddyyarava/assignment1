

import sys, socket, select

def chat_client():
    if (len(sys.argv) < 3):
    	print("ENTER: python chatclient.py hostname:port nickname")
    	sys.exit()
    arg = sys.argv[1].split(':')
    host =arg[0]
    port = int(arg[1])
    nickname = sys.argv[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)


    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. You can start sending messages'
    
    nick = 'NICK ' + nickname
    s.send(nick)
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]


        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:

                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :

                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()

            else :

                msg = sys.stdin.readline()
                msgsnd = 'MSG ' + msg
		s.send(msgsnd.encode('utf-8'))
                sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())


