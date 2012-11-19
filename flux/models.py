from django.db import models

class Account(models.Model):
    """Model for storing information about each account we want to
    track.
    """

    class Meta:
        unique_together = (("type", "name", ), )
        ordering = ("type", "name", )
    
    TYPES = (
        ("twitter", "Twitter"),

        # # FUTURE
        # ("rss", "RSS"),
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
