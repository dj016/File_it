import socket 
import threading  
import sys 
import os    
import time    
import pickle     
  
def check_active(ip_list):

	while True:
		for server_ip in ip_list:
			rep = os.system('ping -c 1 ' + server_ip)

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

	port = 50007              

	try:
		s.bind(('', port))         
		print ("socket binded to",port) 
	except socket.error as err: 
	    print ("bind failed with error",err) 
 
	s.listen()      
	print ("socket is listening")            

	hub = []
	t1 = threading.Thread(target=check_active, args=(hub,)) 
	t1.daemon = True
	t1.start() 

	while True: 

		# Establish connection with client. 
		c, addr = s.accept()
		#print(c.recv(1024).decode())      
		print ('Got connection from', addr)
		#str = 'Thank you for connecting\nHere are the currently active clients\n' 
		#c.send(str.encode())
		print(type(addr))
		hub.append(addr)
		ip_string = pickle.dumps(hub)
		c.send(ip_string)

		print("Client list sent! Connection closing....")
		time.sleep(2) 
		c.close() 

	#t1.join() 
	s.close() 

if __name__ == "__main__":
	main()

