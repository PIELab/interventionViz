import pylab
from datetime import timedelta

from src.settings import setup, DATA_TYPES
from src.post_view_event_steps_bars import makeTheActualPlot, PLOT_TYPES, get_cmap, get_time_indicies
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


def makePlot(type=PLOT_TYPES.bars, pre_win=60*5, post_win=60*5):
    """
    makes aggregation plot of all events (stacked (bars) or average(lines))
    pre_win = 60*5   # window size before event
    post_win = 60*5  # window size after event
    """
    minutes, pids, bars = get_data(pre_win, post_win)

    makeTheActualPlot(minutes, pids, bars, HIGHEST_PNUM, event_time=pre_win, type=type, yLabel='Step Count')

if __name__ == "__main__":
    makePlot()
    pylab.show()