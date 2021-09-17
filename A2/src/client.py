import socket
from threading import Thread
from os import getpid,kill
from sys import argv

PORT = 9999
MAX_LEN = 2048
FORMAT = 'utf-8'

IP = '192.168.1.6'


class Client:

    def __init__(self):
        try:
            
            try:
                destIP = argv[1]
                    
            except:
                destIP = IP
            
            try:
                destPort = int(argv[2])
            except:
                destPort = PORT

            self.sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.reciever = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sender.connect((destIP,destPort))
            self.reciever.connect((destIP,destPort))

            done=False

            while(not done):
                name=input('Enter Username: ')
                self.sender.send(('REGISTER TOSEND '+name+'\n\n').encode(FORMAT))
                self.reciever.send(('REGISTER TORECV '+name+'\n\n').encode(FORMAT))


                reply1 = self.sender.recv(MAX_LEN).decode(FORMAT)
                reply2 = self.reciever.recv(MAX_LEN).decode(FORMAT)

                if(reply1==reply2):
                    print('\n[SERVER]: ',reply1.strip('\n'))
                else:
                    print('\n[SERVER]: ',reply1.strip('\n'))
                    print('[SERVER]: ',reply2.strip('\n'))

                reply1,reply2=reply1.split(),reply2.split()

                if(reply1[0]=='REGISTERED' ):
                    if(reply1[1]!='TOSEND' or reply1[2]!=name):
                        break
                
                else:
                    break

                if(reply2[0]=='REGISTERED'):
                    if(reply2[1]!='TORECV' or reply2[2]!=name):
                        break

                else:
                    break

                done=True

            if(not done):
                self.active=False
                return

            self.name = name
            self.active=True


        except:
            print("Unable to create/connect client socket")
            exit()

    def send(self):

        def parseOut(data):

            try:
                data=data.strip(' ')
                if(data[0]!='@'):
                    return
                to=''
                i=1
                while(i<len(data) and data[i]!=' '):
                    to+=data[i]
                    i+=1
            
                if(i>=len(data)):
                    return

                return to,data[i:]

            except:
                return

        def parseIn(data):
    
            valid = {'SENT':True,'ERROR':True}

            try:
                s=data.split('\n\n')
                header=s[0].split('\n')
                for i in range(len(header)):
                    header[i]=header[i].split(' ')

                if(len(s)!=2 or valid.get(header[0][0])==None or not (s[1]=='' and len(header)==1)):
                    return 

                if(s[1]==''):

                    if(header[0][0]=='SENT'):
                        return 'SENT','SERVER',s[0]

                    elif(header[0][0]=='ERROR'):
                        return 'ERROR','SERVER',s[0]

            except:
                return

        print('Type messages in chat with format <@to msg>')
        while (self.sender):

            par=None
            while(not par):
                data=input()
                par=parseOut(data)
                if(par==None):
                    print('Message format INVALID')
                elif(par[0]==self.name):
                    print('Cant send to yourself')
                    par=None
                

            data=('SEND ' + par[0] + '\n' + 'Content-length: '+str(len(par[1])) +'\n\n' + par[1]).encode(FORMAT)
            if(self.sender):
                self.sender.send(data)
                print('Waiting for reponse')

                ack= parseIn(self.sender.recv(MAX_LEN).decode())
                if(ack):
                
                    print('['+ack[1]+']:',ack[2]+'\n')
                else:
                    print('Message not delivered')

            

    def recieve(self):

        def errorHI():
            self.sender.send(('ERROR 103 Header Incomplete\n\n').encode(FORMAT))

        def parse(data):

            try:
                s=data.split('\n\n')
                header=s[0].split('\n')
                for i in range(len(header)):
                    header[i]=header[i].split(' ')

                if(len(s)!=2 or header[0][0]!='FORWARD' or not (header[1][0]=='Content-length:' and len(s[1]) == int(header[1][1]))):
                    errorHI()
                    return 

                return 'FORWARD',header[0][1],s[1]
            except:
                errorHI()

        while(self.reciever):

            msg= self.reciever.recv(MAX_LEN).decode()
            # print(msg)
            msg= parse(msg)
            if(msg):
                print('['+msg[1]+']:',msg[2]+'\n')
                self.sender.send(('RECIEVED '+msg[1]+'\n\n').encode(FORMAT))

            


    def close(self):
        if(self.sender):
            self.sender.close()
        if(self.reciever):
            self.reciever.close()
        self.active=False




client = Client()

if(not client.active):
    exit()

t1 = Thread(target=client.send)
t2 = Thread(target=client.recieve)

t1.start()
t2.start()

pid = getpid()
while True:
    try:
        if(not client.active or not t1.is_alive() and not t2.is_alive()):
            client.close()
            break
        
    except KeyboardInterrupt:

        print("\nShutting down the Client")
        client.close()
        kill(pid,9)
        break

