__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab
import numpy


def makeTheActualPlot(MINS, pnums, yValues, N, event_time=None, mean=None, std_dev=None ):
    """
    :param MINS: number of minutes
    :param pnums: list of participant id numbers (for coloring the bars)
    :param yValues: list of lists of bar heights
    :param N: highest participant id number (for coloring the bars)

    :param event_time: if given, a vertical line is drawn at the given x value to mark the event

    ideally these values should be passed to represent the mean & std_dev of the full dataset, not just the window
    but if they are not set, then the mean & std_dev of the window will be computed
    :param mean: mean of the sum of all event series
    :param std_dev: standard deviation of the sum of all event series

    :return: None. after running plot should be viewable using pylab.show()
    """
    print 'plotting', len(yValues), 'ranges'

    # set the y-axis to show # of 'sigmas' from mean
    if mean is None and std_dev is None:
        # compute mean & std dev using just the given samples
        bar_total_heights = [0]*len(yValues[0])
        for t in range(len(yValues[0])):
            for event in yValues:
                bar_total_heights[t] += event[t]
        numpy_h = numpy.array(bar_total_heights)
        mean = numpy.mean(numpy_h, axis=0)
        std_dev = numpy.std(numpy_h, axis=0)
        print "WARN: using stats computed from window only. mu=", mean, "sigma=", std_dev
    pylab.yticks([mean-5*std_dev, mean-4*std_dev, mean-3*std_dev, mean-2*std_dev, mean-std_dev,
                  mean,
                  mean+std_dev, mean+2*std_dev, mean+3*std_dev, mean+4*std_dev, mean+5*std_dev],
                 [r'-5$\sigma$', r'-4$\sigma$', r'-3$\sigma$', r'-2$\sigma$', r'-1$\sigma$',
                  'mean',
                  r'1$\sigma$', r'+2$\sigma$', r'+3$\sigma$', r'+4$\sigma$', r'+5$\sigma$']
    )
    pylab.grid(True)

    cmap = pylab.cm.get_cmap(name='spectral')

    if event_time is not None:  # adjust minutes so that event is at t=0
        ttt = range(-event_time, MINS-event_time)
    else:
        ttt = range(MINS)  # sequential time indicies
    bases = [0]*len(ttt)  # keeps track of where the next bar should go
    for i in range(len(pnums)):  # for each list of steps
        steps = yValues
        #print len(steps[i]), len(ttt)
        #print steps[i]
        #print ttt
        pylab.plt.bar(ttt, steps[i], bottom=bases, linewidth=1, width=1, color=cmap(float(pnums[i]) / N))
        bases = [bases[ii] + steps[i][ii] for ii in range(len(bases))]

    if event_time is not None:  # draw the event line
        pylab.axvline(x=0, linewidth=5, linestyle='--', color='gray', label='event')
        #pylab.plot(pre_win, 0, marker='*', color='black', markersize=20, fillstyle="full")


def plot_minutes(data, MINS=10, verbose=True, overap_okay=False, selected_activity_type=None, selected_event_type=None):
    """
    :param data: dataset object
    :param MINS: number of minutes after event which we are looking at
    :param selected_activity_type: type of physical activity level selected for (must be in mAvatar.Data.DAY_TYPE)
    :param selected_event_type: type of event to be selected for (must be in mAvatar.ViewEvent.EventTypes)
    :param verbose:
    :return:
    """
    if selected_event_type is not None:
        raise NotImplementedError("event type selection not yet implemented")  # TODO: implement!

    if selected_activity_type is not None and not DAY_TYPE.is_valid(selected_activity_type):
        raise ValueError('unknown event type selection: ' + str(selected_activity_type))

    events = data.get_aggregated_avatar_view_events()
    steps = list()  # list of lists of steps
    pnums = list()
    skipped = 0  # number of data points skipped
    undata = 0  # number of data points excluded due to selection criteria
    errors = {}
    for evt in events:  # lookup each event and get steps following event
        if selected_activity_type is None or evt.activity_type == selected_activity_type:
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
        else:
            undata += 1

    if verbose: print len(pnums), 'event step lists loaded,', skipped, 'skipped,', undata, 'unselected. Error summary:'
    print errors

    # util.debug.open_console()
    makeTheActualPlot(MINS, pnums, steps, len(data.pids))


#post_event_steps.plot_decaminutes()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)

#post_event_steps.plot_hours()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
