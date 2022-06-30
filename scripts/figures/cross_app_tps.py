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

QR=[58, 55, 57, 53]
CAP=[1167, 901, 627, 538]
L2R=[2613, 2499, 2243, 2111]
QP=[30, 28, 31, 29]
L2P=[264, 257, 220, 209]

for i in range(len(L2R)):
    L2R[i] = int(L2R[i]/1.8)

for i in range(len(L2R)):
    CAP[i] = int(CAP[i]/1.2)

# Set the title and the labels of x-axis and y-axis
# plt.xlabel('k', fontsize=40)
text=plt.ylabel('Throughput (tps)', fontsize=40)

fig = plt.gcf()
fig.set_size_inches(12, 7)

ax = plt.gca()
ax.spines['top'].set_linewidth(3)
ax.spines['right'].set_linewidth(3)
ax.spines['left'].set_linewidth(3)
ax.spines['bottom'].set_linewidth(3)
ax.yaxis.set_major_locator(ticker.MultipleLocator(300.0))
ax.set_ylim([0, 1600])

ax.tick_params("y", which='major', length=15, width= 2)

plt.rcParams['hatch.color'] = 'w'
plt.rcParams['hatch.linewidth'] = 3

bar_label_size = 26

b1 = plt.bar(x - 0.39, QR, width=0.14, label=r'Quorum-R', color = 'w', edgecolor='#2C1654', lw='3')
ax.bar_label(b1, fontsize = bar_label_size)
b2 = plt.bar(x - 0.23, CAP, width=0.14, label=r'CAPER', color = '#00BE65', edgecolor='#00BE65', lw='3')
ax.bar_label(b2, fontsize = bar_label_size)
b3 = plt.bar(x - 0.07, L2R, width=0.14, label=r'L2chain-R', color = 'w', edgecolor='#1F6CC0', hatch = '/', lw='3')
ax.bar_label(b3, fontsize = bar_label_size)
b4 = plt.bar(x + 0.09, QP, width=0.14, label=r'Quorum-P', color = '#FF6464', edgecolor='#FF6464', lw='3')
ax.bar_label(b4, fontsize = bar_label_size)
b5 = plt.bar(x + 0.25, L2P, width=0.14, label=r'L2chain-P', color = 'w', edgecolor='#FDBF50', hatch = '/', lw='3')
ax.bar_label(b5, fontsize = bar_label_size)


group_labels = [r'$0\%$',r'$20\%$',r'$80\%$',r'$100\%$']
plt.xticks(x, group_labels, rotation=0)
leg=ax.legend(prop={'size': 30}, bbox_to_anchor=(-0.09, 1.03, 1, 0.2), ncol = 3, loc='center', borderaxespad=0, frameon=False)
# plt.show()

plt.savefig('../../../cross_app_tps.pdf',
            bbox_extra_artists=(leg,text),
            bbox_inches='tight')