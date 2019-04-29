import socket 
import sys 
import threading
import queue 
from os.path import expanduser
import pickle
import os
import time
import shutil
import stitch
import upload

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

	if len(have_file) > 0:
		print(len(have_file)," Connections have this file")
		myq = recv_meta(have_file[0],filename)

		download_list = []
		start= time.time()
		for c in have_file:
			#make multiple connection and send segments hash 
			down_conn = threading.Thread(target = download_util, args = (c,myq,filename,))
			down_conn.start()
			download_list.append(down_conn)

		for x in download_list:
			x.join()

		end= time.time()
		stitch.stichk(filename)
		print("Download Successful")
		print("Time taken was ",end-start," seconds")
	else:
		print('No one has this file')

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
		print("File Found with ",addr)
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
	if os.path.isfile(filename):
		os.remove(filename)
	if os.path.isdir(filename):
		shutil.rmtree(filename)
	os.mkdir(filename)	
	meta_file = filename + '/Metafile'
	
	with open(meta_file,'wb+') as p:
	# 	while 1:
	# 		m = c.recv(919)
	# 		p.write(m)
	# 	# 	data = data + m.decode()
	# 		if len(m) < 919:
	# 	 		break
	# 	# p.write(data.encode())
	# p.close()
		chunk_len= int(c.recv(7).decode())
		recv_len=7
		while recv_len < chunk_len :
			m = c.recv(919)
			#data = data + m.decode()
			recv_len = recv_len + len(m)
			p.write(m)
		p.close()
	#print("Meta File Received!")
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

	while q.qsize() != 1:	
		seg_num = q.get()
		seg_num = seg_num.rstrip(' ')
		seg_num = seg_num.rstrip('\n')
		seg_num = seg_num.rstrip(' \n')
		hash_file = filename + "/" + seg_num
		with open(hash_file,'wb+') as p:
			st = 'Send Chunk ' + seg_num
			#print(st)
			c.send(st.encode())

			chunk_len= int(c.recv(7).decode())
			recv_len=7
			while recv_len < chunk_len :
				m = c.recv(919)
				#data = data + m.decode()
				recv_len = recv_len + len(m)
				p.write(m)
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
	query = c.recv(919).decode()
	
	while query.find("close") == -1:
		#print('Query message received : ', query)
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
					# contents=mf.read()
					# c.sendall(contents)
					# mf.close()
					contents=mf.read()
					content_len= len(contents)+7
					len_string= ""
					for i in range(0,7):
						ld= content_len%10
						len_string= str(ld)+len_string
						content_len= int(content_len/10)
					final_contents=b"".join([len_string.encode(), contents])
					#c.send(str(len(contents)).encode())
					#time.sleep(0.01)
					c.sendall(final_contents)
					mf.close()
		elif query.find('Send Chunk ') != -1:
			pos = query.find('Send Chunk ') + len('Send Chunk ')
			hashName= query[pos:]
			hashName= hashName.rstrip('\n')
			hashName= hashName.rstrip(' ')
			hashName= hashName.rstrip(' \n')
			#we will reserve first 7 letters for the size of the file
			with open(expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName,"rb") as hf:
					contents=hf.read()
					content_len= len(contents)+7
					len_string= ""
					for i in range(0,7):
						ld= content_len%10
						len_string= str(ld)+len_string
						content_len= int(content_len/10)
					final_contents=b"".join([len_string.encode(), contents])
					#c.send(str(len(contents)).encode())
					#time.sleep(0.01)
					c.sendall(final_contents)
					hf.close()
			#try:
				# with open(expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName,"rb") as hf:
				# 	contents=hf.read()
				# 	c.sendall(contents)
				# 	hf.close()
			# except:
			# 	print("Problem in opening the hashfile")
			# 	print (expanduser("~")+"/dc++_files/files/"+filename+"/"+hashName)
		query=c.recv(919).decode() 

	#print("File Shared sucessfully...closing connection")
	c.close()
	return

def main(): 
	t1 = threading.Thread(target=share) 
	t1.daemon = True
	t1.start() 

	HOST = sys.argv[1]
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

	data = s.recv(919)
	data_arr = pickle.loads(data)
	data_ip = data_arr[:][0]
	data_ip = list(set(data_ip))
	print ('Received',len(data_ip),'Connections..\n')
	s.close()

	while 1 :
		print('\n\n\n')
		ret = input("What are you here For ?\n1.Downloading a file\n2.Sharing a file\nResponce : ")       
	
		if ret == '2':
			upload.myUpload()
		elif ret == '1':
			HOST = sys.argv[1]
			PORT = 50002
			try: 
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				#print ("Socket successfully created")
			except socket.error as err:
				print ("socket creation failed with error",err) 
			try:
				s.connect((HOST, PORT))
				#print("Connected to ",HOST,PORT)
			except socket.error as err:
				print ("connection failed with error",err) 

			data = s.recv(919)
			data_arr = pickle.loads(data)
			data_ip = data_arr[:][0]
			data_ip = list(set(data_ip))
			#print ('Received',len(data_ip),'Connections..\n')
			s.close()
			download(data_arr)
		else:
			print("Enter some correct option")
			
	#write exit condtion 
	t1.join()

if __name__ == "__main__":
	main()
