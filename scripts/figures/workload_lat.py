from turtle import color
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker

font = {
    'size':40
}
mpl.rc('font', **font)
plt.rcParams['ytick.direction'] = 'in'
n = 3
x = np.arange(n)+1

QR_break = [[0, 
14.7 - 0.13 - 0.33 - 0.1, 
16.7 - 0.18 - 0.32 - 0.1], 
[0.04, 0.13, 0.18], [0.34, 0.33, 0.32]]
CAP_break = [[0, 
1.9 - 0.11 - 0.1, 
2.3 - 0.1 - 0.1], 
[0.09, 0.11, 0.1], [0, 0, 0]]
L2R_break = [[0, 
5.6 - 0.21 - 3.1 - 0.1, 
5.9 - 0.26 - 3.7 - 0.1], 
[0.14, 0.21, 0.26], [0.35, 3.1, 3.7]]
QP_break = [[0, 
10.7 - 0.13 - 0.33 - 0.1, 
11.4 - 0.18 - 0.32 - 0.1], 
[0.05, 0.13, 0.18], [0.35, 0.33, 0.32]]
L2P_break = [[0, 
13.7 - 0.25 - 3.2 - 0.1, 
14.8 - 0.29 - 3.9 - 0.1], 
[0.15, 0.25, 0.29], [0.36, 3.2, 3.9]]

QR=[0.4, 14.7, 16.7]
CAP=[0.1, 1.9, 2.3]
L2R=[0.5, 5.6, 5.9]
QP=[0.4, 10.7, 11.4]
L2P=[0.5, 13.7, 14.8]

# Set the title and the labels of x-axis and y-axis
# plt.xlabel('k', fontsize=40)
text=plt.ylabel('Latency (s)', fontsize=40)

fig = plt.gcf()
fig.set_size_inches(13.5, 6)

ax = plt.gca()
ax.spines['top'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['left'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5.0))
ax.set_ylim([0, 23])

ax.tick_params("y", which='major', length=15, width= 2)

# plt.rcParams['hatch.color'] = 'w'
# plt.rcParams['hatch.linewidth'] = 3

bar_label_size = 26

b1 = plt.bar(x - 0.39, QR, width=0.14, label=r'Quorum-R', color = 'w' , edgecolor='#2C1654', lw='3')
ax.bar_label(b1, fontsize = bar_label_size)
b2 = plt.bar(x - 0.23, CAP, width=0.14, label=r'CAPER', color = 'w', edgecolor='#00BE65', lw='3')
ax.bar_label(b2, fontsize = bar_label_size)
b3 = plt.bar(x - 0.07, L2R, width=0.14, label=r'L2chain-R', color = 'w', edgecolor='#1F6CC0', lw='3')
ax.bar_label(b3, fontsize = bar_label_size)
b4 = plt.bar(x + 0.09, QP, width=0.14, label=r'Quorum-P', color = 'w', edgecolor='#FF6464', lw='3')
ax.bar_label(b4, fontsize = bar_label_size)
b5 = plt.bar(x + 0.25, L2P, width=0.14, label=r'L2chain-P', color = 'w', edgecolor='#FDBF50', lw='3')
ax.bar_label(b5, fontsize = bar_label_size)

plt.bar(x - 0.388, QR_break[0], width=0.11, label=r'Consensus', 
        hatch='//', edgecolor='cyan', color='w',lw='1')
plt.bar(x - 0.388, QR_break[1], width=0.11, label=r'Execution',
        bottom=QR_break[0], hatch='x', edgecolor='#A149FA', color='w',lw='1')
plt.bar(x - 0.388, QR_break[2], width=0.11, label=r'Overhead',
        bottom=np.array(QR_break[0]) + np.array(QR_break[1]), 
        hatch='.', edgecolor='#FF06B7', color='w',lw='1')

plt.bar(x - 0.228, CAP_break[0], width=0.11, 
        hatch='//', edgecolor='cyan', color='w',lw='1')
plt.bar(x - 0.228, CAP_break[1], width=0.11,
        bottom=CAP_break[0], hatch='x', edgecolor='#A149FA', color='w',lw='1')
plt.bar(x - 0.228, CAP_break[2], width=0.11,
        bottom=np.array(CAP_break[0]) + np.array(CAP_break[1]), hatch='.', edgecolor='#FF06B7', color='w',lw='1')

plt.bar(x - 0.0685, L2R_break[0], width=0.11,
        hatch='//', edgecolor='cyan', color='w',lw='1')
plt.bar(x - 0.0685, L2R_break[1], width=0.11,
        bottom=L2R_break[0], hatch='x', edgecolor='#A149FA', color='w',lw='1')
plt.bar(x - 0.0685, L2R_break[2], width=0.11,
        bottom=np.array(L2R_break[0]) + np.array(L2R_break[1]), hatch='.', edgecolor='#FF06B7', color='w',lw='1')

plt.bar(x + 0.0915, QP_break[0], width=0.11,
        hatch='//', edgecolor='cyan', color='w',lw='1')
plt.bar(x + 0.0915, QP_break[1], width=0.11,
        bottom=QP_break[0], hatch='x', edgecolor='#A149FA', color='w',lw='1')
plt.bar(x + 0.0915, QP_break[2], width=0.11,
        bottom=np.array(QP_break[0]) + np.array(QP_break[1]), hatch='.', edgecolor='#FF06B7', color='w',lw='1')

plt.bar(x + 0.25, L2P_break[0], width=0.11,
        hatch='//', edgecolor='cyan', color='w',lw='1')
plt.bar(x + 0.25, L2P_break[1], width=0.11,
        bottom=L2P_break[0], hatch='x', edgecolor='#A149FA', color='w',lw='1')
plt.bar(x + 0.25, L2P_break[2], width=0.11,
        bottom=np.array(L2P_break[0]) + np.array(L2P_break[1]), hatch='.', edgecolor='#FF06B7', color='w',lw='1')


group_labels = [r'read-only',r'read-write',r'write-only']
plt.xticks(x, group_labels, rotation=0)
leg=ax.legend(prop={'size': 30}, bbox_to_anchor=(-0.07, 1.15, 1, 0.2), ncol = 3, loc='center', borderaxespad=0, frameon=False)
# plt.show()

plt.savefig('../../../workload_latency.pdf',
            bbox_extra_artists=(leg,text),
            bbox_inches='tight')