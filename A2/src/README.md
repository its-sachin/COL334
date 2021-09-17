# COL334: Assignment2


* ### __How to run :__

    1. Run [__server.py__](./server.py) in the terminal using command ``` python server.py ``` to start the server.

    2. You can specify the maximum number of clients that can be connected to server using comman line argument ``` python server.py max_connection``` but that is optional, default maximum 10 connections can be made.

    3. Once the server is started it will wait for clients to join.

    5. To start an instance of client run [__client.py__](./client.py) in different terminals using command ``` python client.py ```.

    2. Client program will first ask for the username of client with which you want to join the chat. 

    3. Specify an alpha numeric name to start the connection with server, if INVALID username is provided then server will throw error 100.
    
    3. Once the connection is established, Server will aknowledge by sending __REGISTERED TOSEND/TORECV username__ respectively for sender and reciever side of client.
    
    4. Now the client can send messages with format ```@to message``` where __to__ is the recipient and __message__ is actual message. And simultaneously will recieve message if someone in the chat sends to it od broadcasts.

    5. To leave the chat simply exit the program by CTRL+C in windows, server will automatically delete you entries.
    
* ### __How to test error cases :__

    1. __ERROR 100 Malformed username:__ Simply provide an invalid username.

    2. __ERROR 101 No User Registered:__ Change the format of registration message on the line 30 and 31 in [__client.py__](./client.py).

    3. __ERROR 102 Unable to send:__ Send message to an username that doesn't exists.

    4. __ERROR 103 Header Incomplete:__ For sender->server message transfer change header format in line 128 of [__client.py__](./client.py), and for server->reiever message transfer change header format in line 142 (for broadcast) and 165 (unicast) of [__server.py__](./server.py).

    5. __ERROR 104 Username Taken:__ This is a new error that I've chosen to throw when client tries to request for an username that is already taken, in this case simply provide the username that is part of the chat while registration.