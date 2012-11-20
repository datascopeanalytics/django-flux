
class Timeseries(list):
    def __init__(self, beg=None, end=None, *args, **kwargs):
        super(Timeseries, self).__init__(*args, **kwargs)

        self.beg = beg
        self.end = end
