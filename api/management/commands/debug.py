import os
import sys
from django.core.management import call_command
from django.core.management.base import BaseCommand


def initialize_debugger():
    import debugpy

    # optionally check to see what env you're running in, you probably only want this for
    # local development, for example: if os.getenv("MY_ENV") == "dev":

    # RUN_MAIN envvar is set by the reloader to indicate that this is the
    # actual thread running Django. This code is in the parent process and
    # initializes the debugger
    if not os.getenv("RUN_MAIN"):
        debugpy.listen(("0.0.0.0", 9999))
        sys.stdout.write("Ready to debug on port 9999\n")


class Command(BaseCommand):
    help = 'Debug mode'

    def handle(self, *args, **kwargs):
        initialize_debugger()
        call_command('runserver', '127.0.0.1:8000')
