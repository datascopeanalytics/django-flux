from django.db import models

class Account(models.Model):
    """Model for storing information about each account we want to
    track.
    """

    class Meta:
        unique_together = (("name", "type", ), )
    
    TYPES = (
        ("twitter", "Twitter"),

        # # FUTURE
        # ("rss", "RSS"),
        # ("facebook", "Facebook"),
        # ("google+", "Google+"),
        # ("linkedin", "LinkedIn"),
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Enter the name of the account to track",
    )
    type = models.CharField(
        max_length=16,
        db_index=True,
        choices=TYPES,
        help_text="Select the type of account this is.",
    )
    other = models.TextField(
        help_text="Other data associated with this account. JSON format.",
    )

class Flux(models.Model):
    """Model for storing social activity flux for various data feeds.
    """

    class Meta:
        unique_together = (("account", "date", ), )

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
