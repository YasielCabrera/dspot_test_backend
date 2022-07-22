from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from parameterized import parameterized

from profiles.models import Profile


class FillDBTest(TestCase):

    def test_command_no_param(self):
        with self.assertRaises(CommandError) as ce:
            call_command('fill_db')

        self.assertEqual(str(ce.exception),
                         'Error: the following arguments are required: count')

    @parameterized.expand([
        (10, 10),
        (0, 0),
        (-10, 0),
    ])
    def test_command_success(self, count, expected):
        out = StringIO()
        call_command('fill_db', count, stdout=out)

        profile_count = Profile.objects.count()
        self.assertEqual(profile_count, expected)
