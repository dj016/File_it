import socket 
import sys 
import threading
import queue 
from os.path import expanduser
import pickle
import os

#to download whatever client wants
def download(data_arr):
	filename = input("Which File do want : ")

	#contains sockets of connection having the file
	have_file = []
	#query to check if they have the file and put those addr in have_file and also store the meta file 
	for addr in data_arr:
		#down_conn = threading.Thread(target = downlaod_util, args = (addrs,))
		s = download_query_util(addr,filename)
		if s != -1:
			have_file.append(s)

	myq = recv_meta(have_file[0],filename)

	download_list = []

	for c in have_file:
		#make multiple connection and send segments hash 
		down_conn = threading.Thread(target = download_util, args = (c,myq,filename,))
		down_conn.start()
		download_list.append(down_conn)

	for x in download_list:
		x.join()

	import stitch
	stitch.stichk(filename)

def download_query_util(addr,filename):
	HOST = addr[0]   	  # The remote host
	PORT = 50003              # The same port as used by everyone to share
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Trying to connect ",HOST,PORT)
	s.connect((HOST, PORT))
	
	#query
	qry = 'Is present '+ filename
	s.send(qry.encode())

	data = s.recv(1024).decode()
	if data == 'y':
		return s
	else:
		s.send('close'.encode())
		s.close()
		return -1

def recv_meta(c,f_name):
	st = 'Send Meta File' + f_name
	c.send(st.encode())
	filename = expanduser("~")+"/dc++_downloads"
	if not os.path.isdir(filename):
		os.mkdir(filename)
	filename = expanduser("~")+"/dc++_downloads/" + f_name 
	if not os.path.isdir(filename):
		os.mkdir(filename)
	meta_file = filename + '/Metafile'
	
	with open(meta_file,'wb+') as p:
		while 1:
			m = c.recv(4095)
			p.write(m)
		# 	data = data + m.decode()
			if len(m) < 4095:
		 		break
		# p.write(data.encode())
	p.close()
	print("Meta File Received!")
	q = queue.Queue()
	with open(meta_file,"r") as p:
		line=p.readline()
		while line:
			line=p.readline()
			line=line.rstrip("/n")
			q.put(line)
	return q


#with socket c,send required hash num
def download_util(c,q,f_name):
	filename = expanduser("~")+"/dc++_downloads"
	if not os.path.isdir(filename):
		os.mkdir(filename)
	filename = expanduser("~")+"/dc++_downloads/" + f_name 
	if not os.path.isdir(filename):
		os.mkdir(filename)

	while q.empty() == False:	
		seg_num = q.get()
		seg_num = seg_num.rstrip(' ')
		seg_num = seg_num.rstrip('\n')
		seg_num = seg_num.rstrip(' \n')
		hash_file = filename + "/" + seg_num
		with open(hash_file,'wb+') as p:
			st = 'Send Chunk ' + seg_num
			c.send(st.encode())
			while 1:
				m = c.recv(4095)
				#data = data + m.decode()
				p.write(m)
				if len(m) < 4095:
					break;
			#p.write(data.encode())
			print("Downloaded", hash_file)
			p.close()

	c.send('close'.encode())
	c.close()



#will listen for connections to share to them
def share():
	port = 50003
	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		print ("Sharing Socket successfully created")
	except socket.error as err: 
		print ("sharing socket creation failed with error",err)               

	try:
		s.bind(('', port))         
		print ("sharing socket binded to",port) 
	except socket.error as err: 
		print ("sharing socket bind failed with error",err) 
 
	s.listen()      
	print ("Waiting to share .... ")

	while 1:
		c, addr = s.accept() 
		print ('Share : Got connection from.. ', addr)

		share_conn = threading.Thread(target = share_util, args = (c,))
		share_conn.start()

	#join threads


#will share the required segment on socket c
def share_util(c):
	#answer the query, if do not have close socket and return
	query = c.recv(4095).decode()
	print('Query message received : ', query)
	while query.find("close")==-1:
		if query.find('Is present') != -1:
			print("File Found!")
			pos = query.find('Is present') + len('Is present ')
			filename = query[pos:]
			if os.path.isdir(expanduser("~")+"/dc++_files"):
				with open(expanduser("~")+'/dc++_files/file_list.txt',"r") as fileList:
					flag=1
					line= fileList.readline()
					while line:
						line=line.rstrip("\n")
						if line == filename:
							flag=0
							c.send('y'.encode())
							break
						line=fileList.readline()
					if flag ==1:
						c.send('n'.encode()) 
			else:
				c.send('n'.encode()) 
		elif query.find('Send Meta File') != -1: ## i have assumed that file name is present in the query
			pos = query.find('Send Meta File') + len('Send Meta File')
			filename= query[pos:]
			if os.path.isdir(expanduser("~")+"/dc++_files/files/"+filename):
				with open(expanduser("~")+"/dc++_files/files/"+filename+"/Metafile","rb") as mf:
					contents=mf.read()
					c.sendall(contents)
					mf.close()
		elif query.find('Send Chunk ') != -1:
			pos = query.find('Send Chunk ') + len('Send Chunk ')
			hashName= query[pos:]
			hashName= hashName.rstrip('\n')
			try:
				with open(expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName,"rb") as hf:
					contents=hf.read()
					c.sendall(contents)
					hf.close()
			except:
				print("Problem in opening the hashfile")
				print (expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName)
		query=c.recv(4095).decode()

	#receive segment hash and send it 



def main(): 
	t1 = threading.Thread(target=share) 
	t1.daemon = True
	t1.start() 

	HOST = '192.168.103.247'
	PORT = 50002
	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		print ("Socket successfully created")
	except socket.error as err:
		print ("socket creation failed with error",err) 
	try:
		s.connect((HOST, PORT))
		print("Connected to ",HOST,PORT)
	except socket.error as err:
		print ("connection failed with error",err) 

	data = s.recv(4095)
	data_arr = pickle.loads(data)
	print ('Received',len(data_arr),'Connections..\n')
	s.close()

	while 1 :
		ret = input("What are you here For ?\n1.Downloading\n2.Uploading\n\nResponce : ")       
	
		if ret == '2':
			import upload
		else:
			download(data_arr)
			print("Main : Download Successful")
	#write exit condtion 
	t1.join()

if __name__ == "__main__":
	main()
