import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker

font = {
    'size':40
}
mpl.rc('font', **font)
plt.rcParams['ytick.direction'] = 'in'
n = 5
x = np.arange(n)+1

HFA=[16.1308,15.6293,15.6913,15.7296,15.7171]
RDA=[21.4824,20.6497,20.6571,20.6143,20.6769]
LB=[12.6129,12.6129,12.6129,12.6129,12.6129]
LB_2=np.array(LB) * 2

NRDFA=[21.46132,20.76518667,20.83806667,20.69069667,20.88703333]
NRDA=[26.43379667,26.09990333,26.24741333,27.82435333,28.81878333]

# for i in range(0,5):
#     NRDFA[i] *= HFA[i]
#     NRDA[i] *= RDA[i]

# NRDFA=[i * np.random.uniform(1.3,1.7) for i in HFA]
# NRDA=[i * np.random.uniform(1.3,1.7) for i in RDA]
# print(np.array(NRDFA) / np.array(HFA))
# print(np.array(NRDA) / np.array(RDA))

NRDFA=np.array(NRDFA) - np.array(HFA)
NRDA=np.array(NRDA) - np.array(RDA)

# Set the title and the labels of x-axis and y-axis
# plt.xlabel('k', fontsize=40)
text=plt.ylabel('Throughput (tps)', fontsize=40)

fig = plt.gcf()
fig.set_size_inches(10, 6)

ax = plt.gca()
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.yaxis.set_major_locator(ticker.MultipleLocator(10.0))
ax.set_ylim([5, 40])

ax.tick_params("y", which='major', length=15, width= 2)

plt.rcParams['hatch.color'] = 'w'
plt.rcParams['hatch.linewidth'] = 3

plt.bar(x - 0.3, LB, width=0.2, label=r'$LB$', color='#DBD0A7')
plt.bar(x + 0.3, LB_2, width=0.2, label=r'$2xLB$', color='#123555')
plt.bar(x - 0.1, HFA, width=0.183, label=r'$HF$-$A$', color='#E69B03', edgecolor='#E69B03', lw='2')
plt.bar(x + 0.1, RDA, width=0.183, label=r'$RD$-$A$', color='#D1494E', edgecolor='#D1494E', lw='2')

plt.bar(x - 0.1, NRDFA, width=0.183, label=r'$NRD_f$-$A$',
        bottom=HFA, hatch='/', edgecolor='#E69B03', color='w',lw='2')
plt.bar(x + 0.1, NRDA, width=0.183, label=r'$NRD$-$A$',
        bottom=RDA, hatch='/', edgecolor='#D1494E', color='w', lw='2')

group_labels = [r'$2^{5}$',r'$2^{6}$',r'$2^{7}$',r'$2^{8}$',r'$2^{9}$']
plt.xticks(x, group_labels, rotation=0)
leg=ax.legend(prop={'size': 26}, bbox_to_anchor=(0, 1.03, 1, 0.2), ncol = 3, loc='center', borderaxespad=0, frameon=False)
# plt.show()

plt.savefig('../../test.pdf',
            bbox_extra_artists=(leg,text),
            bbox_inches='tight')