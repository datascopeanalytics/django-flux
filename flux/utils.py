
from conf import settings

class Bin(object):
    """Count the number of instances in the interval [beg, end)
    """

    def __init__(self, beg, end):
        self.beg = beg
        self.end = end
        self.count = 0
        self.data = []

    def __contains__(self, t):
        return self.beg <= t < self.end

    def __repr__(self):
        return '[%s, %s): %s' % (self.beg, self.end, self.count)

class Timeseries(list):

    def __init__(self, beg, end):
        super(Timeseries, self).__init__()
        self.beg = beg
        self.end = end

        # instantiate all of the bins
        beg = self.beg
        while beg<self.end:
            end = beg + settings.FLUX_BIN_SIZE
            self.append(Bin(beg, end))
            beg = end

    # override the append method to call add_to_bin
    def append(self, obj):
        if isinstance(obj, Bin):
            super(Timeseries, self).append(obj)
        elif isinstance(obj, (tuple, list,)):
            self.add_to_bin(*obj)

    def add_to_bin(self, t, count):
        """Add count to the bin that includes time t
        """

        # get the bin corresponding with this point in time
        dt = t - self.beg
        i = dt.days / settings.FLUX_BIN_SIZE.days
        bin = self[i]
        if t not in bin:
            raise ValueError("time %s does not belong in bin %s" % (t, bin))

        # increment the bin count
        bin.count += count

