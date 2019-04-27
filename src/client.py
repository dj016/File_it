import socket 
import sys 
import threading
import queue 

if __name__ == "__main__":
	main()

def main(): 
	t1 = threading.Thread(target=share, args=(,)) 
	#t1.daemon = True
    t1.start() 

	ret = input("What are you here For ?\n1.Downloading\n2.Uploading\n\nResponce:")       
	
	if ret == 2:
		upload()
	else:
		HOST = 'localhost'   	  # The remote host
		PORT = 50007              # The same port as used by the server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		# t = 'Hello, world'
		# s.send(t.encode())

		# data = s.recv(1024).decode()
		# print (data)
		data = s.recv(4096)
		data_arr = pickle.loads(data)
		print ('Received',len(data_arr),'Connections..\n')
		s.close()
    	download(data_arr)

    #write exit condtion 
    t1.join()   

#to download whatever client wants
def download(data_arr):
	filename = input("Which File do want : ")

	#contains sockets of connection having the file
	have_file = []
	#query to check if they have the file and put those addr in have_file and also store the meta file 
	for addr in data_arr
		#down_conn = threading.Thread(target = downlaod_util, args = (addrs,))
		s = download_query_util(addr,filename)
		if s != -1:
			have_file.append(s)

	meta_f = recv_meta(have_file[0])
	myq = parse_meta_f(meta_f)

	#make queue based on meta file
	myq = queue.Queue()

	download_list = []

	for c in have_file
		#make multiple connection and send segments hash 
		down_conn = threading.Thread(target = download_util, args = (c,myq,filename,))
		down_conn.start()
		download_list.append(down_conn)

	for x in download_list:
		x.join()

	stitch()

def download_query_util(addr)
	HOST = addr[0]   	  # The remote host
	PORT = 50008              # The same port as used by everyone to share
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	
	#query
	s.send('Is present ',filename)

	data = s.recv(1024)
	if data = 'y':
		return s
	else:
		s.close()
		return -1

def recv_meta(c)
	c.send('Send Meta File')
	while 1:
		m = c.rev(4096)
		data = data + m
		if(m < 4096)
			break;

	return data

#parse meta file return queue of segment hashes
def parse_meta_file(meta)
	q = queue.Queue()

	return q

#with socket c,send required hash num
def download_util(c,q,f_name):
	filename = "/home/dhiraj/dc++" + f_name
	if not os.path.isdir(filename):
    	os.mkdir(filename)
    hash_file = filename + q.get()
	with open(hash_file,'w') as p:

	while q.empty == False:
		c.send('Send Chunk ',q.get())
		while 1:
			m = c.rev(4096)
			data = data + m
			if(m < 4096)
				break;

		p.write(Data)
	p.close()
	c.close()

#to stitch the downloaded file
def stitch():


#will listen for connections to share to them
def share():
	
	port = 50008
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
	if((pos = query.find('Is present')) != -1)

	elif((pos = query.find('Send Meta File')) != -1):

	elif((pos = query.find('Send Chunk ')) != -1):


	#receive segment hash and send it 



#will upload and update client's own file list
def upload():



