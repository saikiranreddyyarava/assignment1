

import sys, socket, select

HOST = ''
SOCKET_LIST = []
clients = {}
RECV_BUFFER = 4096
PORT = 9009

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)


    SOCKET_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:



        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:

            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                name = sockfd.recv(1024)
                SOCKET_LIST.append(sockfd)
                clients[sockfd] = name
                print "Client (%s, %s) connected" % addr

                broadcast(server_socket, sockfd, " %s entered our chatting room\n" % name)


            else:

                try:

                    data = sock.recv(RECV_BUFFER)
                    if data:

                        broadcast(server_socket, sock, "\r" + '[' + str(name) + '] ' + data)
                    else:

                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)


                        broadcast(server_socket, sock, "Client %s is offline\n" % name)


                except:
                    broadcast(server_socket, sock, "Client %s is offline\n" % name)
                    continue

    server_socket.close()


def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:

        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :

                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":

    sys.exit(chat_server())



