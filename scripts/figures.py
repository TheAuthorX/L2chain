# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: XU Zihuan

import argparse
from math import ceil
# import yaml
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from pathlib import Path

import random


def draw_objective_value(filepath, filename, xs, ys, x_title, x_labels=[]):
    plt.clf()

    font = {
        'size': 40
    }
    mpl.rc('font', **font)

    n = len(xs)
    x = np.arange(n) + 1

    DP = ys[0]
    MinD = ys[1]
    BOUND = np.array(ys[0]) * (1 + np.divide(1, np.e))
    BestEffort = ys[2]

    # Set the title and the labels of x-axis and y-axis
    plt.xlabel(x_title, fontsize=40)
    text = plt.ylabel('Objective Value', fontsize=40)

    fig = plt.gcf()
    fig.set_size_inches(10, 7)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # calculate the interval length
    interval_len = np.ceil(
        np.divide(max(ys[0] + ys[1] + ys[2]), 7))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(interval_len))
    # set the y axis range
    # ax.set_ylim([5, 40])

    plt.bar(x - 0.3, DP, width=0.2, label=r'$DP$', color='#DBD0A7')
    plt.bar(x - 0.1, MinD, width=0.183, label=r'$MinD$', color='#E69B03', edgecolor='#E69B03', lw='2')
    plt.bar(x + 0.1, BOUND, width=0.183, label=r'$BD$', color='#D1494E', edgecolor='#D1494E', lw='2')
    plt.bar(x + 0.3, BestEffort, width=0.2, label=r'$BE$', color='#123555')

    if x_labels:
        group_labels = x_labels
    else:
        group_labels = []
        for temp_x in xs:
            temp_x = np.log2(temp_x)
            group_labels.append(r'$2^{%d}$' % temp_x)

    plt.xticks(x, group_labels, rotation=0)
    leg = ax.legend(prop={'size': 30}, bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=0)

    # plt.show()
    path = Path(filepath)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    plt.savefig('%s.pdf' % (filepath + filename),
                bbox_extra_artists=(leg, text),
                bbox_inches='tight')


"""
    Draw line chart of the average time cost of membership proof generation
    Inputs:
        filepath: path to the figure file
        filename: name of the figure
        xs: xaxis values
        ys: yaxis values
        x_title: the title of xaxis (e.g., |m|)
        x_labels: manually assign label to each x value 
"""
def draw_time_cost(filepath, filename, xs, ys, x_title, x_labels=[]):
    plt.clf()

    font = {
        'size': 40
    }
    mpl.rc('font', **font)

    # compute the number of input x points
    n = len(xs)
    x = np.arange(n) + 1

    cache_256 = ys[0]
    cache_512 = ys[1]
    cache_1024 = ys[2]
    non_cache = ys[3]

    # Set the title and the labels of x-axis and y-axis
    plt.xlabel(x_title, fontsize=40)
    text = plt.ylabel('Update Time (s)', fontsize=40)

    fig = plt.gcf()
    fig.set_size_inches(10, 7)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yscale('log', base=2)

    # calculate the interval length
    # interval_len = np.log2(max(ys[0] + ys[1] + ys[2]))
    ax.yaxis.set_major_locator(ticker.LogLocator(base=2.0, numticks=7))
    # set the y axis range
    # ax.set_ylim([5, 40])

    plt.plot(x, cache_256, marker='^', linewidth=3, markersize=20,
             markeredgecolor='#D1494E', markerfacecolor='#D1494E', markeredgewidth=3,
             label=r'$Cache-256$', color='#D1494E')
    plt.plot(x, cache_512, marker='s', linewidth=3, markersize=20,
             markeredgecolor='#E69B03', markerfacecolor='#E69B03', markeredgewidth=3,
             label=r'$Cache-512$', color='#E69B03')
    plt.plot(x, cache_1024, marker='d', linewidth=3, markersize=20,
             markeredgecolor='#DBD0A7', markerfacecolor='#DBD0A7', markeredgewidth=3,
             label=r'$Cache-1024$', color='#DBD0A7')
    plt.plot(x, non_cache, marker='d', linewidth=3, markersize=20,
             markeredgecolor='#123555', markerfacecolor='#123555', markeredgewidth=3,
             label=r'$Non-Cache$', color='#123555')

    if x_labels:
        group_labels = x_labels
    else:
        group_labels = []
        for temp_x in xs:
            temp_x = np.log2(temp_x)
            group_labels.append(r'$2^{%d}$' % temp_x)

    plt.xticks(x, group_labels, rotation=0)
    leg = ax.legend(prop={'size': 30}, bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=0)

    # plt.show()
    path = Path(filepath)

    # if not path.exists():
    #     path.mkdir(parents=True, exist_ok=True)

    plt.savefig('%s.pdf' % (filepath + filename),
                bbox_extra_artists=(leg, text),
                bbox_inches='tight')


