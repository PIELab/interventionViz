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
            if self.ts.empty:
                raise ValueError('loaded time series is empty!')
        except AttributeError:
            raise AttributeError('load_data failed to set self.ts!')

    def reset(self, frequency=None):
        """
        clears all data in the object and resets counters
        """
        freq = frequency or self.frequency
        self = self.__init__(self.source_file, frequency=freq)

    def load_data(self, data_file):
        raise NotImplementedError('abstract method load_data must be implemented by subclass.')