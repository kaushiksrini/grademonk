import datetime
import time
import platform


class Autograder(object):
    def __init__(self, CONFIG=None):
        self.CONFIG = CONFIG

    def run(self):
        initial_time = time.time()
        time_string = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        state_string = 'Graded %s by autograder v%s on %s' % (
            time_string, self.CONFIG['settings']['version'], platform.node())

        if self.CONFIG['settings']['autograder']:
            os.chdir('/autograder/submission')
