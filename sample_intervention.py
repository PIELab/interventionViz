import pylab
from datetime import timedelta

from src.settings import setup, DATA_TYPES
from src.post_view_event_steps_bars import makeTheActualPlot, PLOT_TYPES, get_cmap, get_time_indicies, list_subtract
from src.data.Dataset import Dataset

HIGHEST_PNUM = 0


def get_data(pre_win, post_win):
    settings = setup(dataset='test', data_loc='./data/controlIntervention/', subject_n=3)

    data = Dataset(
        settings,
        trim=True,
        check=False,
        used_data_types=[DATA_TYPES.event, DATA_TYPES.fitbit]
    )

    minutes = post_win+pre_win
    PNUM = 0

    bars = []
    for evt in data.subject_data[0].event_data.time:
        time = evt-timedelta(minutes=pre_win)
        bars.append(data.get_steps_after_time(time, minutes, PNUM))

    pids = [1]*len(bars)  # all events are same participant

    return minutes, pids, bars


def plot_all_events():
    pre_win = 60*5   # window size before event
    post_win = 60*5  # window size after event
    event_time = pre_win
    MINS = pre_win + post_win
    minutes, pids, bars = get_data(pre_win, post_win)
    cmap = get_cmap()
    N = len(bars)
    ttt = get_time_indicies(event_time, MINS)
    for ev, event_ts in enumerate(bars):
        pylab.plt.plot(ttt, event_ts, color=cmap(float(ev) / N))
    ax = pylab.gca()
    ax.set_xlabel("minutes since event")
    ax.set_ylabel(str('step count'))


def get_fake_data(pre_win, post_win, minutes, pids, bars):
    # returns data from randomly chosen fake data points
    settings = setup(dataset='test', data_loc='./data/controlIntervention/', subject_n=3)

    data = Dataset(
        settings,
        trim=True,
        check=False,
        used_data_types=[DATA_TYPES.event, DATA_TYPES.fitbit]
    )

    PNUM = 0
    fake_bars = []
    for evt in data.subject_data[0].event_data.time:
        time = evt-timedelta(days=1, minutes=pre_win)  # get random(ish) time
        fake_bars.append(data.get_steps_after_time(time, minutes, PNUM))

    diff_bars = []
    for i in range(len(bars)):
        diff_bars.append(list_subtract(bars[i], fake_bars[i]))

    return minutes, pids, diff_bars


def makePlot(type=PLOT_TYPES.bars, pre_win=60*5, post_win=60*5, color_events=False, comparison=False, edgecolor=None):
    """
    makes aggregation plot of all events (stacked (bars) or average(lines))
    pre_win = 60*5   # window size before event
    post_win = 60*5  # window size after event
    """
    minutes, pids, bars = get_data(pre_win, post_win)

    if comparison:
        minutes, pids, bars = get_fake_data(pre_win, post_win, minutes, pids, bars)

    if color_events:
        pids = range(len(bars))
        p_count = len(bars)
        edgecolor = "none"
    else:
        p_count = HIGHEST_PNUM

    makeTheActualPlot(minutes, pids, bars, p_count, event_time=pre_win, type=type, yLabel='Step Count', edgecolor=edgecolor)

if __name__ == "__main__":
    makePlot()
    pylab.show()