import socket 
import sys 
import threading
import queue 
from os.path import expanduser
import pickle

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
	stich.stichk(filename)

def download_query_util(addr,filename):
	HOST = addr[0]   	  # The remote host
	PORT = 50009              # The same port as used by everyone to share
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Trying to connect ",HOST,PORT)
	s.connect((HOST, PORT))
	
	#query
	s.send('Is present ',filename)

	data = s.recv(1024)
	if data == 'y':
		return s
	else:
		s.send('close')
		s.close()
		return -1

def recv_meta(c,f_name):
	c.send('Send Meta File',f_name)
	filename = expanduser("~")+"/dc++_downloads" + f_name 
	if not os.path.isdir(filename):
		os.mkdir(filename)
	meta_file = filename + 'Metafile'

	with open(meta_file,'wb+') as p:
		while 1:
			m = c.recv(4096)
			data = data + m
			if m < 4096:
				break;
		p.write(data)
	p.close()
	q = queue.Queue()
	with open(meta_file,"r") as p:
		line=readline()
		while line:
			line=readline()
			q.put(line)
	return q


#with socket c,send required hash num
def download_util(c,q,f_name):
	filename = expanduser("~")+"/dc++_downloads" + f_name 
	if not os.path.isdir(filename):
		os.mkdir(filename)
	hash_file = filename + q.get()

	with open(hash_file,'wb+') as p:

		while q.empty() == False:
			c.send('Send Chunk ',q.get())
			while 1:
				m = c.recv(4096)
				data = data + m
				if m < 4096:
					break;

			p.write(data)
		p.close()
	c.send('close')
	c.close()



#will listen for connections to share to them
def share():
	port = 50009
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
		print ('Got connection from.. ', addr)

		share_conn = threading.Thread(target = share_util, args = (c,))
		share_conn.start()

	#join threads


#will share the required segment on socket c
def share_util(c):
	#answer the query, if do not have close socket and return
	query = c.recv(4096)
	while query.find("close")!=-1:
		if query.find('Is present') != -1:
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
							c.send("y")
							break
						line=fileList.readline()
					if flag ==1:
						c.send("n")
			else:
				c.send("n") 
		elif query.find('Send Meta File') != -1: ## i have assumed that file name is present in the query
			pos = query.find('Send Meta File') + len('Send Meta File')
			filename= query[pos:]
			if os.path.isdir(expanduser("~")+"/dc++_files/files/"+filename):
				with open(expanduser("~")+"/dc++_files/files/"+filename+"/Metafile","rb") as mf:
					contents=mf.read()
					c.sendall(contents)

		elif query.find('Send Chunk ') != -1:
			pos = query.find('Send Chunk ') + len('Send Chunk ')
			hashName= query[pos:]
			try:
				with open(expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName,"rb") as hf:
					contents=mf.read()
					c.sendall(contents)
			except:
				print("Problem in opening the metafile")
		query=c.recv(4096)

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

	data = s.recv(4096)
	data_arr = pickle.loads(data)
	print ('Received',len(data_arr),'Connections..\n')
	s.close()

	while 1 :
		ret = input("What are you here For ?\n1.Downloading\n2.Uploading\n\nResponce : ")       
	
		if ret == '2':
			import upload
		else:
			download(data_arr)
	#write exit condtion 
	t1.join()

if __name__ == "__main__":
	main()
