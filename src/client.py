import socket 
import sys 
import threading

if __name__ == "__main__":
	main()

def main():  
	ret = input("What are you here For ?\n1.For Sharing and Downloading\n2.For Uploading\n\nResponce:")       
	
	if ret == 1:
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

		t1 = threading.Thread(target=share, args=(data_arr[-1][1],)) 
		t1.daemon = True
    	t1.start()
    	 
    	download(data_arr)   

#to download whatever client wants
def download(data_arr):
	filename = input("Which File do want : ")

	have_file = []
	#query to check if they have the file and put those addr in have_file and also store the meta file 
	for addrs in data_arr
		down_conn = threading.Thread(target = downlaod_util, args = (addrs,))

	#make queue based on meta file

	for ad in have_file
		#make multiple connection and send segments hash 

		#receive segments

	stitch()

#will make connection with have_file addresses and tell 
def download_util(addrs):

#to stitch the downloaded file
def stitch():


#will listen for connections to share to them
def share(port):
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

	#join threads


#will share the required segment on socket c
def share_util(c):
	#answer the query, if do not have close socket and return

	#receive segment hash and send it 



#will upload and update client's own file list
def upload():