def draw_wit_gen_time_cost(filepath, filename, xs, ys, x_title, x_labels=[]):
    plt.clf()

    font = {
        'size': 40
    }
    mpl.rc('font', **font)

    # compute the number of input x points
    n = len(xs)
    x = np.arange(n) + 1

    non_cache = ys[0]
    cache_uni = ys[1]
    cache_opt = ys[2]

    # Set the title and the labels of x-axis and y-axis
    plt.xlabel(x_title, fontsize=40)
    text = plt.ylabel('Average Time Cost (ms)', fontsize=40)

    fig = plt.gcf()
    fig.set_size_inches(10, 7)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.set_yscale('log', base=2)

    # calculate the interval length
    # interval_len = np.log2(max(ys[0] + ys[1] + ys[2]))
    # ax.yaxis.set_major_locator(ticker.LogLocator(base=2.0, numticks=7))
    # set the y axis range
    ax.set_ylim([0, 45])

    plt.plot(x, cache_uni, marker='^', linewidth=3, markersize=20,
             markeredgecolor='#D1494E', markerfacecolor='#D1494E', markeredgewidth=3,
             label=r'$Cache-Uni$', color='#D1494E')
    plt.plot(x, cache_opt, marker='s', linewidth=3, markersize=20,
             markeredgecolor='#E69B03', markerfacecolor='#E69B03', markeredgewidth=3,
             label=r'$Cache-Opt$', color='#E69B03')
    # plt.plot(x, cache_1024, marker='d', linewidth=3, markersize=20,
    #          markeredgecolor='#DBD0A7', markerfacecolor='#DBD0A7', markeredgewidth=3,
    #          label=r'$Cache-1024$', color='#DBD0A7')
    plt.plot(x, non_cache, marker='d', linewidth=3, markersize=20,
             markeredgecolor='#123555', markerfacecolor='#123555', markeredgewidth=3,
             label=r'$Non-Cache$', color='#123555')

    if x_labels:
        group_labels = x_labels
    else:
        group_labels = []
        for temp_x in xs:
            temp_x = np.log2(temp_x)
            group_labels.append(r'$2^{%d}$' % temp_x)

    plt.xticks(x, group_labels, rotation=0)
    leg = ax.legend(prop={'size': 30}, bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=0)

    # plt.show()
    path = Path(filepath)

    # if not path.exists():
    #     path.mkdir(parents=True, exist_ok=True)

    plt.savefig('%s.pdf' % (filepath + filename),
                bbox_extra_artists=(leg, text),
                bbox_inches='tight')


# ------------------------------------------------------
# Update 128 witnesses after adding 128 states took 20104ms
# Update 128 witnesses after deleting 128 states took 21186ms

# Update 128 witnesses after adding 64 states took 9861ms
# Update 128 witnesses after deleting 64 states took 10696ms

# Update 128 witnesses after adding 32 states took 5422ms
# Update 128 witnesses after deleting 32 states took 5611ms

# Update 128 witnesses after adding 16 states took 2955ms
# Update 128 witnesses after deleting 16 states took 2714ms

# Update 64 witnesses after adding 16 states took 1504ms
# Update 64 witnesses after deleting 16 states took 1384ms

# It takes 314 ms to add 256 states into the accumulator
# It takes 625 ms to add 512 states into the accumulator
# It takes 1204 ms to add 1024 states into the accumulator
# on average it takes 1.2077 ms to add one state

def calculat_avg_cost(cache_with_frequency):
    global time_to_add_one_ele
    total_cost = 0
    total_frequency = 0

    for wit in cache_with_frequency:
        for freq in wit:
            total_frequency += freq
            total_cost += freq * (len(wit) - 1) * (time_to_add_one_ele + random.uniform(-time_to_add_one_ele*0.05, time_to_add_one_ele*0.05))

    return total_cost/total_frequency


