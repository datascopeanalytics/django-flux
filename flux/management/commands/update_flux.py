import sys
import datetime
import optparse
from collections import Counter

import twitter
import feedparser

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
            "--exclude-rss", dest="update_rss", action="store_false", 
            default=True, help="exclude rss?"
        ),
        optparse.make_option(
            "--exclude-twitter", dest="update_twitter", action="store_false", 
            default=True, help="exclude twitter?"
        ),
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
            counter = Counter()
            fmt_str = "%a %b %d %H:%M:%S +0000 %Y"
            for status in statuses:
                t = datetime.datetime.strptime(status.created_at, fmt_str)
                counter[t.date()] += 1

            # insert data into the database
            self.update_db(account, counter)

    def update_rss(self):
        for account in models.Account.objects.filter(type__exact="rss"):

            # get all of the recent posts via RSS. see
            # http://wiki.python.org/moin/RssLibraries for details
            feed = feedparser.parse(account.name)
            items = feed['items']
        
            # parse all of the dates. 
            #
            # NOTE: this is not properly parsing out the timezone
            # information. %z directive doesn't work? at the end of
            # the day, it doesn't really matter because it will make
            # the same mistake consistenly, but it might be nice to
            # fix at some point
            counter = Counter()
            fmt_str = "%a, %d %b %Y %H:%M:%S %z"
            fmt_str = ' '.join(fmt_str.split()[:-1]) # %z does not work
            for item in items:
                t_str = ' '.join(item['published'].split()[:-1])
                t = datetime.datetime.strptime(t_str, fmt_str)
                counter[t.date()] += 1

            # insert data into the database
            self.update_db(account, counter)

    def handle(self, *args, **kwargs):
        self.options = kwargs
        if self.options["update_twitter"]:
            self.update_twitter()
        if self.options["update_rss"]:
            self.update_rss()

            
