import pylab
from datetime import timedelta

from src.settings import setup, DATA_TYPES
from src.post_view_event_steps_bars import makeTheActualPlot
from src.data.Dataset import Dataset

HIGHEST_PNUM = 2

settings = setup(dataset='test', data_loc='./data/controlIntervention/', subject_n=3)

data = Dataset(
    settings,
    trim=True,
    check=False,
    used_data_types=[DATA_TYPES.event, DATA_TYPES.fitbit]
)

pre_win = 60*5   # window size before event
post_win = 60*5  # window size after event

minutes = post_win+pre_win
PNUM = 0

bars = []
for evt in data.subject_data[0].event_data.time:
    time = evt-timedelta(minutes=pre_win)
    bars.append(data.get_steps_after_time(time, minutes, PNUM))

pids = [1]*len(bars)  # all events are same participant

makeTheActualPlot(minutes, pids, bars, HIGHEST_PNUM, event_time=pre_win)
pylab.show()