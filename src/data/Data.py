__author__ = 'tylarmurray'

class Data(object):
    """
    abstract base data class for building new data on top of
    """
    def __init__(self, data_file, meta_data=None):
        self.meta_data=meta_data
        self.source_file = data_file
        self.load_data(self.source_file)
        try:
            self.ts.head()  # can also print this if you want...
        # NOTE: this breaks on pandas v 0.11:
        #    if self.ts.empty:
        #        raise ValueError('loaded time series is empty!')
        except AttributeError:
            raise AttributeError('overridden load_data failed to set self.ts!')

    def reset(self, frequency=None):
        """
        clears all data in the object and resets counters
        """
        freq = frequency or self.frequency
        self = self.__init__(self.source_file, frequency=freq)

    def load_data(self, data_file):
        raise NotImplementedError('abstract method load_data must be implemented by subclass.')

    def get_earliest_sample(self):
        """
        returns earliest sample dict.
        Assumes that self.ts is stored in chronological order
        """
        return dict(t=self.ts.index[0], v=self.ts[0])

    def get_latest_sample(self):
        """
        returns latest sample dict.
        Assumes that self.ts is stored in chronological order
        """
        return dict(t=self.ts.index[-1], v=self.ts[-1])

    def has_data_after_end(self):
        """
        returns true if data exists after the meta-data study end
        """
        self.get_latest_sample()['t'] > self.meta_data.end

    def has_data_before_start(self):
        """
        returns true if data exists before the meta-data study start
        """
        self.get_earliest_sample()['t'] < self.meta_data.start

    def trim_data(self):
        """
        removes data points from time series self.ts if they are before study start or after study end as specified
        by self.meta_data
        """
        print 'trimmed from ' + self.get_earliest_sample()['t'] + '->' + self.get_latest_sample()['t']
        for i in range(len(self.ts)):
            if self.ts.index[i] < self.meta_data.start or self.ts.index[i] > self.meta_data.end:
                self.ts.pop(self.ts.index[i])
        print '          to ' + self.get_earliest_sample()['t'] + '->' + self.get_latest_sample()['t']