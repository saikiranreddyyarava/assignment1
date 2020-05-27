#!/usr/bin/python3

import sys, socket, select

def chat_client():
    NICKNAME = ""
    if(len(sys.argv) < 2) :
        print("Usage : ./chat_client.py hostname:port [nickname]")
        sys.exit()

    if len(sys.argv) > 2:
        NICKNAME = str(sys.argv[2])
        print("debug: {} {}".format(sys.argv[1], NICKNAME))

    host_addr = sys.argv[1].split(':')
    host = host_addr[0]
    port = int(host_addr[1])


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print("Unable to connect")
        sys.exit()

    # print("Connected to remote host. You can start sending messages")
    # sys.stdout.write('[Me] '); sys.stdout.flush()
    if NICKNAME != "":
        print("debug: setting nickname")
        s.sendall("NICK {}\n".format(NICKNAME).encode())

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                # print("\ndebug: incoming msg from remote server {}".format(data))
                if not data :
                    print("\nDisconnected from chat server")
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data.decode())
                    sys.stdout.write('[Me] '); sys.stdout.flush()

            else :
                # user entered a message
                msg = sys.stdin.readline()
                # print("debug: {}".format(msg))
                s.send(msg.encode())
                sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())
