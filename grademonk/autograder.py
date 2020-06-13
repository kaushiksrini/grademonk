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
        self.tests = []

        # set time string
        time_string = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        self.state_string = 'Graded %s by autograder v%s on %s' % (
            time_string, self.CONFIG['settings']['version'], platform.node())

    @staticmethod
    def get_autograder_status():
        return self.autograder

    def create_folders(self):
        folders = self.CONFIG["settings"]["foldersReq"]

        # create the folders
        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def run(self):
        initial_time = time.time()

        self.create_folders()

        # mount the autograder
        if self.autograder:
            os.chdir('/autograder/submission')
        else:
            os.chdir(self.CONFIG["settings"]["locationMount"])

        # run each class test
        classes = self.CONFIG["test"]["tests"]
        groupTests = self.CONFIG["settings"]["groupTests"] if "groupTests" in self.CONFIG["settings"] else False

        for cl in classes:
            val = cl.run(group=groupTests)
            self.tests.extend(val)
        # print(self.tests)

        # 3 do something with the tests
        self.generate_results(initial_time)

    def generate_results(self, init_time):
        import json
        from operator import itemgetter

        tot_score = sum(map(itemgetter('score'), self.tests))
        max_score = sum(map(itemgetter('max_score'), self.tests))

        # generating results
        json_out = json.dumps({
            'score': tot_score,
            'max_score': max_score,
            'execution_time': time.time() - init_time,
            'output': self.state_string,
            'tests': self.tests
        }, indent=4, sort_keys=True)

        if self.autograder:
            with open('/autograder/results/results.json', 'w') as ofh:
                ofh.write(json_out + '\n')

        else:
            json_print = json.loads(json_out)

            for test in json_print['tests']:
                print("=================================")
                print("TEST NAME: %s, SCORE: %.02f/%.02f" %
                      (test["name"], test["score"], test["max_score"]))
                print("OUTPUT: %s" % test["output"])
