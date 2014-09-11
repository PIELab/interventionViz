import warnings

import pylab

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.Dataset import Dataset


settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

# # avatar view "score"
# data.get_aggregated_avatar_view_scores().hist(bins=20, histtype='stepfilled')
# pylab.plt.show()


# #'daily step counts'
# data.get_aggregated_fitbit_days_ts().hist(bins=20, histtype='stepfilled')
# pylab.plt.show()


# data.get_aggregated_fitbit_min_ts().hist(bins=50, histtype='stepfilled')#'minute step counts')
# pylab.plt.show()


# data.get_aggregated_avatar_view_days().hist(bins=20, histtype='stepfilled')#'daily avatar view s')
# pylab.plt.show()


# avatar_view_log_points = data.get_aggregated_avatar_view_log_points()#'avatar log points')
# pylab.hist(avatar_view_log_points, 100, histtype='stepfilled')
# pylab.plt.show()


# print 'plotting fitbit time series'
# pylab.plt.figure('fitbit time series')
# for sub in data.subject_data:
#    sub.fitbit_data.ts.plot()
#
# print 'plotting avatar views time series'
# pylab.plt.figure('avatar view time series')
# for sub in data.subject_data:
#    sub.avatar_view_data.ts.plot()
#
# pylab.plt.show()


# # stacked bar chart & p-value
# import src.paired_t_test as paired_t_test
# paired_t_test.plot(data)
# # pylab.plt.show()


# # correlation scatterplot
# import src.scatterplot as scatterplot
# scatterplot.plot(data)
# pylab.show()


# import src.dep.interaction_x_PA.scatterPlot as scatterPlot
# scatterPlot.plot( setup(dataset='USF', dataLoc='../subjects/', subjectN=8) )
# pylab.plt.savefig('scatterPlot.png')

# plot histogram of view event lengths
# events = data.get_aggregated_avatar_view_events()
# lens = [event.length for event in events]
# pylab.hist(lens, 100, histtype='stepfilled')
# pylab.show()


# plot histogram of time between view events
# intervals = list()
# for event in events:
#     try:
#         intervals.append(event.time_until_next_event)
#     except AttributeError:
#         pass
# pylab.hist(intervals, 100, histtype='stepfilled')
# pylab.show()


import src.post_view_event_steps_bars as post_event_steps
# stacked bar chart for every view event, step counts in following 10m... aka:
# Figure ###: Sum of Step Counts Following An Avatar Viewing (minute-level)

post_event_steps.plot_minutes(data, MINS=10)
pylab.show()


## Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
post_event_steps.plot_minutes(data, MINS=45)
pylab.show()


post_event_steps.plot_minutes(data, MINS=60*6, overap_okay=True)
print 'plot next 6 hrs'
pylab.show()


# Figure ###: comparison effect size of avatar view events sorted by amount of time after event being analyzed.
# (bar chart, height=effect size=difference/total step count, leftmost=smallest time (~1m), rightmost=most time (~12hrs)

# bar graph with active-day sedentary-day average difference in subject PA, separating subjects into 3 groups as explained

# additional (non-published) diagnostics:
import src.dep.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.dep.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()
pylab.show()


import src.data.metaData.compareAllLengths as studyLen
studyLen.show()