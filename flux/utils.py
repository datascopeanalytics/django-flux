
from conf import settings

class Bin(object):
    """Count the number of instances in the interval [beg, end)
    """

    def __init__(self, timeseries, beg, end):
        self.timeseries = timeseries
        self.beg = beg
        self.end = end
        self.count = 0
        self.data = []

    def __contains__(self, t):
        return self.beg <= t < self.end

    def __repr__(self):
        return '[%s, %s): %s' % (self.beg, self.end, self.count)

    # CSS styling functions
    def _pct_str(self, val):
        return "%s%%" % (val*100)

    def _dict2css_str(self, d):
        css_str = ''
        for key, val in d.iteritems():
            css_str += "%s: %s;" % (key, val)
        return css_str

    def inner_style(self):
        h = float(self.count) / self.timeseries.max_count()
        return self._dict2css_str({
            "height": self._pct_str(h),
            # "margin-top": "auto", #self._pct_str(1-h),
        })

    def outer_style(self):
        w = 1.0/len(self.timeseries)
        return self._dict2css_str({
            "width": self._pct_str(w),
        })

class Timeseries(list):

    def __init__(self, beg, end):
        super(Timeseries, self).__init__()
        self.beg = beg
        self.end = end

        # instantiate all of the bins
        beg = self.beg
        while beg<self.end:
            end = beg + settings.FLUX_BIN_SIZE
            self.append(Bin(self, beg, end))
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

    def mean(self):
        """Return the mean count in every bin
        """
        total = 0.0
        for bin in self:
            total += bin.count
        return total / len(self)

    def max_count(self):
        return max([bin.count for bin in self])
