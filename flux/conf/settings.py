import os
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

# this settings variable specifies the size of the bin in which the
# timeseries data is aggregated
FLUX_BIN_SIZE = getattr(
    settings, "FLUX_BIN_SIZE", 
    datetime.timedelta(days=7)
)
if not isinstance(FLUX_BIN_SIZE, datetime.timedelta):
    msg = 'FLUX_BIN_SIZE must be a datetime.timedelta object'
    raise TypeError(msg)

# specify a bunch of labels for flux account types
FLUX_TWITTER_MEAN_LABEL = getattr(
    settings, "FLUX_TWITTER_MEAN_LABEL", "tweets / week",
)
FLUX_RSS_MEAN_LABEL = getattr(
    settings, "FLUX_RSS_MEAN_LABEL", "posts / week",
)
FLUX_FACEBOOK_MEAN_LABEL = getattr(
    settings, "FLUX_FACEBOOK_MEAN_LABEL", "updates / week",
)
FLUX_LINKEDIN_MEAN_LABEL = getattr(
    settings, "FLUX_LINKEDIN_MEAN_LABEL", "updates / week",
)

# make sure that FLUX_BIN_SIZE evenly divides FLUX_MAX_TIME_WINDOW,
# otherwise we will end up with uneven bins. NOTE: This requirement is
# also enforced in Account.get_timeseries to make sure that timeseries
# bins do not extend into the future.
if FLUX_MAX_TIME_WINDOW.days % FLUX_BIN_SIZE.days != 0:
    msg = "FLUX_BIN_SIZE must evenly divide FLUX_MAX_TIME_WINDOW"
    raise ValueError(msg)


# this settings variable specifies the location to which the icon
# images are uploaded for the Account.icon
FLUX_UPLOAD_TO = getattr(
    settings, "FLUX_UPLOAD_TO",
    os.path.join("uploads", "flux"),
)

