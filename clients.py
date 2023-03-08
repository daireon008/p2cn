import os
import pickle
import socket
import threading


def inet_addr():
	# To get the ip address of the client
	os.system("ifconfig ens33 | grep inet > ip.txt")     # Using ifconfig to get the ip address of the client - using system call (e) - this should change for different pcs/os     
	f=open("ip.txt",'r')				     # storing the output of the ifcofig command and using it to find the ip address
	my_host=f.read().lstrip().split(' ')[1]              # the first entry 'inet' corresponds to the ip address of the client   
	f.close()
	os.system("rm ip.txt")
	return my_host

def list_files():
	# List all the files that are stored in the shared folder (centralized directory server - having the list of files available in the network)
	os.system("ls shared > list_files.txt")
	f=open("list_files.txt",'r')
	l=f.read()
	f.close()
	os.system("rm list_files.txt")
	return l


def client_thread():
	# The client thread is resposible for receiving the files
	print("Enter the IP Address of Server for the File Request")
	host = str(input()) #taking the ip address of the server/peer acting as a server as input
	port = 1234 #assigning a port to it
	client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	# Establishing the connection with the connection socket
	client_socket.connect((host,port))
	print(client_socket.recv(1024).decode())
	# inputing the file name that the client peer wants to receive
	file_name = str(input())
	# asking the peers that have the required files
	client_socket.sendall(file_name.encode())
	file_received=client_socket.recv(8056).decode()
	f=open(file_name, 'wb')
	f.write(file_received)
	os.system("notify-send 'File Received!'")
	f.close()
	client_socket.close()


def server_thread():
	# the server thread responsible for sharing files
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
	host= inet_addr() # getting the ip address of the client acting as the server
	port=1234 #assigning a port to it
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((host,port))
	print("Waiting for connection..."+str(host))
	server_socket.listen(5)
	while True:
		# Establishing the connection between client (asking side) with the server (receiving side)
		conn,addr=server_socket.accept()
		print("Connected to"+str(addr))
		conn.sendall(b"File Name") # ask for the file the peer is requesting
		file_name=conn.recv(1024).decode()
		try:
			f=open(file_name,'rb')
			l=f.read()
			conn.sendall(l)
		except:
			conn.sendall(b"File not found")
		print('Disconnected with client')

def main(network_ip):
	# Connect to the network
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host= network_ip
	port= 9999
	s.connect((host,port))   # Connect to socket (IP address+Port number)
	
	# Getting the details of server
	data = s.recv(1024).decode()
	print(data)
	
	# Send files in your shared folder to the index server
	files=list_files()
	s.sendall(files.encode())
	print(files)
	os.system("notify-send 'File Sent!'") # Push notification 
	
	# List of files in the network
	peer_files = s.recv(1024)
	peer_files = pickle.loads(peer_files) # de-pickling (de-serializing the byte stream sent) the files using the information sent by the tcp_server
	s.close()
	print(peer_files)
	
	# Starting the client and server thread
	print("Do you want to receive some files (y/n)")
	decision=str(input())
	if(decision=='y'):
	    #client_thread()
		threading.Thread(target=client_thread, args=()).start()
	#server_thread()
	threading.Thread(target=server_thread, args=()).start()

print("Enter the IP Address of Network")
network_ip=str(input())
main(network_ip)
