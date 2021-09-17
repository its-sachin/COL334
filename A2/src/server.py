import socket
from threading import Thread
from os import getpid,kill

MAX_CON = 5
MAX_LEN = 2048
PORT = 9999
FORMAT = 'utf-8'

users = {'ALL': {'reciever':True}}


class ClientSoc:    

    def printNB(self,s):
        while True:
            if(not self.printing):
                self.printing=True
                print(s)
                self.printing=False
                break

    
    def __init__(self,soc,clAdd):

        self.socket=soc
        self.address=clAdd
        self.printing=False
        self.name='ALL'
        self.printNB("----[CONNECTION REQUEST FROM: "+str(clAdd[1]) +"]----")

    def start(self):

        def wellformed(name):
            return name.isalnum()

        def errorNS():
            self.socket.send(('ERROR 101 No User Registered\n\n').encode(FORMAT))
            self.close()

        def errorMU():
            self.socket.send(('ERROR 100 Malformed username\n\n').encode(FORMAT))
            self.close()

        def errorUT():
            self.socket.send(('ERROR 104 Username Taken\n\n').encode(FORMAT))
            self.close()

        def errorHI():
            self.socket.send(('ERROR 103 Header Incomplete\n\n').encode(FORMAT))
            self.close()

        def errorUS():
            self.socket.send(('ERROR 102 Unable to send\n\n').encode(FORMAT))

        def search(name,mode):

            if(not wellformed(name)):
                errorMU()
                return False

            else:
                if(name=='ALL'):
                    errorUT()
                    return False
                if(not users.get(name)):
                    if(self.name=='ALL' or self.name==name):
                        self.name=name
                        users[name]={mode:self.socket,'ack':None}
                else:
                    if(users[name].get(mode)==None):
                        if(self.name=='ALL' or self.name==name):
                            self.printNB('\n[WELCOME ' + name + ' ]\n')
                            self.name=name
                            users[name][mode]=self.socket
                            users[name]['ack']=None

                        else:
                            users[name]=None
                            return False
                    else:
                        errorUT()
                        return False
            return True
        
        def parsedReg(data):
            s=data.split('\n\n')
            if(len(s)==2 and s[-1]==''):
                return s[0]

            return None

        def parsed(data):

            valid = {'SEND':True,'RECIEVED':True,'ERROR':True}
            try:
            
                s=data.split('\n\n')

                header=s[0].split('\n')
                for i in range(len(header)):
                    header[i]=header[i].split(' ')
                
                if(len(s)!=2 or valid.get(header[0][0])==None or not ((s[1]=='' and len(header)==1) or (header[1][0]=='Content-length:' and len(s[1]) == int(header[1][1])))):
                    errorHI()
                    return 

                if(s[1]==''):
    
                    if(header[0][0]=='RECIEVED'):
                        return 'RECIEVED',header[0][1],s[0]

                    elif(header[0][0]=='ERROR'):
                        return 'ERROR',None,s[0]

                    else:
                        errorHI()
            
            except:
                errorHI()
                return

            if(users.get(header[0][1])==None or users[header[0][1]].get('reciever')==None):
                errorUS()
                return

            return 'SEND',header[0][1],s[1]

        def send(data):
            # print(data)
            par=parsed(data)
            # print(self.name,par)
            if(par!=None):
                if(par[0]=='SEND'):

                    self.printNB('[' + self.name + '] to [' + par[1] + ']: '+par[2])
                    if(par[1]=='ALL'):

                        error=False
                        for i in users:
                            if(i!=self.name and i!='ALL' and users[i].get('reciever')!=None):
                                data = ('FORWARD '+ self.name + '\n' +'Content-length: '+str(len(par[2])) +'\n\n' + par[2]).encode(FORMAT)
                                users[i]['sender']=self.name
                                users[i]['reciever'].send(data)
                                while(not users[self.name]['ack']):
                                    pass
                                
                                ack=users[self.name]['ack']
                                users[self.name]['ack']=None

                                if(ack[0]=='ERROR'):
                                    self.socket.send((ack[2]+'\n\n').encode(FORMAT))
                                    error=True
                                    break
                                elif(ack[0]!='RECIEVED'):
                                    errorUS()
                                    error=True
                                    break


                        if(not error):
                            self.socket.send(('SENT ALL '+'\n\n').encode(FORMAT))

                    else:
                        data = ('FORWARD '+ self.name + '\n' +'Content-length: '+str(len(par[2])) +'\n\n' + par[2]).encode(FORMAT)
                        users[par[1]]['sender']=self.name
                        users[par[1]]['reciever'].send(data)
                        while(not users[self.name]['ack']):
                            pass
                        
                        ack=users[self.name]['ack']
                        users[self.name]['ack']=None

                        if(ack[0]=='ERROR'):
                            self.socket.send((ack[2]+'\n\n').encode(FORMAT))
                        elif(ack[0]!='RECIEVED'):
                            errorUS()
                        else:
                            self.socket.send(('SENT '+ par[1]+'\n\n').encode(FORMAT))

                else:
                    sender = users[self.name].get('sender')
                    if(sender):
                        users[sender]['ack']=par[0],par[1],par[2]
                        self.printNB('['+self.name+']: '+par[2]+'\n')



        rec = self.socket.recv(MAX_LEN).decode(FORMAT)
        rec=parsedReg(rec)

        if(rec==None or len(rec.split())<3):
            errorNS()
            return
    
        # self.printNB('----['+str(self.address[1])+']: '+ rec+'----')
        rec=rec.split()

        if(rec[0]=='REGISTER'):

            if(rec[1]=='TOSEND'):

                if(not search(rec[2],'sender')):
                    self.close()
                    return

                self.socket.send(('REGISTERED TOSEND '+ rec[2] +'\n\n').encode(FORMAT))
                    
                while (True):
                    try:
                        rec = self.socket.recv(MAX_LEN).decode(FORMAT)
                        send(rec)
                    except:
                        self.close()
                        break
                    

            elif(rec[1]=='TORECV'):

                if(not search(rec[2],'reciever')):
                    self.close()
                    return 

                self.socket.send(('REGISTERED TORECV '+ rec[2] +'\n\n').encode(FORMAT))

            else:
                errorNS()
        else:
            errorNS()

    def close(self):
        
        if(self.name!='ALL' and users[self.name]==None):
            self.printNB('[DISCONNECTING '+self.name+']')
        users[self.name]=None
        if(self.socket):
            self.socket.close()

class Server:
    

    def __init__(self,ip,port,maxCon):
        try:
            m_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket Created')

            m_socket.bind((ip,port))
            m_socket.listen(maxCon)
            print('Waiting for connections\n')

            self.socket = m_socket

        except:
            print("Unable to create/bind server socket")
            exit()

    def close(self):
        if(self.socket):     
            self.socket.close()

    def start(self):

        while(True):
    
            soc,add = self.socket.accept()
            client = ClientSoc(soc,add)
            
            currTh = Thread(target=client.start)
            currTh.start()


locIP = socket.gethostbyname(socket.gethostname())
print('Local IP: ',locIP)

server = Server(locIP,PORT,MAX_CON)
  
servingTh = Thread(target=server.start,daemon=False)
servingTh.start()
a=socket.socket

pid = getpid()
while True:
    try:
        if(not servingTh.is_alive()):
            server.close()
            break
        
    except KeyboardInterrupt:

        print("\nShutting down the Server")
        server.close()
        kill(pid,9)
        break