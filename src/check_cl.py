import socket, pickle

import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# t = 'Hello, world'
# s.send(t.encode())

# data = s.recv(1024).decode()
# print (data)


data = s.recv(1024)
#print(data)
data_arr = pickle.loads(data)
#print ('Received',type(data_arr[2]))
# arr = (1,2,3,4,6)
# data_string = pickle.dumps(arr)
# s.send(data_string)

# data = s.recv(4096)
# data_arr = pickle.loads(data)
print ('Received',len(data_arr))
s.close()