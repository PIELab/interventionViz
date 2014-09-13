__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab

def plot_individuals(data, MINS=10, verbose=False, overlap_okay=False, show_dots=True):
    figName = "step counts following active vs sedentary view events"
    pylab.figure(figName)
    pnum = 0
    for sub in data.subject_data:
        events = sub.avatar_view_data.get_view_event_list()
        for evt in events:
            evt.pnum = pnum

        active_steps, active_pnums = data.select_events(MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
        sedentary_steps, sedentary_pnums = data.select_events(MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
        ttt = range(MINS)

        pylab.subplot(len(data), 1, pnum)
        plot_steps_and_average(active_steps, ttt, 'bx', 'b', show_dots=show_dots)
        plot_steps_and_average(sedentary_steps, ttt, 'r+', 'r', show_dots=show_dots)
        #pylab.plt.show()
        pnum += 1


def plot_individuals_together(data, MINS=10, verbose=False, overlap_okay=False):
    cmap = pylab.cm.get_cmap(name='spectral')
    pnum = 0
    for sub in data.subject_data:
        events = sub.avatar_view_data.get_view_event_list()
        for evt in events:
            evt.pnum = pnum

        active_steps, active_pnums = data.select_events(MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
        sedentary_steps, sedentary_pnums = data.select_events(MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
        ttt = range(MINS)

        plot_steps_and_average(active_steps, ttt, '', '-', show_dots=False, color=cmap(float(pnum) / float(len(data))))
        plot_steps_and_average(sedentary_steps, ttt, '', '--', show_dots=False, color=cmap(float(pnum) / float(len(data))))
        #pylab.plt.show()
        pnum += 1

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

    active_steps, active_pnums = data.select_events(MINS, events, DAY_TYPE.active, overlap_okay, verbose=verbose)
    sedentary_steps, sedentary_pnums = data.select_events(MINS, events, DAY_TYPE.sedentary, overlap_okay, verbose=verbose)
    ttt = range(MINS)  # sequential time indicies

    print len(active_steps)

    plot_steps_and_average(active_steps, ttt, 'bx', 'b')
    plot_steps_and_average(sedentary_steps, ttt, 'r+', 'r')


def plot_steps_and_average(steps, times, dot_formatter, avg_formatter, show_dots=True, **kwargs):
    MINS = len(times)
    avg = [0]*MINS  # average across all participants
    for i in range(len(steps)):  # for each list of steps
        if show_dots:
            pylab.plt.plot(times, steps[i], dot_formatter, markersize=3, **kwargs)
        for min in range(MINS):
            avg[min] += steps[i][min]
    for min in range(MINS):
        avg[min] = avg[min]/float(len(steps))
    pylab.plt.plot(times, avg, avg_formatter, linewidth=4, **kwargs)

#post_event_steps.plot_decaminutes()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)

#post_event_steps.plot_hours()
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
