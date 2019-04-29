#first i will open the directory which contains all the chunks
#Then I will open the metafile and make another file with the name present in the first line
#then i will acess the hash in the order specified in the metafile and append in binary to the main file 
#then i will delete all the hash files and the metafile
import os
import sys
import shutil
from os.path import expanduser

def stichk(fileName):
    home = expanduser("~")
    arg= home+'/dc++_downloads/'+fileName
    metaPath = arg+"/Metafile"
    with open(metaPath, "r") as mf:
        line = mf.readline()
        dirName= metaPath[:-8]
        fileName= dirName+line
        fileName=fileName.rstrip(' ')
        fileName=fileName.rstrip(' \n')
        fileName=fileName.rstrip('\n')
        #print(dirName)
        with open(fileName,"wb+") as f:
            line=mf.readline()
            while line:
                hashPath= dirName+line
                hashPath= hashPath.rstrip("\n")
                #print(hashPath)
                with open(hashPath,"rb") as hf:
                    contents=hf.read()
                    f.write(contents)
                    hf.close()
                    os.remove(hashPath)
                line= mf.readline()
            f.close()
        mf.close()
        os.remove(metaPath)
        if not os.path.isdir(home+"/dc++_downloads"):
            os.mkdir(home+'/dc++_downloads')
        pos=fileName.rfind('/')
        newPath=home+"/dc++_downloads"+fileName[pos:]
        dest=expanduser("~")+"/dc++_downloads/temp"
        os.rename(newPath,dest)
        pos2=fileName.rfind('/')
        dest= dest+fileName[pos2:]
        #print(dest)
        #print(newPath)
        shutil.move(dest,newPath)
        if os.path.isdir(expanduser("~")+"/dc++_downloads/temp"):
            shutil.rmtree(expanduser("~")+"/dc++_downloads/temp")