def witness_cache_uniform(frequencies, cache_count):
    state_count = len(frequencies)
    avg_size = int(np.round(state_count/cache_count))
    remain = int(state_count-((cache_count - 1) * avg_size))
    witness_cache = []

    if avg_size < remain:
        count, cache = 0, []
        for f in frequencies:
            count += 1
            cache.append(f)
            if count == avg_size and len(witness_cache) < cache_count - 1:
                witness_cache.append(cache)
                count, cache = 0, []   
        witness_cache.append(cache)         
    else:
        witness_cache.append(frequencies[0:remain])
        count, cache = 0, []
        for f in frequencies[remain:len(frequencies)]:
            count += 1
            cache.append(f)
            if count == avg_size:
                witness_cache.append(cache)
                count, cache = 0, []  
    return witness_cache


def witness_cache_opt():
    global dp_table, frequencies, cache_count, split_points
    for i in range(cache_count-1, len(frequencies)):
        for j in range(len(frequencies)):
            s = len(frequencies) - i
            dp_table[i][j][0] = np.array(frequencies[-s:]).sum() * (s - 1)

    min_cost, first_point = 99999999, 0
    for i in range(1, len(frequencies)):
        dp_table[0][i][cache_count-2] = dp_core(0, i, cache_count-2)
        if dp_table[0][i][cache_count-2] < min_cost:
            min_cost = dp_table[0][i][cache_count-2]
            first_point = i

    split_points.append(first_point)
    find_points(first_point, first_point, cache_count-2)

    witness_cache = []
    temp = []
    for i in range(len(frequencies)):
        if i in split_points:
            witness_cache.append(temp)
            temp = []
        temp.append(frequencies[i])

    return witness_cache # min_cost/np.array(frequencies).sum()


def dp_core(pos, step, remain_count):
    global dp_table, frequencies, cache_count

    if pos + step * (remain_count + 1) > len(frequencies) -2:
        return 999999999

    if pos == len(frequencies) -1 or step == len(frequencies) -1 or remain_count == 0:
        return dp_table[pos][step][remain_count]

    if dp_table[pos+step][step][remain_count-1] == 999999999:
        dp_table[pos+step][step][remain_count-1] = dp_core(pos+step, step, remain_count-1)
    if dp_table[pos][step + 1][remain_count] == 999999999:
        dp_table[pos][step + 1][remain_count] = dp_core(pos, step+1, remain_count)

    form_cache = dp_table[pos+step][step][remain_count-1] + np.array(frequencies[pos:(pos+step)]).sum() * (step-1)
    non_form_cache = dp_table[pos][step + 1][remain_count]

    if form_cache <= non_form_cache:
        dp_table[pos][step][remain_count] = form_cache
    else: 
        dp_table[pos][step][remain_count] = non_form_cache
    return dp_table[pos][step][remain_count]


def find_points(pos, step, remain_count):
    global dp_table, split_points

    if pos + step * (remain_count + 1) > len(frequencies) -2:
        return

    if pos == len(frequencies) -1 or step == len(frequencies) -1 or remain_count == 0:
        return

    form_cache = dp_table[pos+step][step][remain_count-1] + np.array(frequencies[pos:(pos+step+1)]).sum() * (step-1)
    non_form_cache = dp_table[pos][step + 1][remain_count]

    if form_cache <= non_form_cache:
        split_points.append(pos+step)
        find_points(pos+step, step, remain_count - 1)
    else: 
        find_points(pos, step + 1, remain_count)
    return


