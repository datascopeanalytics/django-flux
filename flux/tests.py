import datetime

from django.test import TestCase

import models

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
        account = models.Account.objects.get(pk=1)
        timeseries = account.get_timeseries()
        for bin in timeseries:
            self.assertTrue(
                bin.end<datetime.date.today(), 
                "bin '%s' extends into the future!" % bin,
            )
