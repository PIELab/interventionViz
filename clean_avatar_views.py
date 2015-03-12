__author__ = 'tylar'

import csv

from src.settings import setup, DATA_TYPES

MIN_LEN = 10 # min legitimate view time in ms
MAX_LEN = 60*1000  # max legitimate view time in ms
REPLACE_TIME = 10*1000  # length of time placed at start and end of illegitimate times

settings = setup(dataset='USF', data_loc='../subjects/', subject_n=0)

old_total = new_total = replaced = removed = kept = 0  # various counters

pids = settings.get_pid_list()
for pid in pids:
    view_file_loc = setup(dataset=settings.dataset, data_loc=settings.dataLoc, subject_n=pid).get_file_name(DATA_TYPES.avatar_views)

    # read all the rows in
    cols = list()
    with open(view_file_loc, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            old_total += 1
            #print ', '.join(row)    # print the raw data
            # print row        # print raw data matrix
            t0 = int(row[0])
            tf = int(row[1])
            len = int(row[2])
            act = row[3]

            if len < MIN_LEN: # if view less than 10ms
                # remove row
                print 'removed p'+str(pid)+"'s", len, 'ms pt @', t0
                removed += 1
                continue
            if len <= MAX_LEN:  # if this row is fine
                cols.append([t0, tf, len, act])
                kept += 1
                new_total += 1
            else:  # else this row needs to be modified
                replaced += 1
                
                # log point at start of overly long view
                n_tf = t0 + REPLACE_TIME
                cols.append([t0, n_tf, REPLACE_TIME, act])
                new_total += 1

                # log another point at end of overly long view
                n_t0 = tf - REPLACE_TIME
                cols.append([n_t0, tf, REPLACE_TIME, act])
                new_total += 1

                
                print 'replaced p'+str(pid)+"'s", len, 'ms pt @', t0, 'with', REPLACE_TIME, 'ms pts '#@', t0, '&', n_t0
    
    # rewrite the file
    with open(view_file_loc, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in cols:
            writer.writerow(row)

print 'replaced', replaced, 'removed', removed, 'kept', kept, 'rows. Now', new_total, 'rows compared to', old_total, 'originally'
assert old_total == replaced + removed + kept