from django.db import models

class BaseAccount(models.Model):
    """Base model for storing information about each account we want
    to track.
    """
    
    class Meta:
        abstract = True

    id = models.CharField(
        max_length=255,
        unique=True,
        primary_key=True,
        help_text="Enter the id of the account to track",
    )
    other = models.TextField(
        help_text="Other data associated with this account. JSON format.",
    )

class BaseStats(models.Model):
    """Base model for storing social activity stats for various data feeds.
    """

    class Meta:
        abstract = True

    account = models.ForeignKey(
        BaseAccount,
        db_index=True,
        help_text="THIS IS OVERRIDDEN BY ALL CHILD CLASSES",
    )
    date = models.DateField(
        unique=True,
        help_text="Enter the date the content was shared.",
    )
    count = models.IntegerField(
        default=0,
        help_text="Enter the number of pieces of content per day",
    )

class TwitterAccount(Account):
    """Twitter accounts to track
    """

class TwitterStats(BaseStats):
    """Track the number of tweets that are posted per day by this
    twitter account
    """
    account = models.ForeignKey(
        TwitterAccount,
    )

# class RssAccount(BaseAccount):
#     """RSS feeds to track
#     """

# class RssStats(BaseStats):
#     """Track the number of articles that are posted per day in the
#     specified RSS feed.
#     """
#     account = models.ForeignKey(
#         RssAccount,
#     )

# class LinkedInAccount(BaseAccount):
#     """LinkedIn feeds to track
#     """

# class LinkedInStats(BaseStats):
#     """Track the number of posts per day to the specified LinkedIn account.
#     """
#     account = models.ForeignKey(
#         LinkedInAccount,
#     )

# class FacebookAccount(BaseAccount):
#     """Facebook accounts to track
#     """

# class FacebookStats(BaseStats):
#     """Track the number of posts per day to this Facebook account.
#     """
#     account = models.ForeignKey(
#         FacebookAccount,
#     )

