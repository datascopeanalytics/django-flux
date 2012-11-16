import sys
import getpass

from django.core.management.base import CommandError, BaseCommand


class Command(BaseCommand):
    __doc__ = """
    Download all of the activity for all of the 'social' feeds (e.g.,
    twitter, RSS, etc). This downloads all of the relevant data and
    stores it locally in the database.
    """
    args = ''
    help = __doc__

    def handle(self, *args, **kwargs):

        raise NotImplementedError
