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
n = 4
x = np.arange(n)+1

QR_break = [[7.5 - 0.11 - 0.31 - 0.1, 
12.3 - 0.13 - 0.33 - 0.1, 
16.7 - 0.2 - 0.28 - 0.1, 
20.3 - 0.09 - 0.3 - 0.1], 
[0.11, 0.13, 0.2, 0.09], [0.31, 0.33, 0.28, 0.3]]
CAP_break = [[1.7 - 0.13 - 0.1, 
1.76 - 0.12 - 0.1, 
1.83 - 0.11 - 0.1, 
1.96 - 0.09 - 0.1], [0.13, 0.12, 0.11, 0.09], [0, 0, 0, 0]]
L2R_break = [[5.83 - 0.23 - 3.9 - 0.1, 
5.91 - 0.25 - 3.5 - 0.1, 
5.77 - 0.2 - 3.7 - 0.1, 
6.11 - 0.19- 3.8 - 0.1], 
[0.23, 0.25, 0.2, 0.19], [3.9, 3.5, 3.7, 3.8]]
QP_break = [[10.3, 9.9, 9.7, 10.2], [0.1, 0.11, 0.13, 0.09], [0.3, 0.33, 0.29, 0.32]]
L2P_break = [[10.6, 10.2, 9.5, 9.8], [0.2, 0.21, 0.17, 0.16], [3.8, 3.3, 3.9, 4.1]]

QR=[7.5, 12.3, 16.7, 20.3]
CAP=[1.7, 1.76, 1.83, 1.96]
L2R=[5.83, 5.91, 5.77, 6.11]
QP=[10.3 + 0.3 + 0.1, 
9.9 + 0.33 + 0.11,
9.7 + 0.29 + 0.13,
10.2+ 0.32 + 0.09
]
L2P=[10.6 + 3.8 + 0.20,
10.2 + 3.3 + 0.21,
9.5 + 3.9 + 0.17,
9.8+ 4.1 + 0.16
]

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


group_labels = [r'$1$',r'$2$',r'$4$',r'$8$']
plt.xticks(x, group_labels, rotation=0)
leg=ax.legend(prop={'size': 30}, bbox_to_anchor=(-0.07, 1.15, 1, 0.2), ncol = 3, loc='center', borderaxespad=0, frameon=False)
# plt.show()

plt.savefig('../../../dapp_latency.pdf',
            bbox_extra_artists=(leg,text),
            bbox_inches='tight')