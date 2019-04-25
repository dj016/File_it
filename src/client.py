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
		t1 = threading.Thread(target=check_active, args=(share,)) 
    	t1.start() 
	s = socket.socket() 
	port = 12345                
	
	servaddr = sys.argv[1]
	s.connect((servaddr, port)) 

	while True:
		share()
		upload()
		download()
		print s.recv(1024) 
		 
		s.close()  



#to download whatever client wants
def download():
	filename = input("Which File do want : ")

#will listen for connections and share required segments
def share():


#will upload and update client's own file list
def upload():
