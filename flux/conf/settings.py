import datetime

from django.conf import settings

# this settings variable specifies the maximum time window over which
# the flux_timeseries template tag aggregates data. That is,
# flux_timeseries uses the lesser of FLUX_MAX_TIME_WINDOW or the
# maximum amount of time that has been parsed to date.
FLUX_MAX_TIME_WINDOW = getattr(
    settings, "FLUX_TIME_WINDOW", 
    datetime.timedelta(days=52*7)
)
if not isinstance(FLUX_MAX_TIME_WINDOW, datetime.timedelta):
    msg = 'FLUX_MAX_TIME_WINDOW must be a datetime.timedelta object'
    raise TypeError(msg)
