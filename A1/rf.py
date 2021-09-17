from matplotlib import pyplot as plt

dst = 'www.google.com'
a=[
    [1,1,2,4],
    [2,4,5,4],
    [2,5,4,6],
    [2,5,5,4],
    [24,25,24,26],
    [37,54,45,28],
    [0,0,0,0],
    [33,35,35,34],
    [37,39,37,38],
    [31,33,34,34],
    [37,51,44,34],
    [20,21,27,47],
    [14,16,14,15],
    [35,39,35,38]
]
rtt = [0]

for i in a:
    k=0
    for j in range(4):
        k+=i[j]
    k//=4
    rtt.append(k)
plt.plot(rtt, "r", linewidth = 2, marker = 'o', markerfacecolor = "r", label = "RTT(ms)")
plt.grid(True, color = "k")
plt.title('RTT vs hop for ' + dst)
plt.ylabel('RTT(ms)')
plt.xlabel('Hop number')
plt.show()