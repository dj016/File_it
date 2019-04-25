import socket 
import threading  
import sys 
import os    
import time         
  
def check_active(ip_list):

	while True:
		for server_ip in ip_list:
			rep = os.system('ping ' + server_ip)

			if rep != 0:
				print (server_ip," is down")
				ip_list.remove(server_ip)
		time.sleep(60)	

def main():
	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		print ("Socket successfully created")
	except socket.error as err: 
	    print ("socket creation failed with error",err) 

	port = 12375                

	try:
		s.bind(('', port))         
		print ("socket binded to",port) 
	except socket.error as err: 
	    print ("bind failed with error",err) 
 
	s.listen()      
	print ("socket is listening")            

	hub = ()
	t1 = threading.Thread(target=check_active, args=(hub,)) 
	t1.daemon = True
	t1.start() 

	while True: 

		# Establish connection with client. 
		c, addr = s.accept()      
		print ('Got connection from', addr) 
		c.send('Thank you for connecting')

		c.send('Here are the currently active clients')
		c.send(hub)
		hub.append(addr) 
		c.close() 

	t1.join() 
	s.close() 

if __name__ == "__main__":
	main()

