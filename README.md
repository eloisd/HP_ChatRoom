# DVIC Chat

Simple chatroom project to test devops and sockets

The project is made of a client and a server.

The Server:

- Receives a connection on a socket
- Handle multiple clients
- Broadcasts messages to clients
- Handles when a client disconnects (send "`<username>` disconnected" )

The Client:

- Connects to the server
- Sends its information (username)
- Sends and receives messages from the server

The Gui:

- is cool interface for client :-)


## usage

### start the server

```bash

$ python3 -m  dvic-chat.server

```

### start the client

```bash

$ python3 -m  dvic-chat.client

```

## start gui

```bash

$ pip install dvic-chat.gui

```