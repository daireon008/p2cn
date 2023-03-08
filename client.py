import socket


def client_program():
    host = socket.gethostname()  # Using the host name as both are running on same pc
    port = 5000  # Server port number that will be assigned to the socket

    client_socket = socket.socket()  # Instantiate
    client_socket.connect((host, port))  # Connect to the server

    message = input(" -> ")  # Take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # Send message
        data = client_socket.recv(1024).decode()  # Receive response

        print('Received from server: ' + data)  # Show in terminal

        message = input(" -> ")  # Again take input

    client_socket.close()  # Close the connection


if __name__ == '__main__':
    client_program()
