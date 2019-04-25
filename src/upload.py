import hashlib
import sys
import os
import shutil
hashlist=[]
dirName=''
if not os.path.isdir("/home/dhiraj/dc++"):
    os.mkdir('/home/dhiraj/dc++')
with open(sys.argv[1], "rb") as f:
    dirName= '/home/dhiraj/dc++/'+sys.argv[1]
    if os.path.isdir(dirName):
        shutil.rmtree(dirName)
    os.mkdir(dirName)
    byte = f.read(1)
    size=1048576
    i=0
    cnt=0
    name='dfns'
    while byte:
        if i==0:
            #create a new file temp
            name= dirName+'/temp'+str(cnt)
            t= open(name,'w+b')
        t.write(byte)
        i+=1
        if i==size:
            t.close()
            BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
            sha1 = hashlib.sha1()
            print(name)
            with open(name, 'rb') as n:
                while True:
                    data = n.read(BUF_SIZE)
                    if not data:
                        break
                    sha1.update(data)
                n.close()
                newName= dirName+'/'+ format(sha1.hexdigest())
                print("SHA1: {0}".format(sha1.hexdigest()))
                hashlist.append(format(sha1.hexdigest()))
                os.rename(name,newName)
            cnt+=1
            i=0
            if not byte:
                break
        byte = f.read(1)
        if not byte:
            t.close()
            BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
            sha1 = hashlib.sha1()
            print(name)
            with open(name, 'rb') as n:
                while True:
                    data = n.read(BUF_SIZE)
                    if not data:
                        break
                    sha1.update(data)
                n.close()
                newName= dirName+'/'+ format(sha1.hexdigest())
                print("SHA1: {0}".format(sha1.hexdigest()))
                hashlist.append(format(sha1.hexdigest()))
                os.rename(name,newName)
            cnt+=1
            i=0
metaName= dirName+'/Metafile'
with open(metaName,'w') as p:
	p.write(sys.argv[1])
	for i in hashlist:
		p.write('\n')
		p.write(i)
p.close()

            
