import datetime

from django.test import TestCase

import models
from conf import settings

# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

class AccountTest(TestCase):
    
    fixtures = ['test_data.json', ]

    def test_timeseries_bins(self):
        """timeseries bins should not extend into future"""

        # alter the data to make sure that tests give interesting results
        for account in models.Account.objects.iterator():
            today = datetime.date.today()
            for flux in account.flux_set.order_by("date"):
                dt = today - flux.date
                if dt > settings.FLUX_MAX_TIME_WINDOW:
                    flux.delete()
                elif dt.days % settings.FLUX_BIN_SIZE.days != 0:
                    break
                else:
                    flux.delete()


            timeseries = account.get_timeseries()
            self.assertTrue(
                timeseries[-1].end==datetime.date.today(),
                "last bin '%s' does not end today" % timeseries[-1],
            )
