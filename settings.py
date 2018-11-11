# settings
rss_list_file = 'rss_list.txt'  # file with list your rss channels

timeout = 120  # time between queries

# available modes, pick one or more
subprocess_mode = False

file_mode = False

shell_mode = False # do not set True if stdout_mode True
init_ent_count = 5 # the number of entries from the channel shown at startup, set 0 to disable

stdout_mode = True # do not set True if shell_mode True;
# command: python rss.py | while read -r line;do firefox $line; done;