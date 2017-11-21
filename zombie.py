from socket import *
import select
import _thread
import time
import io
import sys
import subprocess

class Zombie:

    def __init__(self,name,serverIP,serverPort):
        self.name = name
        self.serverIP = serverIP
        self.serverPort= int(serverPort)
        self.jobList = {}
        self.jobCounter = 0
        
    def getName(self):
        return self.name

    def connect(self):
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.serverIP,self.serverPort))

    def send(self,request):
        self.clientSocket.send(request.encode())

    def respond(self):
        buffer=""
        while True:
            r = self.clientSocket.recv(1024).decode()
            buffer = buffer + r
            if "\r\n\r\n" in buffer:

                #print(buffer)
                
                
                lines = buffer.split("\r\n")
                line = lines[0].split(" ")
                message = line[0]
                URL = lines[0][len(message)+1:]

                if message == "RUN":

                    #print("==================RUN=========================")
                    
                    #print(URL)
                    self.process = subprocess.Popen(["python",URL], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    jobNumber = int(lines[2].split(" ")[1])
                    self.jobList[jobNumber] = self.process
                    #print(self.jobList)
                    #print(str(self.process.poll()))
                    if (self.process.poll() == 0 or self.process.poll() == None):
                        try:
                            f = open(URL,"r")
                            f.close()
                            reply = "1 Process started\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"
                        except:
                            reply = "2 Fail to run\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"
                    else:
                        reply = "2 Fail to run\r\n"
                        reply = reply + "Content-Length: 0\r\n\r\n"

                    buffer=""
                    self.send(reply)

                    #print(reply)

                if message == "STOP":

                    #print("==================STOP=========================")
                    
                    try :
                        #print(self.jobCounter)
                        self.process = self.jobList[int(URL)]
                        #print(str(self.process.poll()))
                        if self.process.poll() == None:
                            self.process.kill()
                            reply = "9 Process stoped\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"
                        else:
                            reply = "3 File not running\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"
                    except Exception as e:
                        reply = "12 ID does not exist\r\n"
                        reply = reply + "Content-Length: 0\r\n\r\n"

                    buffer=""
                    self.send(reply)

                    #print(reply)

                if message == "RETURN":

                    #print("==================RETURN=========================")
                    
                    try:
                        
                        #print(str(self.process.poll()))

                        self.process = self.jobList[int(URL)]
                        if self.process.poll() == 0:
                            reply = "6 Result found\r\n"
                            data = self.process.stdout.read().decode()
                            reply = reply + "Content-Length: " + str(len(data)) + "\r\n\r\n"
                            reply = reply + data
                        elif self.process.poll() == None:
                            reply = "4 Process still running\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"
                        else:
                            reply = "11 No result due to forced stop\r\n"
                            reply = reply + "Content-Length: 0\r\n\r\n"

                            
                    except:
                        reply = "5 Result not found\r\n"
                        reply = reply + "Content-Length: 0\r\n\r\n"

                    buffer=""
                    self.send(reply)

                    #print(reply)

                if message == "GET":

                    #print("==================GET=========================")

                    #print("URL: "+URL)
                    
                    try:
                        file = open(URL,"r")
                        data = file.read()
                        reply = "8 File found\r\n"
                        reply = reply + "Content-Length: " + str(len(data)) + "\r\n\r\n"
                        reply = reply + data
                        file.close()

                    except:
                        reply = "7 File not found\r\n"
                        reply = reply + "Content-Length: 0\r\n\r\n"

                    buffer=""
                    self.send(reply)

                    #print(reply)


                if message == "SEND":


                    #print("==================SEND=========================")

                    cPoint = buffer.index("\r\n\r\n")
                    expectLen = int(lines[1].split(" ")[2])
                    actualLen = len(buffer[cPoint+4:])
                    if actualLen < expectLen:
                        continue
                    else:
                        data = buffer[cPoint+4:cPoint+4+expectLen]
                        file = open(URL,"w")
                        file.write(data)
                        file.close()
                        reply = "10 File received\r\n"
                        reply = reply + "Content-Length: 0\r\n\r\n"

                        buffer=""
                        self.send(reply)

                        #print(reply)
                    
                    
         
    
if __name__ == "__main__":
    zombie = Zombie(sys.argv[1],sys.argv[2],sys.argv[3])
    zombie.connect()
    zombie.send(zombie.getName())
    zombie.respond()
