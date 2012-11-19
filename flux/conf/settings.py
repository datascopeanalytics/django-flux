from django.conf import settings

# specify the twitter username and password for which we need to parse
# out the info
SOCIAL_ACTIVITY_TWITTER_USERNAME = getattr(
    settings, 
    "SOCIAL_ACTIVITY_TWITTER_USERNAME",
    None
)

# specify the RSS URL that you want to parse 
SOCIAL_ACTIVITY_RSS_URL = getattr(
    settings, 
    "SOCIAL_ACTIVITY_RSS_URL",
    None
)

# specify facebook account information


# specify linkedin account information
