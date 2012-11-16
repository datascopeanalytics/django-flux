from django.db import models

# Create your models here.

class SocialActivityStats(models.Model):
    """Base model for storing social activity stats for various data feeds.
    """

    class Meta:
        abstract = True

    date = models.DateField(
        unique=True,
        help_text="Enter the date the content was shared.",
    )
    count = models.IntegerField(
        default=0,
        help_text="Enter the number of pieces of content per day",
    )

class TwitterStats(SocialActivityStats):
    """Track the number of tweets that are posted per day by the
    twitter account specified by SOCIAL_ACTIVITY_TWITTER_USERNAME
    """

class RssStats(SocialActivityStats):
    """Track the number of articles that are posted per day in the RSS
    feed specified by SOCIAL_ACTIVITY_RSS_URL
    """

class FacebookStats(SocialActivityStats):
    """Track the number of posts shared on Facebook that are posted
    per day by the facebook page account specified by
    SOCIAL_ACTIVITY.FACEBOOK.XXXX
    """

class LinkedInStats(SocialActivityStats):
    """Track the number of posts shared on LinkedIn that are posted
    per day by the LinkedIn account specified by
    SOCIAL_ACTIVITY.LINKEDIN.XXXX
    """
