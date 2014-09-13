__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab

def plot_all_participant_scores(data, MINS=10, overlap_okay=True, verbose=False):

    scores = list()
    pnum = 0
    for sub in data.subject_data:
        events = sub.avatar_view_data.get_view_event_list()
        for evt in events:
            evt.pnum = pnum

        active_steps, active_pnums = data.select_events(MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
        sedentary_steps, sedentary_pnums = data.select_events(MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
        ttt = range(MINS)

        act_avg = average_steps_after_events(active_steps, MINS)
        sed_avg = average_steps_after_events(sedentary_steps, MINS)

        assert len(act_avg) == len(sed_avg)
        diff = [0]*len(act_avg)
        for i in range(len(act_avg)):
            diff[i] = act_avg[i] - sed_avg[i]

        scores.append(sum(diff))
        pnum+=1

    # TODO: show each as a bar or dot on the histogram, split into 3 manually specified areas no, neutral, and yes
    #pylab.hist(scores, 10)#, histtype='stepfilled')

    pylab.plot(scores, 'b_', markersize=200)

def average_steps_after_events(steps, MINS):
    avg = [0]*MINS
    for i in range(len(steps)):  # for each list of steps
        for min in range(MINS):
            avg[min] += steps[i][min]
    for min in range(MINS):
        avg[min] = avg[min]/float(len(steps))
    return avg