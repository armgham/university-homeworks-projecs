# -*- coding: utf-8 -*-
import os
import re
import matplotlib as mpl
import gc

mpl.use('Agg')

import matplotlib.pyplot as plt
from bidi.algorithm import get_display

from .fonts import persian_reshaper
import matplotlib.font_manager as fm


import io


def ds(day):
    if day == get_display(persian_reshaper.reshape('شنبه')):
        return 0
    elif day == get_display(persian_reshaper.reshape('يکشنبه')):
        return 1
    elif day == get_display(persian_reshaper.reshape('دوشنبه')):
        return 2
    elif day == get_display(persian_reshaper.reshape('سه شنبه')):
        return 3
    elif day == get_display(persian_reshaper.reshape('چهارشنبه')):
        return 4
    elif day == get_display(persian_reshaper.reshape('پنج شنبه')):
        return 5
    return -1


def main(data_of_time_table, part=None):
    mpl.interactive(False)
    days = []
    starts = []
    ends = []
    coms = []
    darss = []
    
    colors = ['pink', 'lightgreen', 'lightblue', 'crimson', 'salmon', 'yellow', 'silver', 'yellowgreen', 'y', 'tan',
              'orchid', 'c', 'aqua', 'deeppink']

    for line in data_of_time_table:
        data = line.split(' | ')
        days.append(get_display(persian_reshaper.reshape(data[0])))
        starts.append(float(data[1].split(':')[0]) + float(data[1].split(':')[1]) / 60)
        ends.append(float(data[2].split(':')[0]) + float(data[2].split(':')[1]) / 60)
        if len(data) == 6:
            coms.append(get_display(persian_reshaper.reshape(data[3])))
        darss.append(get_display(persian_reshaper.reshape(data[4])))
    days2 = set(days)
    prop = fm.FontProperties(fname=os.path.dirname(os.path.abspath(__file__))+'/fonts/XP_ZibaBd.ttf')  # os.path.abspath('app/fonts/XP_ZibaBd.ttf'))
    dd = dict((ds(x), x) for x in days2)
    sorted_days = []
    for key in sorted(dd):
        sorted_days.append(dd[key])

    darss = list(set(darss))
    nl = dict((darss[x], x) for x in range(len(darss)))
    mn = min(starts)
    mx = max(ends)
    fig = plt.figure(figsize=(16, 9))
    gc.collect()
    for i, line in zip(range(len(days)), data_of_time_table):
        data = line.split(' | ')
        this_start = float(data[1].split(':')[0]) + float(data[1].split(':')[1]) / 60
        this_end = float(data[2].split(':')[0]) + float(data[2].split(':')[1]) / 60
        temp3 = []
        if len(data[3]) > 200 * (this_end - this_start) / (mx - mn):  # 300
            for iji in range(int(len(data[3]) / (213 * (this_end - this_start) / (mx - mn))) + 1):  # 32
                temp3.append(data[3][iji * int(213 * (this_end - this_start) / (mx - mn)):int(213 * (
                            this_end - this_start) / (mx - mn)) * (iji + 1)])  # 32
            data[3] = '\n'.join(temp3)
        temp5 = []
        if len(data[5]) > (213 * (this_end - this_start) / (mx - mn)):  # 32
            for ijl in range(int(len(data[5]) / (226 * (this_end - this_start) / (mx - mn))) + 1):  # 34
                temp5.append(data[5][ijl * int(226 * (this_end - this_start) / (mx - mn)):int(226 * (this_end - this_start) / (mx - mn)) * (ijl + 1)])  # 34
            data[5] = '\n'.join(temp5)
        if part is None:
            c = colors[nl[get_display(persian_reshaper.reshape(data[4]))]]
        elif days[i] == get_display(persian_reshaper.reshape(part.split(' | ')[0])) and float(part.split(' | ')[1].split(':')[0]) + float(part.split(' | ')[1].split(':')[1]) / 60 == this_start:
            c = 'pink'
        else:
            c = 'whitesmoke'
        plt.fill_between([starts[i] + 0.05, ends[i] - 0.05],
                         [sorted_days.index(days[i]) + 0.53, sorted_days.index(days[i]) + 0.53],
                         [sorted_days.index(days[i]) + 1.3, sorted_days.index(days[i]) + 1.43],
                         color=c, edgecolor='red', linewidth=5)

        temp4 = []
        if len(data[4]) > (150 * (this_end - this_start) / (mx - mn)):  # 24
            for ijk in range(int(len(data[4]) / (180 * (this_end - this_start) / (mx - mn))) + 1):  # 27
                temp4.append(data[4][ijk * int(180 * (this_end - this_start) / (mx - mn)):int(180 * (this_end - this_start) / (mx - mn)) * (ijk + 1)])  # 27
            data[4] = '\n'.join(temp4)

        plt.text(starts[i] + 0.25, sorted_days.index(days[i]) + 0.55,
                 '{0}:{1:0>2}'.format(int(data[1].split(':')[0]), int(data[1].split(':')[1])), va='top', fontsize=7)
        plt.text(ends[i] - 0.05, sorted_days.index(days[i]) + 0.55,
                 '{0}:{1:0>2}'.format(int(data[2].split(':')[0]), int(data[2].split(':')[1])), va='top', fontsize=7)
        plt.text((starts[i] + ends[i]) * 0.5,
                 (sorted_days.index(days[i]) + 0.5 + sorted_days.index(days[i]) + 1.4) * 0.5 - 0.2,
                 get_display(persian_reshaper.reshape(data[4])), ha='center', va='center', fontproperties=prop,
                 fontsize=13 - 1.5 * len(temp4))

        plt.text((starts[i] + ends[i]) * 0.5,
                 (sorted_days.index(days[i]) + sorted_days.index(days[i]) + 2.05) * 0.5,
                 get_display(persian_reshaper.reshape(data[3])), ha='center', va='center', fontsize=9 - len(temp3))
        plt.text((starts[i] + ends[i]) * 0.5,
                 (sorted_days.index(days[i]) + sorted_days.index(days[i]) + 2) * 0.5 + 0.23,
                 get_display(persian_reshaper.reshape(data[5])), ha='center', va='center', fontsize=8 - len(temp5))
    gc.collect()

    """
    examsb = []
    for line in user_data['exams']:
        pattern = r'^.*(?P<y>\d{4})\/(?P<m>\d{2})\/(?P<d>\d{2}).*از ((?P<h>\d{2})\:\d{2}) تا.*$'
        examsb.append(re.search(pattern, line))

    exams = dict(
        (int(k.group('h')) / 24 + int(k.group('d')) + (int(k.group('m')) - 1) * 31 + (int(k.group('y')) - 1) * 31 * 12,
         list()) for k in examsb
        if k is not None)

    [exams[int(k.group('h')) / 24 + int(k.group('d')) + (int(k.group('m')) - 1) * 31 + (
            int(k.group('y')) - 1) * 31 * 12].append(k.group()) for k
     in examsb if k is not None]

    mtermsb = []
    for line in user_data['midterm']:
        pattern = r'^.*(?P<y>\d{4})\/(?P<m>\d{1,2})\/(?P<d>\d{1,2}).*$'
        mtermsb.append(re.search(pattern, line))

    mterms = dict(
        (int(k.group('d')) + (int(k.group('m')) - 1) * 31 + (int(k.group('y')) - 1) * 31 * 12,
         list()) for k in mtermsb
        if k is not None)

    [mterms[int(k.group('d')) + (int(k.group('m')) - 1) * 31 + (
            int(k.group('y')) - 1) * 31 * 12].append(k.group()) for k
     in mtermsb if k is not None]

    
    jj = 0
    exx = mx
    plt.text(exx + 0.5, (1 + 5.5 * len(sorted_days)) * 0.2, get_display(persian_reshaper.reshape(':پایانترم')),
             fontsize=13)

    for key in sorted(exams):
        for j in exams[key]:
            if jj == 8:
                exx -= 4
                jj = 0
            plt.text(exx, (jj + 1.5 + 5.5 * len(sorted_days)) * 0.2, get_display(persian_reshaper.reshape(j)),
                     fontsize=11)
            jj += 1

    if from_scrp:
        mterms = []
    if not from_scrp:
        if 'midterm' in user_data:
            plt.text(mn - 0.05, (1 + 5.5 * len(sorted_days)) * 0.2, get_display(persian_reshaper.reshape('میانترم:')),
                     fontsize=11)
    jj2 = 0
    exx = mn + 3
    for key in sorted(mterms):
        for j in mterms[key]:
            if jj2 == 8:
                exx += 4
                jj2 = 0
            plt.text(exx, (jj2 + 1.5 + 5.5 * len(sorted_days)) * 0.2, get_display(persian_reshaper.reshape(j)),
                     fontsize=11)
            jj2 += 1

    """
    ax = fig.add_subplot(111)

    ax.set_ylim(len(days2) + 2 / 4, 0.4)
    ax.set_xlim(mx, mn)
    ax.set_yticks(range(1, len(days2) + 1))
    ax.set_yticklabels(sorted_days)
    ax.xaxis.grid()
    ax2 = ax.twiny().twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xlim(ax.get_xlim())
    ax2.set_yticks(ax.get_yticks())
    ax2.set_yticklabels(sorted_days, fontsize=13)
    plt.subplots_adjust(left=0.06, bottom=0.26, right=0.95, top=0.96, wspace=0.2, hspace=0.2)

    
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    
    
    
    plt.cla()
    plt.clf()
    ax.cla()
    ax2.cla()
    gc.collect()

    plt.close('all')
    
    return s
    