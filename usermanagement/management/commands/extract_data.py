from django.core.management.base import BaseCommand
from pathlib import Path
from io import StringIO
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Dumps database file to fixtures'

    def handle(self, *args, **kwargs):
        buf = StringIO()
        call_command('dumpdata', 'usermanagement.Movies',indent=2, format='json', stdout=buf)
        buf.seek(0)
        with open(Path.cwd().joinpath('usermanagement', 'fixtures', 'movies.json'), 'w',encoding="utf-8") as f:
            f.write(buf.read())
        self.stdout.write("Dumped Movies data")