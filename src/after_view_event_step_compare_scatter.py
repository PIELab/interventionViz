__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab


def plot_individuals(data, MINS=10, verbose=False, overlap_okay=False):
    cmap = pylab.cm.get_cmap(name='spectral')
    pnum = 0

    class Colors(object):
        def __init__(self):
            self.i = 0
            self.colors = ['r', 'y', 'g', 'b']
        def next(self):
            self.i += 1
            try:
                return self.colors[self.i]
            except IndexError:
                self.i = 0
                return self.colors[self.i]

    c = Colors()
    for sub in data.subject_data:
        events = sub.avatar_view_data.get_view_event_list()
        for evt in events:
            evt.pnum = pnum

        active_steps, active_pnums = select_events(data, MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
        sedentary_steps, sedentary_pnums = select_events(data, MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
        ttt = range(MINS)

        # TODO: take difference of two series to classify worked/not worked and return score of how well it worked
        #        (aka difference in MINS step count average following an event...)
        # TODO: participants should be different colors, sedentary should be dotted
        color = c.next()
        print color+'..'
        plot_steps_and_average(active_steps, ttt, '', color, show_dots=False)
        plot_steps_and_average(sedentary_steps, ttt, '', color+'--', show_dots=False)
        pnum += 1
        pylab.plt.show()

def select_events(data, mins, events, day_type, overlap_okay, verbose=False):
    """
    returns subselection of events based on given criteria
    :param events: list of ViewEvents to search
    :param day_type: mAvatar.Data.DAY_TYPE to select
    :return: list of ViewEvents which are of given day_type
    """
    steps = list()  # list of lists of steps
    pnums = list()
    skipped = 0  # number of data points skipped
    undata = 0  # number of data points excluded due to selection criteria
    errors = {}
    for evt in events:  # lookup each event and get steps following event
        if evt.activity_type == day_type:
            try:
                steps.append(data.get_steps_after_event(evt, mins, overlap_okay=overlap_okay))
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

    if verbose: print len(pnums), 'active step lists loaded,', skipped, 'skipped,',undata,'unselected. Error summary:'
    print errors
    return steps, pnums

def plot(data, MINS=10, verbose=True, overlap_okay=False, selected_event_type=None):
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

    events = data.get_aggregated_avatar_view_events()

    active_steps, active_pnums = select_events(data, MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
    sedentary_steps, sedentary_pnums = select_events(data, MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
    ttt = range(MINS)  # sequential time indicies

    print len(active_steps)

    plot_steps_and_average(active_steps, ttt, 'bx', 'b')
    plot_steps_and_average(sedentary_steps, ttt, 'r+', 'r')


def plot_steps_and_average(steps, times, dot_formatter, avg_formatter, show_dots=True):
    MINS = len(times)
    avg = [0]*MINS  # average across all participants
    for i in range(len(steps)):  # for each list of steps
        if show_dots:
            pylab.plt.plot(times, steps[i], dot_formatter, markersize=3)
        for min in range(MINS):
            avg[min] += steps[i][min]
    for min in range(MINS):
        avg[min] = avg[min]/float(len(steps))
    pylab.plt.plot(times, avg, avg_formatter, linewidth=4)

#post_event_steps.plot_decaminutes()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)

#post_event_steps.plot_hours()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
