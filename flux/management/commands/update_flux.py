import sys
import datetime
import optparse
from collections import Counter
import json
import random
import string
import cookielib
import urllib
import urlparse
import time
import oauth2 as oauth
import httplib2
import os

import twitter
import dateutil.parser
import feedparser
import mechanize
import fbconsole

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
            "--exclude-facebook", dest="update_facebook", action="store_false", 
            default=True, help="exclude facebook?"
        ),
        optparse.make_option(
            "--exclude-linkedin", dest="update_linkedin", action="store_false", 
            default=True, help="exclude linkedin?"
        ),
        optparse.make_option(
            "-q", "--quiet", dest="quiet", action="store_true", default=False, 
            help="do not report updates to stderr."
        ),
        optparse.make_option(
            "-d", "--debug", dest="debug", action="store_true", default=False, 
            help="print debugging information when connecting to services."
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

    def update_counter(self, counter, t):
        """This method is used to update the counter"""
        if not isinstance(counter, Counter):
            raise TypeError("counter must be a collections.Counter object")
        if isinstance(t, datetime.datetime):
            counter[t.date()] += 1
        elif isinstance(t, datetime.date):
            counter[t] += 1
        else:
            msg = "t must be a datetime.datetime or datetime.date instance!"
            raise TypeError(m)

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
                self.update_counter(counter, t)

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
            # NOTE: this uses python-dateutil instead of datetime to
            # properly handle the timezone information
            counter = Counter()
            for item in items:
                t = dateutil.parser.parse(item['published']).date()
                self.update_counter(counter, t)

            # insert data into the database
            self.update_db(account, counter)

    class FacebookOAuthError(Exception): pass


    def setup_browser(self):
        """setup the mechanize browser to handle redirects,
        etc. Helpful resources:

        http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/
        """

        # instantiate the mechanize browser
        br = mechanize.Browser()

        # set different settings
        br.set_handle_equiv(True)
        # br.set_handle_gzip(True) # this is experimental
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(), 
            max_time=1,
        )

        # add debug logging
        if self.options["debug"]:
            br.set_debug_http(True)
            br.set_debug_redirects(True)
            br.set_debug_responses(True)

        # add the cookie jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # setup the headers
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        return br

    def update_facebook(self):
        """get the facebook access token for use with fbconsole by
        programmatic login to the facebook OAuth. Helpful resources:

        http://developers.facebook.com/docs/authentication/server-side/
        """

        for account in models.Account.objects.filter(type__exact="facebook"):
            other = json.loads(account.other)

            try:
                app_id = other["app_id"]
                client_secret = other["client_secret"]
                scope = other["scope"]
                email = other["email"]
                password = other["password"]
            except KeyError:
                msg = "every facebook Account must specify an "
                msg += "app_id, client_secret, scope, email, and password "
                msg += "in the `other` attribute json"
                raise KeyError(msg)

            # the state is a random string that is used in subsequent requests
            state = ''.join((random.choice(string.ascii_lowercase+string.digits)
                             for i in range(20)))

            # open the mechanize browser
            br = self.setup_browser()

            # 1. redirect the "user" to the OAuth dialog
            url = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode({
                "client_id": app_id,
                "redirect_uri": "http://staging.datascopeanalytics.com/www",
                "scope": ','.join(scope),
                "state": state,
            })
            br.open(url)

            # 2. "user" is prompted to authorize your application
            br.select_form(nr=0)
            br.form["email"] = email
            br.form["pass"] = password
            response = br.submit()

            # 3. Once the user is redirected back to our app, parse out the
            #    code generated by facebook
            auth_url = urlparse.urlparse(response.geturl())
            oauth = urlparse.parse_qs(auth_url.query)
            assert oauth["state"][0] == state, "%s != %s" % (
                oauth["state"][0], state,
            )
            code = oauth["code"][0]

            # 4. Exchange the code for a user access token for this user's data
            url="https://graph.facebook.com/oauth/access_token?"
            url += urllib.urlencode({
                "client_id": app_id,
                "redirect_uri": "http://staging.datascopeanalytics.com/www",
                "client_secret": client_secret,
                "code": code,
            })
            br.open(url)
            response = br.response()
            oauth = urlparse.parse_qs(response.read())
            access_token = oauth["access_token"][0]

            # authenticate on facebook
            fbconsole.APP_ID = app_id
            fbconsole.AUTH_SCOPE = scope
            fbconsole.ACCESS_TOKEN = access_token

            if self.options["debug"]:
                print "ACCESS_TOKEN:", fbconsole.ACCESS_TOKEN

            # get all the posts for last year
            now = datetime.datetime.now()
            last_year = now - datetime.timedelta(days=365)
            opts = {
                "fields": "id,name", 
                "since": str(int(time.mktime(last_year.timetuple()))),
            }
            statuses = fbconsole.get("/132503850149625/posts", opts)


            # aggregate status count by date
            counter = Counter()
            fmt_str = "%Y-%m-%dT%H:%M:%S+0000"
            for status in statuses["data"]:
                t = datetime.datetime.strptime(status["created_time"], fmt_str)
                self.update_counter(counter, t)

            # insert data into the database
            self.update_db(account, counter)

    def update_linkedin(self):
        """Helpful links in setting this up
        https://developer.linkedin.com/documents/quick-start-guide
        """

        for account in models.Account.objects.filter(type__exact="linkedin"):
            other = json.loads(account.other)

            try:
                api_key = other["api_key"]
                api_secret = other["api_secret"]
                token = other["token"]
                secret = other["secret"]
            except KeyError:
                msg = "every linkedin Account must specify an "
                msg += "api_key, api_secret, token, and secret "
                msg += "in the `other` attribute json"
                raise KeyError(msg)

            # Use your API key and secret to instantiate consumer object
            consumer = oauth.Consumer(api_key, api_secret)

            # Use your developer token and secret to instantiate
            # access token object
            access_token = oauth.Token(
                key=token,
                secret=secret,
            )

            client = oauth.Client(consumer, access_token)

            # Make call to LinkedIn to retrieve your own profile
            url = "http://api.linkedin.com/v1/companies/%s=%s/updates"%(
                "universal-name",
                account.name, 
            )
            response, content = client.request(url+"?format=json", "GET")
            result = json.loads(content)
            
            # aggregate status count by date
            counter = Counter()
            for status in result["values"]:
                t = datetime.datetime.fromtimestamp(status['timestamp']/1000.)
                self.update_counter(counter, t)

            # insert data into the database
            self.update_db(account, counter)

    def handle(self, *args, **kwargs):
        self.options = kwargs
        if self.options["update_twitter"]:
            self.update_twitter()
        if self.options["update_rss"]:
            self.update_rss()
        if self.options["update_facebook"]:
            self.update_facebook()
        if self.options["update_linkedin"]:
            self.update_linkedin()

            
