import pylab
import warnings

import pandas

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset

from src.post_view_event_steps_bars import test_get_avg_list
test_get_avg_list()


### USF mAVATAR DATA LOADING ###
settings = setup(dataset='USF', data_loc='../subjects/', subject_n=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

UP_TO_DATE = True  # true if software versions are good
if pandas.version.version < '0.12.0':
    UP_TO_DATE = False
    print '\n\nWARN: Some analysis cannot be completed due to outdated pandas version ' + pandas.version.version + '\n\n'


### START ACTUAL VISUALS ###



from src.post_view_event_steps_bars import plot_minutes, PLOT_TYPES
plot_minutes(data, MINS=60, verbose=False, overap_okay=True,
             selected_activity_type=DAY_TYPE.active, type=PLOT_TYPES.lines)
pylab.show()

import sample_intervention
from src.post_view_event_steps_bars import PLOT_TYPES
print 'control data all events...'
sample_intervention.plot_all_events()
pylab.show()

print 'control avg...'
sample_intervention.makePlot(type=PLOT_TYPES.lines)
pylab.show()
print 'control stackPlot...'
sample_intervention.makePlot(type=PLOT_TYPES.bars)
pylab.show()

#[8, 10, 11, 12, 13, 15, 26, 28, 32, 44, 49]
import src.day_step_compare as day_step_compare
day_step_compare.plot_all_avg_diffs(data)
pylab.show()
day_step_compare.plot_individual_mirrors_together(data)
pylab.show()

import knowMe
print 'knowMe stackPlot...'
knowMe.makePlot()
pylab.show()

