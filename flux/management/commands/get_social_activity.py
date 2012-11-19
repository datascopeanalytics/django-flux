import sys
import datetime

import twitter

from django.core.management.base import CommandError, BaseCommand

from social_activity.conf import settings
from social_activity import models

class Command(BaseCommand):
    __doc__ = """
    Download all of the activity for all of the 'social' feeds (e.g.,
    twitter, RSS, etc). This downloads all of the relevant data and
    stores it locally in the database.
    """
    args = ''
    help = __doc__

    def update_db(self, counter, model_cls):
        """Update the database specified by model_cls with the latest
        counts from counter. If the counts are the same, do not update
        the stored information.x
        """

        for date in sorted(counter):
            instance, created = model_cls.objects.get_or_create(date=date)
            if created or instance.count < counter[date]:
                instance.count = counter[date]
                instance.save()

    def handle(self, *args, **kwargs):

        # find the number of twitter posts on each day
        if settings.SOCIAL_ACTIVITY_TWITTER_USERNAME:

            # Get all of the statuses that would appear in the
            # username timeline if you started following this
            # person. Here, we include retweets (include_rts) because
            # all retweets appear in a follower's timeline.
            api = twitter.Api()
            statuses = api.GetUserTimeline(
                settings.SOCIAL_ACTIVITY_TWITTER_USERNAME, 
                count=200, # this is the maximum
                include_rts=True,
                # exclude_replies=True,
            )

            # aggregate status count by date
            fmt_str = "%a %b %d %H:%M:%S +0000 %Y"
            counter = {}
            for status in statuses:

                # cast to a datetime.date object
                t = datetime.datetime.strptime(status.created_at, fmt_str)
                t = t.date()

                # count 'em up
                try:
                    counter[t] += 1
                except KeyError:
                    counter[t] = 1

            # insert data into the database
            self.update_db(counter, models.TwitterStats)

        # if settings.SOCIAL_ACTIVITY_RSS_URL:

            
