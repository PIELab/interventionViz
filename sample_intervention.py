import pylab

from src.settings import setup, DATA_TYPES
from src.post_view_event_steps_bars import makeTheActualPlot
from src.data.Dataset import Dataset


settings = setup(dataset='test', data_loc='./data/controlIntervention/', subject_n=3)

data = Dataset(settings, trim=True, check=False, used_data_types=[DATA_TYPES.event, DATA_TYPES.fitbit])