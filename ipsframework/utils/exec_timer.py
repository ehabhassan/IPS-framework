#! /usr/bin/env python
# -------------------------------------------------------------------------------
# Copyright 2006-2012 UT-Battelle, LLC. See LICENSE for more information.
# -------------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sys
from . import BeautifulSoup
import urllib.request
import urllib.error
import urllib.parse
PLOT = True
try:
    from pylab import figure, xlabel, ylabel, title, grid, plot, show, legend
except:
    PLOT = False


def plot_exec_time(task_time_map):
    figure()
    for (comp_name, time_map) in list(task_time_map.items()):
        x = [float(k) for k in sorted(list(time_map.keys()), key=float)]
        y = [float(time_map[k]) for k in sorted(list(time_map.keys()), key=float)]
        plot(x, y, label=comp_name)
    legend()
    xlabel('Physics Time')
    ylabel('Task execution Time')
    title('Execution time for IPS tasks')
    grid(True)
    show()


def get_task_times(url_list):
    task_time_map = {}
    all_phys_stamps = set()
    for url in url_list:
        try:
            page = urllib.request.urlopen(url)
        except:
            print('Error retreiving URL ', url)
            raise
        parsed_page = BeautifulSoup.BeautifulSoup(page)
        events_table = parsed_page('table')[3]
        events = events_table('tr')[1:]
        for event in events:
            fields = event('td')
            field_values = [field.contents[0].strip() for field in fields]
            if (field_values[2] == 'IPS_TASK_END'):
                # print ' '.join(field_values)
                comp_task = field_values[3]
                comment = field_values[-1]
                exec_time = comment.split()[-2]
                phys_stamp = field_values[-2]
                # print phys_stamp, comp_task, exec_time
                try:
                    comp_task_map = task_time_map[comp_task]
                except KeyError:
                    comp_task_map = {}
                    task_time_map[comp_task] = comp_task_map
                comp_task_map[phys_stamp] = exec_time
                all_phys_stamps.add(phys_stamp)

    print('Phys_stamp', end=' ')
    for comp in list(task_time_map.keys()):
        print(',   ', comp, end=' ')
    print()

    for phys_stamp in sorted(all_phys_stamps, key=float):
        print(phys_stamp, end=' ')
        for comp_map in list(task_time_map.values()):
            # print comp_map
            try:
                print(',   ', comp_map[phys_stamp], end=' ')
            except KeyError:
                print(',           ', end=' ')
                comp_map[phys_stamp] = 'Nan'
        print()

    if (PLOT):
        plot_exec_time(task_time_map)


if __name__ == '__main__':
    get_task_times(sys.argv[1:])
    sys.exit(0)
