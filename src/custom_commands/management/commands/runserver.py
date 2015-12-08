import atexit
import os
import psutil
import subprocess
import traceback
from concurrent.futures import ThreadPoolExecutor
from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand
)
from django.core.management.base import CommandError
from signal import SIGTERM


class Command(StaticfilesRunserverCommand):
    """
    Subclass the RunserverCommand from Staticfiles to set up our grunt
    environment.
    """

    def __init__(self, *args, **kwargs):
        self.cleanup_closing = False
        self.grunt_process = None

        super(Command, self).__init__(*args, **kwargs)

    @staticmethod
    def grunt_exited_cb(future):
        if future.exception():
            print(traceback.format_exc())

            children = psutil.Process().children(recursive=True)

            for child in children:
                print('>>> Killing pid {}'.format(child.pid))

                child.send_signal(SIGTERM)

            print('>>> Exiting')

            # It would be nice to be able to raise a CommandError or use
            # sys.kill here but neither of those stop the runserver instance
            # since we're in a thread. This method is used in django as well.
            os._exit(1)

    def handle(self, *args, **options):
        # We're subclassing runserver, which spawns threads for its
        # autoreloader with RUN_MAIN set to true, we have to check for
        # this to avoid running grunt twice.
        if not os.getenv('RUN_MAIN', False):
            pool = ThreadPoolExecutor(max_workers=1)

            grunt_thread = pool.submit(self.start_grunt)
            grunt_thread.add_done_callback(self.grunt_exited_cb)

        return super(Command, self).handle(*args, **options)

    def kill_grunt_process(self):
        if self.grunt_process.returncode is not None:
            return

        self.cleanup_closing = True
        self.stdout.write('>>> Closing grunt process')

        self.grunt_process.terminate()

    def start_grunt(self):
        self.stdout.write('>>> Starting grunt')

        grunt_command = 'node -e "require(\'grunt\').tasks([\'default\']);"'
        self.grunt_process = subprocess.Popen(
            [grunt_command],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr)

        if self.grunt_process.poll() is not None:
            raise CommandError('grunt failed to start')

        self.stdout.write('>>> grunt process on pid {0}'
                          .format(self.grunt_process.pid))

        atexit.register(self.kill_grunt_process)

        self.grunt_process.wait()

        if self.grunt_process.returncode != 0 and not self.cleanup_closing:
            raise CommandError('grunt exited unexpectedly')
