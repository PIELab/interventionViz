__author__ = 'tylar'

from src.data.Dataset import TimeWindowError
from src.data.mAvatar.Data import DAY_TYPE
#from src.util.debug import open_console()
import pylab

def makeTheActualPlot(MINS, pnums, yValues, N):
    print 'plotting', len(yValues), 'ranges'
    cmap = pylab.cm.get_cmap(name='spectral')
    ttt = range(MINS)  # sequential time indicies
    bases = [0]*len(ttt)  # keeps track of where the next bar should go
    for i in range(len(pnums)):  # for each list of steps
        steps = yValues
        #print len(steps[i]), len(ttt)
        #print steps[i]
        #print ttt
        pylab.plt.bar(ttt, steps[i], bottom=bases, linewidth=1, width=1, color=cmap(float(pnums[i]) / N))
        bases = [bases[ii] + steps[i][ii] for ii in range(len(bases))]


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
