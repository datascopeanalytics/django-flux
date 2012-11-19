import sys
import datetime
import optparse

import twitter

from django.core.management.base import CommandError, BaseCommand

from flux.conf import settings
from flux import models

class Command(BaseCommand):
    __doc__ = """
    Download all of the activity for all of the content feeds (e.g.,
    twitter, RSS, etc). This downloads all of the relevant data and
    stores it in the django database.
    """
    args = ''
    help = __doc__
    option_list = BaseCommand.option_list + (
        optparse.make_option(
            "-q", "--quiet", dest="quiet", action="store_true", default=False, 
            help="do not report updates to stderr."
        ),
    )

    def update_db(self, account, counter):
        """Update the database for this account with the latest date
        counts from counter. If the counts are the same, do not update
        the stored information.
        """
        
        if not isinstance(account, models.Account):
            raise TypeError('account must be of type models.Account')

        for date in sorted(counter):
            instance, created = models.Flux.objects.get_or_create(
                account=account, 
                date=date,
            )
            if created or instance.count < counter[date]:
                instance.count = counter[date]
                instance.save()
                if not self.options["quiet"]:
                    if created:
                        verb = "created"
                    else:
                        verb = "updated"
                    self.stderr.write("%s %s\n" % (verb, instance))

    def update_twitter(self):
        """Update the TwitterStats table for all TwitterAccounts
        """

        for account in models.Account.objects.filter(type__exact="twitter"):
        
            # Get all of the statuses that would appear in the
            # username timeline if you started following this
            # person. Here, we include retweets (include_rts) because
            # all retweets appear in a follower's timeline.
            api = twitter.Api()
            statuses = api.GetUserTimeline(
                account.name,
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
            self.update_db(account, counter)

    def handle(self, *args, **kwargs):

        self.options = kwargs
        self.update_twitter()

            
