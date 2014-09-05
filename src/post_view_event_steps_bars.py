__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
import pylab


def plot_minutes(data, MINS=10, verbose=True):
    """
    :param data:
    :param MINS: number of minutes after event which we are looking at
    :param verbose:
    :return:
    """
    N = len(data.pids)
    cmap = pylab.cm.get_cmap(name='spectral')

    events = data.get_aggregated_avatar_view_events()
    steps = list()  # list of lists of steps
    pnums = list()
    skipped = 0
    for evt in events:  # lookup each event and get steps following event
        try:
            steps.append(data.get_steps_after_event(evt, MINS))
            pnums.append(evt.pnum)
        except TimeWindowError:  # if not enough time between events error
            skipped += 1
            pass

    if verbose: print len(pnums), 'event step lists loaded,', skipped, 'skipped'

    ttt = range(MINS)  # sequential time indicies
    bases = [0]*len(ttt)  # keeps track of where the next bar should go
    for i in range(len(pnums)):  # for each list of steps
        pylab.plt.bar(ttt, steps[i], bottom=bases, linewidth=1, width=1, color=cmap(float(pnums[i]) / N))
        bases = [bases[ii] + steps[i][ii] for ii in range(len(bases))]

#post_event_steps.plot_decaminutes()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)

#post_event_steps.plot_hours()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)

