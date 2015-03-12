__author__ = 'tylarmurray'

import dateutil.parser    # for parsing datestrings
from datetime import timedelta
import csv        # for csv file reading
from datetime import datetime
from calendar import timegm
import pandas

from src.data.Data import Data as base_data


class Data(base_data):
    """
    fitbit data class for loading, processing, and accessing step counts for one participant in various ways.
    """
    def __init__(self, minute_file, day_file=None, *args, **kwargs):
        """
        :param minute_file: location of file containing minute level step counts.
        :param day_file: location of file containing daily step counts (used only in data validation and (maybe) as a
            shortcut to daily aggregation).
        """
        self.loaded = False

        self.count = 0

        self.time = list()  # list of times which the event occurs
        self.timestamp = list()  # list of timestamps which go along with events

        super(Data, self).__init__(minute_file, *args, **kwargs)

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.time)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

    def load_data(self, file_loc):
        """
        builds the lists of values corresponding to data samples.
        """
        with open(file_loc, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            for r_i, row in enumerate(reader):
                if r_i == 0:  # skip header row
                    continue
                if len(row) > 0:
                    date = row[3]
                    time = row[4]
                    self.time.append(date+' '+time)
                    print self.time[-1]  # TODO: self.timestamps = ???
                else:
                    print 'WARN: empty row detected; assuming EOF'
                    break

        self.ts = pandas.Series(data=[1]*len(self.time), index=self.time)
        self.loaded = True


    def get_view_event_list(self, recovery_period=120, min_view_time=0, max_view_time=60, verbose=True):
        """
        :param recovery_period: [s] time which must have no avatar viewing before a new view event is created.
                The min length of the 'gap' in between view events.
        :param min_view_time: [s] minimum amount of time viewed to count as a view event.
        :return: list of View Events
        """
        # convert params to ms:
        recovery_period *= 1
        min_view_time *= 1000
        max_view_time *= 1000

        events = list()
        long_faults = short_faults = new_points = continued_points = 0
        for i in range(len(self.log_points)):
            pt = self.log_points[i]
            if pt.len > max_view_time:
                # complain, but don't do anything... (this should be fixed beforehand)
                long_faults += 1
                warnings.warn("logged view point is too long!!! OH GOD WHY?!?")

            if pt.len < min_view_time:  # logged point isn't long enough
                short_faults += 1
                continue  # skip it

            elif i == 0:  # no previous point
                # go to next point, create a new event
                events.append(ViewEvent(pt))
                new_points += 1

            elif (pt.t0 - self.log_points[i-1].tf < recovery_period   # if point is close to last point
                and self._check_type_or_fail(pt.type, events[-1].activity_type)):  # and type matches
                # verify that the type is good...
                events[-1].activity_type = self._check_type_or_fail(pt.type, events[-1].activity_type)
                # continue this event
                events[-1].extend_event(pt)
                continued_points += 1

            else:  # this point is far from last point
                # end this event, start new event
                events[-1].end_event(pt)
                events.append(ViewEvent(pt))
                new_points += 1

        # close off and add that last ViewEvent
        events[-1].end_event()

        if verbose:
            print len(events), 'view events created.', new_points, 'initialized and', \
                   continued_points, 'extended. longfaults='+str(long_faults), 'shortfaults='+str(short_faults)
        return events