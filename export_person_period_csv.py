__author__ = 'tylar'

import csv
import warnings
#from random import shuffle

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset

EXPORTED_FILE_LOC = '../subjects/person_period_days_halves.csv'
DESIRED_QUALITY = QUALITY_LEVEL.partial

settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=DESIRED_QUALITY, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

shuffled_pids = range(len(data.pids))
# shuffle(shuffled_pids)  # don't bother with this since things get put into the file in pid order anyway

with open(EXPORTED_FILE_LOC+'_pid_map', 'wb') as pid_map:
    writer = csv.writer(pid_map)
    writer.writerow(data.pids)
    writer.writerow(shuffled_pids)

# write the csv file
with open(EXPORTED_FILE_LOC, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'day', 'intervention', 'seconds_viewed', 'step_count'])

    for subN in range(len(data)):
        subject = data.subject_data[subN]
        id = shuffled_pids[subN]

        seconds_viewed = subject.avatar_view_data.get_day_ts(start=subject.meta_data.start, end=subject.meta_data.end)
        step_counts = subject.fitbit_data.get_day_ts(start=subject.meta_data.start, end=subject.meta_data.end)
        interventions = subject.avatar_view_data.get_day_type_ts(start=subject.meta_data.start, end=subject.meta_data.end)

        # The PA vs. Sed is coded is -0.5 and 0.5:
        interv = [0.5 * float(interventions[i]) for i in range(len(interventions))]

        assert len(interventions) == len(interv)
        assert len(interventions) == len(seconds_viewed)
        assert len(interventions) == len(step_counts)

        # time is centered on the first day of use (i.e., day 1 using the system =0, day 2=1, etc).
        for dayN in range(len(interventions)):  # for each day in the data...
            writer.writerow([id, dayN, interv[dayN], seconds_viewed[dayN], step_counts[dayN]])


    # TODO: add:
    # any control variables (are there any factors we measured that might make sense?
    # Don't need them but just thought I'd check) have been checked for normality