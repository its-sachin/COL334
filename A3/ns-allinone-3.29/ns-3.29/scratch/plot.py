from matplotlib import pyplot as plt
from os import listdir
from sys import argv

def First():
    files = []
    for i in listdir():
        if(i.endswith('-out.cwnd') and i.startswith('Tcp')):
            files.append(i)
    drops = []

    for file in files:
        
        time = []
        cwnd = []
        drop = 0
        for line in open(file,'r+').readlines():
            try:
                line = line.split()
                if(line[0] == 'RxDrop'):
                    drop +=1
                else:
                    time.append(float(line[0]))
                    cwnd.append(int(line[1]))
            except:
                continue
        drops.append(drop)
        print('Packets dropped at ',file[:-9],drop)

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "b", markerfacecolor = "b")
        plot.grid(True, color = "k")
        plot.set_title(file[:-9])
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q1-"+file[:-9])
        figure.savefig("Q1-"+file[:-9]+".png")

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (5,5))
        plot.plot([file[:-9] for file in files], drops,"b", linewidth = 2,marker = 'o', markerfacecolor = "b")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets')
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('Protocol')
        figure.canvas.set_window_title("Q1- Dropped")
        figure.savefig("Q1- Dropped.png")

def extractApp(name:str):
    return name[ name.index('[')+1:name.index(']') ]

def extractChannel(name:str):
    firsts = [name.index('['),name.index(']')]
    return name[ name.index('[',firsts[0]+1)+1:name.index(']',firsts[1]+1) ]

def add(time,cwnd,drops,file,val):
    drop = 0
    for line in open(file,'r+').readlines():
        try:
            line = line.split()
            if(line[0] == 'RxDrop'):
                drop +=1
            else:
                time.append(float(line[0]))
                cwnd.append(int(line[1]))
        except:
            continue
    drops[val] = drop
    print('Packets dropped at ',file[:-9],drop)

def SecondA(appDR):
    files = []
    cdr = {2:True,4:True,10:True,20:True,50:True}

    for i in listdir():
        if(i.endswith('-out.cwnd') and i.startswith('a-')):
            try:
                if(float(extractApp(i)) == appDR and cdr.get(float(extractChannel(i)))):
                    files.append(i)
            except:
                return False

    for file in files:
        
        time = []
        cwnd = []
        add(time,cwnd,cdr,file,float(extractChannel(file)))

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "c", markerfacecolor = "c")
        plot.grid(True, color = "k")
        plot.set_title('App DataRate-' + str(appDR) + "Mbps \nChannel DataRate-" + extractChannel(file)+'Mbps')
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q2a_" + file[:-9])
        figure.savefig("Q2a_" + file[:-9]+".png")

    drops = []
    val = []
    for i in cdr:
        if(cdr.get(i)):
            val.append(i)
            drops.append(cdr[i])

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (8,5))
        plot.plot(val, drops,"c", linewidth = 2,marker = 'o', markerfacecolor = "c")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets when App DataRate - ' + str(appDR))
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('Channel Data Rate(Mbps)')
        figure.canvas.set_window_title("Q2a- Dropped")
        figure.savefig("Q2a- Dropped.png")


def SecondB(channelDR):
    files = []
    adr = {0.5:True,1:True,2:True,4:True,10:True}

    for i in listdir():
        if(i.endswith('-out.cwnd') and i.startswith('a-')):
            try:
                if(float(extractChannel(i)) == channelDR and adr.get(float(extractApp(i)))):
                    files.append(i)
            except:
                return False
    drops = []

    for file in files:
        
        time = []
        cwnd = []
        add(time,cwnd,adr,file,float(extractApp(file)))

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "g", markerfacecolor = "g")
        plot.grid(True, color = "k")
        plot.set_title('App DataRate-' + extractApp(file) + "Mbps\nChannel DataRate-" + str(channelDR) + 'Mbps')
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q2b_" + file[:-9])
        figure.savefig("Q2b_" + file[:-9]+".png")

    drops = []
    val = []
    for i in adr:
        if(adr.get(i)):
            val.append(i)
            drops.append(adr[i])

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (8,5))
        plot.plot(val, drops,"g", linewidth = 2,marker = 'o', markerfacecolor = "g")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets when Channel DataRate - ' + str(channelDR) + 'Mbps')
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('App Data Rate(Mbps')
        figure.canvas.set_window_title("Q2b- Dropped")
        figure.savefig("Q2b- Dropped.png")

def Third():
    for i in range(1,4):
        file = open('Third'+str(i)+'-out.cwnd','r+')
        oneT,oneV=[],[]
        twoT,twoV=[],[]
        threeT,threeV=[],[]

        drop=0

        for l in file.readlines():
            line=l.split()

            if(line[0] == 'RxDrop'):
                drop +=1
            else:
                if(line[1]=='1'):
                    oneT.append(float(line[0]))
                    oneV.append(int(line[2]))
                elif(line[1]=='2'):
                    twoT.append(float(line[0]))
                    twoV.append(int(line[2]))
                elif(line[1]=='3'):
                    threeT.append(float(line[0]))
                    threeV.append(int(line[2]))

        a = [[oneT,oneV],[twoT,twoV],[threeT,threeV]]

        print('Dropped packets for Configuration - ' + str(i) +' = ',drop)

        for j in range(3):
            figure,plot = plt.subplots(figsize= (8,5))
            plot.plot(a[j][0],a[j][1],"g",markerfacecolor = "g")
            plot.grid(True, color = "k")
            plot.set_title('Configuration - ' + str(i) + ' Connection - ' +str(j+1))
            plot.set_ylabel('CWND size(bytes)')
            plot.set_xlabel('Time(s)')
            figure.canvas.set_window_title("Q3-Config"+str(i)+'_Con-'+str(j+1))
            figure.savefig("Q3-Config"+str(i)+'_Con-'+str(j+1)+'.png')
        


if(len(argv) == 1):
    First()
    SecondA(2)
    SecondB(6)
    Third()
else:
    try:
        ques = int(argv[1])
    except:
        print('INVALID QUESTION')
        exit()

    if(ques==1):
        First()
    elif(ques==2):

        if(len(argv) == 2):
            SecondA(2)
            SecondB(6)

        else:
            try:
                ques = int(argv[2])
            except:
                print('INVALID SUB QUESTION')
                exit()
            
            if(ques==1):
                SecondA(2)
            elif(ques==2):
                SecondB(6)
    elif(ques==3):
        Third()
plt.show()