import shlex
import subprocess

from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as BaseCommand
)


class Command(BaseCommand):
    """
    A version of collectstatic that runs `grunt build` first.
    """

    def handle(self, *args, **options):
        if options['dry_run']:
            return

        popen_args = {
            'shell': False,
            'stdin': subprocess.PIPE,
            'stdout': self.stdout,
            'stderr': self.stderr
        }

        # node -e "require('grunt').tasks(['build']);"
        grunt_command = 'node -e "require(\'grunt\').tasks([\'build\']);"'
        subprocess.Popen(shlex.split(grunt_command), **popen_args).wait()

        super(Command, self).handle(*args, **options)
