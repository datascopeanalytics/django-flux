import os
import datetime

from django.db import models

import utils
from conf import settings

class Account(models.Model):
    """Model for storing information about each account we want to
    track.
    """

    class Meta:
        unique_together = (("type", "name", ), )
        ordering = ("type", "name", )
    
    TYPES = (
        ("twitter", "Twitter"),
        ("rss", "RSS"),

        # # FUTURE
        # ("facebook", "Facebook"),
        # ("google+", "Google+"),
        # ("linkedin", "LinkedIn"),
    )

    type = models.CharField(
        max_length=16,
        db_index=True,
        choices=TYPES,
        help_text="Select the type of account this is.",
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Enter the name of the account to track",
    )
    other = models.TextField(
        help_text="Other data associated with this account. JSON format.",
        blank=True,
    )

    def __unicode__(self):
        return "%s: %s" % (self.type, self.name)

    def get_timeseries(self):
        """Get the timeseries specified for this account.
        """

        # aggregate all of the old data points. 
        #
        # NOTE: this oldest_date functionality isn't quite right. if
        # oldest_date>beg, the last bin can go into the future in the
        # Timeseries
        end = datetime.date.today() 
        beg = end - settings.FLUX_MAX_TIME_WINDOW
        oldest_date = self.flux_set.aggregate(models.Min("date"))['date__min']
        timeseries = utils.Timeseries(
            beg=max(beg, oldest_date),
            end=end,
        )
        for flux in self.flux_set.filter(date__gte=beg, date__lt=end)\
                .order_by("date"):
            timeseries.append((flux.date, flux.count))

        # return a utils.Timeseries instance
        return timeseries

    def get_mean_label_template(self):
        return os.path.join(
            "flux",
            "mean_label_%s.html" % self.type,
        )

class Flux(models.Model):
    """Model for storing social activity flux for various data feeds.
    """

    class Meta:
        unique_together = (("account", "date", ), )
        ordering = ("-date", )

    account = models.ForeignKey(
        Account,
        db_index=True,
        help_text="Select the account with which this Flux datum is associated",
    )
    date = models.DateField(
        db_index=True,
        help_text="Enter the date the content was shared.",
    )
    count = models.IntegerField(
        default=0,
        help_text="Enter the number of pieces of content per day",
    )

    def __unicode__(self):
        return unicode("%s: %s" % (self.account, self.date))
