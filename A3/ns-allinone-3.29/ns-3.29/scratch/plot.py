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

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "b", markerfacecolor = "b")
        plot.grid(True, color = "k")
        plot.set_title(file[:-9])
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q1-"+file[:-9])

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (8,5))
        plot.plot([file[:-9] for file in files], drops,"b", linewidth = 2,marker = 'o', markerfacecolor = "b")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets')
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('Protocol')
        figure.canvas.set_window_title("Q1- Dropped")

def SecondA(appDR):
    files = []
    for i in listdir():
        if(i.endswith('-out.cwnd') and i.startswith('a-')):
            try:
                if(int(i[2]) == appDR):
                    files.append(i)
            except:
                return False
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

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "c", markerfacecolor = "c")
        plot.grid(True, color = "k")
        plot.set_title('App DataRate-' + file[2] + "Mbps \nChannel DataRate-" + file[10:-9])
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q2a_" + file[:-9])

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (8,5))
        plot.plot([file[10:-9] for file in files], drops,"c", linewidth = 2,marker = 'o', markerfacecolor = "c")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets when App DataRate - ' + str(appDR))
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('Channel Data Rate')
        figure.canvas.set_window_title("Q2a- Dropped")


def SecondB(channelDR):
    files = []
    for i in listdir():
        if(i.endswith('-out.cwnd') and i.startswith('a-')):
            try:
                if(int(i[-14]) == channelDR):
                    files.append(i)
            except:
                return False
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

        figure,plot = plt.subplots(figsize= (10,5))
        plot.plot(time,cwnd, "g", markerfacecolor = "g")
        plot.grid(True, color = "k")
        plot.set_title('App DataRate-' + file[2:-17] + "\nChannel DataRate-" + str(channelDR) + 'Mbps')
        plot.set_ylabel('CWND size(bytes)')
        plot.set_xlabel('Time(s)')
        figure.canvas.set_window_title("Q2b_" + file[:-9])

    if(len(drops) > 0):
        figure,plot = plt.subplots(figsize= (8,5))
        plot.plot([file[2:-17] for file in files], drops,"g", linewidth = 2,marker = 'o', markerfacecolor = "g")
        plot.grid(True, color = "k")
        plot.set_title('Dropped packets when Channel DataRate - ' + str(channelDR) + 'Mbps')
        plot.set_ylabel('# of Dropped packets')
        plot.set_xlabel('App Data Rate')
        figure.canvas.set_window_title("Q2b- Dropped")

if(len(argv) == 1):
    First()
    SecondA(2)
    SecondB(6)
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
plt.show()