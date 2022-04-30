from subprocess import run

def ques1():
    tcp = ['TcpNewReno','TcpHighSpeed','TcpVeno','TcpVegas']
    for i in tcp:
        print('Running Ques 1 on',i)
        run('./waf --run \" scratch/First -TCP=' + i + '\"')
    print()

def ques2():
    parta = [2,4,10,20,50]
    partb = [0.5,1,2,4,10]

    for i in parta:
        print('Running Ques 2 part a on ADR = 2 Mbps CDR = ',i,'Mbps')
        run('./waf --run \" scratch/Second -P=False -ADR=2 -CDR=' + str(i)+ '\"',shell=True)
    for i in partb:
        print('Running Ques 2 part b on ADR =', str(i),'Mbps CDR = 6 Mbps')
        run('./waf --run \" scratch/Second -P=False -ADR=' + str(i) +' -CDR=6\"',shell=True)
    print()

def ques3():

    for i in range(1,4):
        print('Running Ques 3 with configuration = ',i)
        run('./waf --run \" scratch/Third -C='+ str(i)+ '\"',shell=True)
    print()

ques1()
ques2()
ques3()