from matplotlib import pyplot as plt
from subprocess import run
from sys import argv

def nslookup(dst):
    temp = open("out.txt", "w")
    run("nslookup " + dst, shell = True, stdout=temp, stderr=temp)

    temp = open("out.txt", "r")
    lines = temp.readlines()
    
    d={}
    key='rf'
    for i in range(4,len(lines)):
        sep = lines[i].split()
        if(len(sep)>0 and sep[0][-1]==':'):
            key=sep[0][:-1]
            if(key=='Addresses'):
                key='Address'

        for j in sep:
            if(d.get(key)==None):
                d[key]=[j]
            else:
                d[key].append(j)

    if(d.get('Address')==None):
        return -1
    return d['Address'][-1]
    

def ping(dst,ttl):
    temp = open("out.txt", "w")
    run("ping -i " +str(ttl) + " " + dst, shell = True, stdout=temp, stderr=temp)

    temp = open("out.txt", "r")
    lines = temp.readlines()

    time=['*']*4
    curr = lines[2].split()[2][:-1]

    if(curr!='out'):
        for i in range(4):
            t=lines[2+i].split()
            if(len(t)>4):
                t=t[4]
                if(t!='expired'):
                    time[i]=t[5:]

    return curr,time
    


if(len(argv)<2):
    dst=input("Domain name: ")
else:
    dst = argv[1]

dstIP = nslookup(dst)
if(dstIP==-1):
    print('Invalid domain')
    exit()

print('\nTracing route to ' + dst + ' [' + dstIP + ']\nover a maximum of 30 hops:\n')

ttl=1
rtt = [0]
while(ttl<=30):
    
    ch=len(str(ttl))
    print(str(ttl) + ' '*(5-ch),end="")

    curr,time = ping(dstIP,ttl)

    if(curr!='out'):
        _,time=ping(curr,ttl+5)

    avg=0
    for i in range(4):
        ch=len(time[i])
        print(time[i] + ' '*(8-ch),end="")

        if(time[i]!='*'):
            avg+=int(time[i][:-2])

    rtt.append(avg//4)

    if(curr!='out'):
        print(curr)
    else:
        print('Request timed out')

    ttl+=1
    if(curr==dstIP):
        break

print('\nTrace Complete.')

plt.plot(rtt, "r", linewidth = 2, marker = 'o', markerfacecolor = "r", label = "RTT(ms)")
plt.grid(True, color = "k")
plt.title('RTT vs hop for ' + dst)
plt.ylabel('RTT(ms)')
plt.xlabel('Hop number')
plt.show()