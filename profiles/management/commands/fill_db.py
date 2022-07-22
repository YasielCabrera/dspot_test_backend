from django.core.management.base import BaseCommand, CommandError
from profiles.factories import FullProfileFactory


class Command(BaseCommand):
    help = 'Create fake data in the Data Base.'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of profiles to be created')

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.HTTP_INFO('Creating fake data...'))
        for _ in range(count):
            FullProfileFactory()

        self.stdout.write(self.style.SUCCESS('Successfully created fake data.'))
