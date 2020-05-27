# assignment1
## Chat Client and Server
Implemented a Command line Chat system, based on TCP

### Chat Server
Implemented a chat server that is compatible with chat client and it can handle multiple users simultaneously.
To run the Chat System we need to run the chat server first then we need to run the clients
First we have to run the chat server, To run the the server we have to use the following command:
```
./chatserver hostname:port
```
hostname:port is the address to start the server.
On establishing the connection successfully you can see that the chatserver is started on the hostname and port.

### Chat Client
we have to start the client only after starting the server, To start the client we have to use the following command:
```
./chatclient hostname:port [nickname]
``` 

The [nickname] is the user name of client, The command line [nickname] is optional. you can either set [nickname] on commandline or after establishing connection with server. To set the nick name after entering the chat use the following command: ```NICK [nickname]``` where Nickname is limited to 12 characters (A-Za-z0-9\_), setting nickname is mandatory to communicate with the other clients.
To establish client connection we have to use the same (hostname:port) address used for server connection. On establishing the connection successfully you will recieve a welcome message from the server.
On adding multiple clients with the above command you can start communicating with the other clients.

We can add multiple clients on single server.






