from _thread import *
import os
import pickle
import socket


def index_peers(files_data,address):
	# for breaking the details of files (location and name)
	l=list()
	k=files_data.split('\n')
	m=k[:-1]
	n=k[-1]
	l.append(n)
	l.append(m)
	return l
    

all_files=list()  # stores list of peers with file details

# Setting up the centralized directory server
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host="0.0.0.0"
port=9999
s.bind((host,port))

print("Waiting for connection...  "+str(host))
s.listen(5)
flag=0
while True:
	# Look for the clients asking for connections
	conn,addr=s.accept()
	print("Connected to "+str(addr))
	
	conn.sendall(b"Centralized Directory Server wants File list")
	files_data=conn.recv(1024).decode()
	received_files=index_peers(files_data,addr[0]) # getting the information of files received by this server
	ip=received_files[0] 
	upgrade_flag=1
	if(flag):
		print(ip,all_files[0][0])
		for i,j in enumerate(all_files):
			if(str(all_files[i][0]) == str(ip)):
				print("True")
				del all_files[i]
				all_files.append(received_files) # add to the list of files
				upgrade_flag=0
				break
	if(upgrade_flag):
		all_files.append(received_files)
	flag=1
	for i in all_files:
		print(i)
	
	data=pickle.dumps(all_files) # Converting the details/names of all the files into bytes (pickling the data)
	conn.sendall(data)
	print("Data sent to peer.")
	conn.close()
s.close()
