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
    mMonitor data class for loading, processing, and accessing activity levels for one participant in various ways.
    """
    def __init__(self, minute_file, day_file=None, *args, **kwargs):
        """
        :param minute_file: location of file containing minute level step counts.
        :param day_file: location of file containing daily step counts (used only in data validation and (maybe) as a
            shortcut to daily aggregation).
        """


        # TODO!!!


        super(Data, self).__init__(minute_file, *args, **kwargs)
