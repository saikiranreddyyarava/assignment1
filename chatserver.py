#!/usr/bin/python3

import sys, socket, select, re

HOST = ''
SOCKET_LIST = []
NICK_LIST = {}
RECV_BUFFER = 4096
PORT = 9000

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    print("Chat server started on {}:{}".format(HOST,PORT))

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client %s:%s connected" % addr)
                sockfd.sendall(b"Hello 1\n")

                broadcast(server_socket, sockfd, "\n[server] %s:%s entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER).decode()
                    # print("\ndebug: len of msg from client {}".format(len(data.strip())))
                    if data:
                        if len(data) > 255:
                            sock.send(b"\n[server] ERROR the message cannot be more than 255 characters\n")
                            continue
                        if data == "\n":
                            continue
                        cmd = data.strip("\n").split(" ")
                        # print("debug: {}".format(cmd))
                        if "NICK" in cmd and cmd[0] != "NICK":
                            sock.send(b"\n[server] ERROR malformed command\n")
                            continue
                        if "NICK" in cmd and cmd[0]=="NICK" and len(cmd)>1:
                            if len(cmd[1]) < 13 and re.match("^[A-Za-z0-9\_]+$", cmd[1]) is not None:
                                NICK_LIST[cmd[1]] = sock
                                sock.send(b"\n[server] OK\n")
                                continue
                            else:
                                sock.send(b"\n[server] ERROR nickname is limited to 12 characters and cannot have \
                                                special characters\n")
                                continue
                        if sock not in NICK_LIST.values():
                            sock.send(b"\n[server] ERROR no nick set\n")
                        else:
                            nick_keys = NICK_LIST.keys()
                            nick_values = NICK_LIST.values()
                            nick = list(NICK_LIST.keys())[list(NICK_LIST.values()).index(sock)]
                            broadcast(server_socket, sock, "\r" + '[server] ' + '[' + str(nick) + '] ' + data)

                        # there is something in the socket
                        # broadcast(server_socket, sock, "\r" + '[server] ' + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "[server] Client %s:%s is offline\n" % addr)
                        print("Client %s:%s is offline" % addr)

                # exception
                except:
                    if sock in SOCKET_LIST:
                        print("couldn't process data from client %s:%s" % addr)
                    else:
                        print("Client %s:%s is offline" % addr)
                        broadcast(server_socket, sock, "[server] Client %s:%s is offline\n" % addr)
                    continue

    server_socket.close()

# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    # print("debug: broadcasting messages......")
    # print("debug: socket_list: {}".format(SOCKET_LIST))
    for socket in SOCKET_LIST:
        # print("debug: \nsocket: {}\nserver_socket: {}\nsock: {}\nmsg: {}".format(socket,server_socket,sock,message))
        # send the message only to peer
        if socket != server_socket and socket != sock:
            # print("debug: broadcast  {}".format(message))
            try:
                socket.send(message.encode())
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
    # print("debug: broadcast complete. {} ---- {}".format(len(SOCKET_LIST),SOCKET_LIST))

if __name__ == "__main__":
    N = len(sys.argv)
    if N < 2:
        print ("USAGE: ./chatserver <IP>:<PORT>")
        sys.exit()
    host = sys.argv[1].split(':')
    HOST = host[0]
    PORT = int(host[1])
    sys.exit(chat_server())


