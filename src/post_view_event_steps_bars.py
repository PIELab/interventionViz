__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab
import numpy


class PLOT_TYPES(object):
    """
    """
    bars = 0
    lines = 1


def test_get_avg_list():
    test_list = [[1,1,1,1,1,1,-1,-1,-1],
                 [3,3,3,2,2,2, 1, 1, 1]]
    res_list = get_avg_list(test_list)

    print res_list
    assert(res_list == [2,2,2,1.5,1.5,1.5,0,0,0])
    print 'get avg list works good'


def get_avg_list(yValues):
    """

    :param yValues:
    :return: list of values averaged across all given lists
    """
    #print 'yValues len:', len(yValues)
    n_times = len(yValues[0])
    n_events = len(yValues)
    avgs = [0]*n_times
    for i in range(n_times):  # for each time index
        sum = 0
        for ev in range(n_events):  # for each event series at time i
            event_value = yValues[ev][i]
            sum += event_value
        avgs[i] = sum / float(n_events)
    return avgs


def get_stats(type, yValues):
    """
    returns mean, std_dev
    :param type:
    :return:
    """
    # compute mean & std dev using just the given samples
    if type == PLOT_TYPES.bars:
        bar_total_heights = [0]*len(yValues[0])
        for t in range(len(yValues[0])):
            for event in yValues:
                bar_total_heights[t] += event[t]
        numpy_h = numpy.array(bar_total_heights)
        mean = numpy.mean(numpy_h, axis=0)
        std_dev = numpy.std(numpy_h, axis=0)
    elif type == PLOT_TYPES.lines:
        numpy_h = numpy.array(get_avg_list(yValues))
        mean = numpy.mean(numpy_h, axis=0)
        std_dev = numpy.std(numpy_h, axis=0)
    else:
        raise NotImplementedError('plot type unknown:', type)
    return mean, std_dev


def makeTheActualPlot(MINS, pnums, yValues, N, event_time=None, mean=None, std_dev=None,
                      type=PLOT_TYPES.bars, yLabel="", show_p_averages=True):
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
        mean, std_dev = get_stats(type, yValues)
        print "WARN: using stats computed from window only. mu=", mean, "sigma=", std_dev

    pylab.yticks([mean-5*std_dev, mean-4*std_dev, mean-3*std_dev, mean-2*std_dev, mean-std_dev,
                  mean,
                  mean+std_dev, mean+2*std_dev, mean+3*std_dev, mean+4*std_dev, mean+5*std_dev],
                 [r'-5$\sigma$', r'-4$\sigma$', r'-3$\sigma$', r'-2$\sigma$', r'-1$\sigma$',
                  'mean',
                  r'1$\sigma$', r'+2$\sigma$', r'+3$\sigma$', r'+4$\sigma$', r'+5$\sigma$']
    )

    if type == PLOT_TYPES.bars:
        plotStackedBars(event_time, pnums, yValues, N, MINS)
    elif type == PLOT_TYPES.lines:
        plot_avg_lines(event_time, pnums, yValues, N, MINS, show_p_averages=show_p_averages)
    else:
        raise NotImplementedError('plot type not recognized:'+str(type))

    if event_time is not None:  # draw the event line
        pylab.axvline(x=0, linewidth=5, linestyle='--', color='gray', label='event')
        #pylab.plot(pre_win, 0, marker='*', color='black', markersize=20, fillstyle="full")

    ax = pylab.gca()
    ax.grid(True)
    ax.set_xlabel("Minutes Since Event")

    # show dual axis of actual values
    ax2 = ax.twinx()
    print ax.get_ylim()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_ylabel(yLabel)

    n_events = len(yValues)
    if type == PLOT_TYPES.bars:
        # adjust 2ndary y axis to be average
        ymin, ymax = ax.get_ylim()
        ax2.set_ylim(ymin/n_events, ymax/n_events)
        ax2.set_ylabel('average' + str(yLabel))


def get_cmap():
    return pylab.cm.get_cmap(name='spectral')


def get_time_indicies(event_time, MINS):
    if event_time is not None:  # adjust minutes so that event is at t=0
        return range(-event_time, MINS-event_time)
    else:
        return range(MINS)  # sequential time indicies


