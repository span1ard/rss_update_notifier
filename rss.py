#!/usr/bin/env python

__author__ = 'span1ard'

import sys
import subprocess
from datetime import datetime
from time import sleep

import feedparser

from settings import *

def config_check():
    if not shell_mode and not subprocess_mode and not stdout_mode and not file_mode:
        print('ERROR: Pick at least one of available modes!')
        sys.exit(1)

def rss_list_read():
    with open(rss_list_file, 'r') as f:
        rss_list = []
        for line in f.readlines():
            if line[0] not in ['#', '\n']:
                rss_list.append(line.rstrip())
        return rss_list

def show_entries(entries_list, diff = False):
    for i in entries_list:
        if diff:
            if subprocess_mode:
                subprocess.call('firefox {}'.format(i.link), shell=True)
            if stdout_mode:
                print(i.link, flush=True)
                # is equivalent to
                # sys.stdout.write(i.link)
                # sys.stdout.flush()
            if file_mode:
                f = open('rss_update.txt', 'a')
                print('{} | {} | {}'.format(i.dt, i.title, i.link), file=f)
                f.close()

        if shell_mode:
            print('{} | {} | {}'.format(i.dt, i.title, i.link))

def main():
    # config_check
    config_check()

    # reading rss list file
    rss_list = rss_list_read()

    # processing rss list items
    try:
        feeds_info = {}
        for i in rss_list:
            feeds_info.update({i: {}})
        init = True

        while True:
            for i in rss_list:
                f = feedparser.parse(i)

                # adding date in the same format for all rss for all feeds
                if len(f.entries):
                    for j in f.entries:
                        normaltime = None
                        try:  # reddit
                            t = j.updated[:-6].replace('T', ' ')
                            format = '%Y-%m-%d %H:%M:%S'
                            normaltime = datetime.strptime(t, format)
                        except:
                            try:
                                t = j.published[5:-6] # upwork syntax
                                format = '%d %b %Y %H:%M:%S'
                                normaltime = datetime.strptime(t, format)
                            except: # other
                                pass
                        if normaltime == None:
                            normaltime = '1970-01-01 00:00:00'
                        j.update({'dt': normaltime})

                # init print
                if init:
                    try:
                        if shell_mode:
                            print('\nChannel: {} ({})'.format(f.feed.title, f.feed.description))
                    except:
                        if shell_mode:
                            print('\nChannel: {}'.format(f.feed.title))

                    if init_ent_count and shell_mode:
                        print('Last {} feeds:'.format(init_ent_count))
                        init_entries = None
                        if len(f.entries) > init_ent_count:
                            show_entries(f.entries[:init_ent_count])
                        else:
                            show_entries(f.entries)
                    if len(f.entries):
                        feeds_info[i] = f.entries

                # comparing new feeds entities with existing
                if len(f.entries):
                    diff = []
                    last_feed_time = None
                    f_count = 0
                    for j in feeds_info[i]:
                        if not f_count:
                            last_feed_time = j.dt
                        if j.dt > last_feed_time:
                            last_feed_time = j.dt
                        f_count += 1
                    if last_feed_time:
                        for j in f.entries:
                         if j.dt > last_feed_time:
                             diff.append(j)
                    if len(diff):
                        if shell_mode:
                            print('\nUPDATE! Channel: {}'.format(f.feed.title))
                        show_entries(diff, True)
                    feeds_info[i] = f.entries
            if init:
                init = False
            sleep(timeout)

    except KeyboardInterrupt:
        if shell_mode:
            print('\nBye!')

if __name__ == '__main__':
    main()
