__author__ = 'tylarmurray'

from pandas import Series

class Data(Series):
    """
    abstract base data class for building new data on top of
    """
    def __init__(self, data_file):
        self.source_file = data_file
        self.ts = self.load_data(self.source_file)

    def reset(self, frequency=None):
        '''
        clears all data in the object and resets counters
        '''
        freq = frequency or self.frequency
        self = self.__init__(self.source_file, frequency=freq)

    def load_data(self, data_file):
        raise NotImplementedError('abstract method load_data must be implemented by subclass.')