def plot_avg_lines(event_time, pnums, yValues, N, MINS, show_p_averages=True, show_events=False):
    """
    :param event_time: index of the event in yValues ts
    :param pnums: list of pids matching yValues
    :param yValues: list of time-series hieght values
    :param N:
    :param MINS:
    :param show_p_average: true to show average for each participant
    :param show_events: true to show each event series
    :return:
    """
    ttt = get_time_indicies(event_time, MINS)

    # compute average over all events
    avgs = get_avg_list(yValues)
    cmap = get_cmap()

    if show_p_averages:
        for pid in range(N):
            p_events = []
            for ev, ev_pid in enumerate(pnums):
                if pid == ev_pid:
                    p_events.append(yValues[ev])

            p_avg = get_avg_list(p_events)
            print 'plotting p', pid
            print p_avg[1:5]
            pylab.plt.plot(ttt, p_avg, color=cmap(float(pid) / N))

    if show_events:
        cmap = get_cmap()
        for ev, event_ts in enumerate(yValues):
            pid = pnums[ev]
            pylab.plt.plot(ttt, event_ts, color=cmap(float(pid) / N))

    pylab.plt.plot(ttt, avgs, color=cmap(1.0), linewidth=4)


def plotStackedBars(event_time, pnums, yValues, N, MINS):
        cmap = get_cmap()
        ttt = get_time_indicies(event_time, MINS)

        bases = [0]*len(ttt)  # keeps track of where the next bar should go
        for i in range(len(pnums)):  # for each list of steps
            steps = yValues
            #print len(steps[i]), len(ttt)
            #print steps[i]
            #print ttt
            pylab.plt.bar(ttt, steps[i], bottom=bases, linewidth=1, width=1, color=cmap(float(pnums[i]) / N))
            bases = [bases[ii] + steps[i][ii] for ii in range(len(bases))]


def plot_difference(data, control_event, experimental_event, MINS=10, verbose=True, overlap_okay=False):
    """
    makes plot of difference between experimental event and control event
    :param data:
    :param control_event:
    :param experimental_event:
    :param MINS:
    :param verbose:
    :param overlap_okay:
    :return:
    """
    check_activity_type(control_event)
    check_activity_type(experimental_event)

    cn_steps, cn_pnums = get_steps_after_event_type(data, control_event, MINS, overlap_okay, verbose=verbose)
    ex_steps, ex_pnums = get_steps_after_event_type(data, experimental_event, MINS, overlap_okay, verbose=verbose)

    # TODO: get averages for each pariticpant

    control_avg_ts = get_avg_list(cn_steps)
    experiment_avg_ts = get_avg_list(ex_steps)

    diff_ts = [0]*len(control_avg_ts)
    for t in range(len(control_avg_ts)):
        diff_ts[t] = experiment_avg_ts[t] - control_avg_ts[t]

    makeTheActualPlot(MINS, [1], [diff_ts], len(data.pids), type=PLOT_TYPES.lines, show_p_averages=False)



def check_event_type(event_type):
    if event_type is not None:
        raise NotImplementedError("event type selection not yet implemented")  # TODO: implement!


def check_activity_type(activity_type):
    if activity_type is not None and not DAY_TYPE.is_valid(activity_type):
        raise ValueError('unknown event type selection: ' + str(activity_type))

def plot_minutes(data, MINS=10, verbose=True, overlap_okay=False, selected_activity_type=None,
                 selected_event_type=None, type=PLOT_TYPES.bars):
    """
    plots minutes following specified event type
    :param data: dataset object
    :param MINS: number of minutes after event which we are looking at
    :param selected_activity_type: type of physical activity level selected for (must be in mAvatar.Data.DAY_TYPE)
    :param selected_event_type: type of event to be selected for (must be in mAvatar.ViewEvent.EventTypes)
    :param verbose:
    :return:
    """
    check_event_type(selected_event_type)
    check_activity_type(selected_activity_type)

    steps, pnums = get_steps_after_event_type(data, selected_activity_type, MINS, overlap_okay, verbose=verbose)

    # util.debug.open_console()
    makeTheActualPlot(MINS, pnums, steps, len(data.pids), type=type)


def get_steps_after_event_type(data, selected_activity_type, MINS, overlap_okay, verbose=False):
    """
    :param data: subject data obj
    :param selected_activity_type: evt.activity_type selected for
    :return: list of steps & corresponding list of pids which match
    """
    events = data.get_aggregated_avatar_view_events()
    steps = list()  # list of lists of steps
    pnums = list()
    skipped = 0  # number of data points skipped
    undata = 0  # number of data points excluded due to selection criteria
    errors = {}
    for evt in events:  # lookup each event and get steps following event
        if selected_activity_type is None or evt.activity_type == selected_activity_type:
            try:
                steps.append(data.get_steps_after_event(evt, MINS, overlap_okay=overlap_okay))
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
    return steps, pnums

