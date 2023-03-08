# Computer Networks - Practical 2
### Daire O' Neill
### Ujjayant Kadian

# Messaging Functionality - 
1. Run messaging_server.py first by typing `python3 messaging_server.py` in the command prompt.
2. Run messaging_client.py next by typing `python3 messaging_client.py` in the command prompt.
3. Connection should now be established and the client can start the conversation.

Note: At most 2 connections can be maintained in this network.

# P2P File-Sharing Functionality using a Centralized Directory Server - 
1. First check `clients.py` and see if the `ifconfig` command is valid for your PC (if not valid the code would have to be changed).
2. Run the centralized directory server first by typing `python3 centralized_directory_server`
3. Run as many as 4 clients by typing `python3 clients.py` in different terminals.
4. Enter the ip address of the network (`0.0.0.0`) in the concerned client's terminal to establish the connection between the centralized directory server and itself.
5. After establishing connection you can either download existing files in `shared` folder or update the network by adding the file into it.
6. The clients can act as peers and will ask each other for their required files (the files that they want to receive) by following the instructions of the code. They can receive a file that is already in the network or can wait or can disconnect.
