__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
#from src.util.debug import open_console()
import pylab


def plot_minutes(data, MINS=10, verbose=True, overap_okay=False):
    """
    :param data: dataset object
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
    errors = {}
    for evt in events:  # lookup each event and get steps following event
        try:
            steps.append(data.get_steps_after_event(evt, MINS, overlap_okay=overap_okay))
            pnums.append(evt.pnum)
        except TimeWindowError as e:  # if not enough time between events error
            skipped += 1
            try:  # keep a count of errors encountered
                errors[e.message[:14]+'...'] += 1  # only use first part of error message (because of keys)
            except KeyError:  # if this error has not yet been encountered
                errors[e.message[:14]+'...'] = 1  # add an entry to the dict
            pass

    if verbose: print len(pnums), 'event step lists loaded,', skipped, 'skipped. Error summary:'
    print errors

    # util.debug.open_console()


    ttt = range(MINS)  # sequential time indicies
    bases = [0]*len(ttt)  # keeps track of where the next bar should go
    for i in range(len(pnums)):  # for each list of steps
        pylab.plt.bar(ttt, steps[i], bottom=bases, linewidth=1, width=1, color=cmap(float(pnums[i]) / N))
        bases = [bases[ii] + steps[i][ii] for ii in range(len(bases))]

#post_event_steps.plot_decaminutes()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)

#post_event_steps.plot_hours()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