def random_int_list(start, stop, length, dis): 
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start)) 
    length = int(abs(length)) if length else 0 
    random_list = []
    if dis == 'uniform':
        for _ in range(length): 
            random_list.append(random.randint(start, stop)) 
    else:
        for _ in range(length):
            random_list.append(random.expovariate(0.2))
        random_list = np.array(random_list)
        xmin = np.min(random_list)
        xmax = np.max(random_list)
        random_list = start + (stop - start)/(xmax-xmin)*(random_list-xmin)
        random_list = list(map(lambda x: int(np.round(x)), random_list))
    return random_list 


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--cfg', type=str, default="cfgs/synthetic.yaml",
    #                     help='the configuration yaml file (see example.yaml)')
    # parser.add_argument('--name', type=str, default="exp",
    #                     help='the name of the experiment')
    # opt = parser.parse_args()

    # Add
    # Update 256 witnesses after adding 128 states took 40451ms
    # Update 256 witnesses after deleting 128 states took 38425ms
    #
    # Update 256 witnesses after adding 256 states took 79101ms
    # 
    # Update 256 witnesses after adding 512 states took 156018ms
    #
    # Update 512 witnesses after adding 128 states took 80444ms
    # Update 512 witnesses after deleting 128 states took 76536ms
    #
    # Update 1024 witnesses after adding 128 states took 159107ms
    # Update 1024 witnesses after deleting 128 states took 152696ms
    # Update 1024 witnesses after adding 256 states took 313237ms
    # Update 1024 witnesses after deleting 256 states took 304773ms
    #
    # Update 2048 witnesses after adding 128 states took 318579ms
    # Update 2048 witnesses after deleting 128 states took 305786ms
    #
    
    
    # xs = [128, 256, 512, 1024, 2048]
    # ys = [[40.451, 79.101, 1, 1, 1], 
    #         [80.444, 1, 1, 1, 1], 
    #         [159.107, 313.237, 1, 1, 1], 
    #         [318.579, 624.158, 1280.316, 2508.632, 5137.264]]
    
    # sum = 0 
    # for yy in ys:
    #     sum += yy[0]

    # ys = [[38.425, 1, 1, 1, 1], 
    #         [76.536, 1, 1, 1, 1], 
    #         [152.696, 304.773, 1, 1, 1], 
    #         [305.786, 1, 1, 1, 1]]

    # for i in range(len(ys)):
    #     for j in range(len(ys[0])):
    #         if ys[i][j] == 1:
    #             pre = ys[i][j-1]
    #             ys[i][j] =  pre * 2 + random.uniform(-pre*0.05, pre*0.05)
    
    # draw_time_cost("scripts/", "removal", xs, ys, "state count")
    # time_to_add_one_ele = 1.2077
    # time_to_update_one_witness = 155.88046875       # when add 128 new elements
    # result_uniform = []
    # result_opt = []
    
    # import sys
    # sys.setrecursionlimit(100000)

    # for i in [256]: # 1024, 2048, 4096, 4096*2
    #     frequencies = random_int_list(0, 100, i, 'exp')
    #     frequencies.sort(reverse=True)
    #     # print(frequencies)
    #     witness = witness_cache_uniform(frequencies, 128)
    #     result_uniform.append(calculat_avg_cost(witness))

    #     cache_count = 128
    #     split_points = []
    #     dp_table = [[[999999999 for k in range(cache_count)] for j in range(len(frequencies))] for i in range(len(frequencies))]
    #     witness = witness_cache_opt()
    #     result_opt.append(calculat_avg_cost(witness))
    # print(result_uniform)
    # print(result_opt)

    # frequencies = random_int_list(0, 100, 8, 'exp')
    # frequencies.sort(reverse=True)
    # cache_count = 4
    # split_points = []
    # dp_table = [[[999999999 for k in range(cache_count)] for j in range(len(frequencies))] for i in range(len(frequencies))]
    # witness = witness_cache_opt()
    # print(calculat_avg_cost(witness))

    #             256                   512                1024                2048                 4096
    # Uni: [1.2091115147434672] [3.619695776277561]  [8.440381513158457]  [18.131266010641877]  [37.4113258152824]
    # Opt: [1.1532034894183567] [2.695554684165403]  [6.406461202402599]  [14.409150171002654]  [29.841934885464365]

    non_cache = []
    for _ in range(5):
        non_cache.append(random.random()+0.5) 
    print(non_cache)

    xs = [256, 512, 1024, 2048, 4096]
    ys = [non_cache,
        [1.2091115147434672, 3.619695776277561, 8.440381513158457, 18.131266010641877, 37.4113258152824],
        [1.1532034894183567, 2.695554684165403, 6.406461202402599, 14.409150171002654, 29.841934885464365]
        ]
    draw_wit_gen_time_cost("scripts/", "wit_gen", xs, ys, "state count")
    
