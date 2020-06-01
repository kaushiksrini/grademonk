import datetime
import time
import platform
import os


class Autograder(object):
    def __init__(self, CONFIG=None, autograder=''):
        self.CONFIG = CONFIG
        self.autograder = False
        if autograder:
            self.autograder = autograder
        elif os.environ.get('AM_I_IN_A_DOCKER_CONTAINER'):
            self.autograder = True

    def run(self):
        initial_time = time.time()
        time_string = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        state_string = 'Graded %s by autograder v%s on %s' % (
            time_string, self.CONFIG['settings']['version'], platform.node())

        if self.autograder:
            os.chdir('/autograder/submission')
        else:
            os.chdir(self.CONFIG["settings"]["locationMount"])

        classes = self.CONFIG["test"]["tests"]
        tests = []
        for cl in classes:
            val = cl.run()
            tests.append(val)
        print(tests)
