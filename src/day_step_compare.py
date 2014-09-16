__author__ = 'tylar'

from src.data.mAvatar.Data import DAY_TYPE
from datetime import datetime
from src.data.Dataset import TimeWindowError

import pylab

def plot_individual_mirrors_together(data):
    cmap = pylab.cm.get_cmap(name='spectral')
    N = len(data)
    for pn in range(N):
        strt = data.subject_data[pn].meta_data.start
        end  = data.subject_data[pn].meta_data.end
        # get t0 @ 00:00 of each active day???
        days = data.subject_data[pn].avatar_view_data.get_day_type_ts(start=strt, end=end)
        act_days = list()
        sed_days = list()
        err = dict()
        for d in range(len(days)):
            try:
                time = days.index[d].to_datetime()
                steps = data.get_steps_after_time(time, 60*24, pn)
                day_t = days[d]
                if day_t == DAY_TYPE.active:
                    # get list of active day step count series
                    act_days.append(steps)

                elif day_t == DAY_TYPE.sedentary:
                    # get list of sed. day step count series
                    sed_days.append(steps)

                elif day_t == 0:
                    continue
                else:
                    try:
                        err[str(day_t)] += 1
                    except KeyError:
                        err[str(day_t)] = 1
                    continue
                    raise AssertionError('day type should be '+str(DAY_TYPE.active)+'|'+str(DAY_TYPE.sedentary)+'|'
                                         + str(DAY_TYPE.neutral)+ '. not '+str(day_t))
            except TimeWindowError:
                continue
        a_avg = [0]*24*60
        s_avg = [0]*24*60
        try:
            for min in range(24*60):
                for stps in act_days:
                    a_avg[min] += stps[min]
                a_avg[min] = a_avg[min]/float(len(act_days))

                for stps in sed_days:
                    s_avg[min] -= stps[min]
                s_avg[min] = s_avg[min]/float(len(sed_days))
        except ZeroDivisionError:  # if act or sed list is empty
            print 'WARN: act or sed list is empty'
            continue

        tt = range(24*60)
        print 'plottting...'
        pylab.plt.plot(tt, a_avg, color=cmap(float(pn) / N))
        pylab.plt.plot(tt, s_avg, color=cmap(float(pn) / N))

    print err

def plot_all_avg_diffs(data, verbose=False):
    cmap = pylab.cm.get_cmap(name='spectral')
    N = len(data)
    n_diffs = 0
    avg_diff = [0]*24*60
    for pn in range(N):
        strt = data.subject_data[pn].meta_data.start
        end  = data.subject_data[pn].meta_data.end
        # get t0 @ 00:00 of each active day???
        days = data.subject_data[pn].avatar_view_data.get_day_type_ts(start=strt, end=end)
        act_days = list()
        sed_days = list()
        err = dict()
        for d in range(len(days)):
            try:
                time = days.index[d].to_datetime()
                steps = data.get_steps_after_time(time, 60*24, pn)
                day_t = days[d]
                if day_t == DAY_TYPE.active:
                    # get list of active day step count series
                    act_days.append(steps)

                elif day_t == DAY_TYPE.sedentary:
                    # get list of sed. day step count series
                    sed_days.append(steps)

                elif day_t == 0:
                    continue
                else:
                    try:
                        err[str(day_t)] += 1
                    except KeyError:
                        err[str(day_t)] = 1
                    continue
                    raise AssertionError('day type should be '+str(DAY_TYPE.active)+'|'+str(DAY_TYPE.sedentary)+'|'
                                         + str(DAY_TYPE.neutral)+ '. not '+str(day_t))
            except TimeWindowError:
                continue
        a_avg = [0]*24*60
        s_avg = [0]*24*60
        diff  = [0]*24*60
        try:
            for min in range(24*60):
                for stps in act_days:
                    a_avg[min] += stps[min]
                a_avg[min] = a_avg[min]/float(len(act_days))

                for stps in sed_days:
                    s_avg[min] += stps[min]
                s_avg[min] = s_avg[min]/float(len(sed_days))

                diff[min] = a_avg[min] - s_avg[min]
                avg_diff[min] += diff[min]

        except ZeroDivisionError:  # if act or sed list is empty
            print 'WARN: act or sed list is empty'
            continue

        tt = range(24*60)
        print 'plottting...'
        pylab.plt.plot(tt, diff, color=cmap(float(pn) / N))
        n_diffs += 1

    if verbose: print err

    for i in range(60*24):
        avg_diff[i] /= float(n_diffs)

    pylab.plt.plot(tt, avg_diff, color=cmap(1.0), linewidth=4)
    pylab.plt.grid(b=True, which='major')