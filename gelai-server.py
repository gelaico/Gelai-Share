#Programmer: Elaine George
#Date: Feb 9th, 2023
#Purpose: Hosts the server for sharing a file with gelai-client
from socket import *
import os
import random

#simple helper functions for byte management
def file_to_byte(string):
    try:
        f = open("repo/"+ string)
        file = f.read()
        f.close()
        return file
    except:
        return -1

def to_byte(inty, size, which = 0):
    if which == 0:
        return inty.to_bytes(size,'little')
    return inty.to_bytes(size,'big')

#server setup
port = 10000
port = port + random.randint(0,9999)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind( ('', port) )

#Creates the repo directory if it doesn't exist
if not os.path.isdir("repo"):
    os.makedirs("repo")
listy = os.listdir("repo")
numbFile = len(listy)

#If there are no files in the repo directory, close the server before any connections can be made
if len(listy) == 0:
    print("no files to host: ")
    serverSocket.close()
    quit()

    
#opens the server to the connection
serverSocket.listen()
print('**Server up and listening on port: ', port)

#Closes with Control C
try:
    
    #accept clients until closed
    while True:

        # wait for client to connect, then establish socket
        clientConn, clientAddr = serverSocket.accept()
        
        #list repo files
        #save number of files
        x = 0
        numbFileB = to_byte(numbFile,4)
        
        #Sends the number of files to the client
        clientConn.send(numbFileB)
        
        #send file names prefixed by their length
        while x < numbFile:
            msg = listy[x]
            intvar = len(msg.encode())
            byte = to_byte(intvar,4)
            clientConn.send(byte)
            clientConn.send(msg.encode())
            x = x + 1

        #send file names prefixed by their length
        #send if the file exists
        fileIndex = clientConn.recv(4)
        fileIndex = int.from_bytes(fileIndex,"little")
        msg = listy[fileIndex]
        file_byte = file_to_byte(msg).encode()
        
        #sends the file if it exists
        if file_byte != -1:
            length = to_byte(len(file_byte),4)
            clientConn.send(length)
            clientConn.send(file_byte)

        #write to log file what has been requested
        flog = open(".gelai_log","a")
        flog.write(str(clientAddr[0]) + " " + listy[fileIndex] +"\n")
        flog.close()
        clientConn.close()

except KeyboardInterrupt:
    serverSocket.close()
