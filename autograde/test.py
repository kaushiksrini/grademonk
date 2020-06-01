class TestGroup(object):
    def __init__(self, group_name, tests, visibility='visible', max_score=0.01, valgrind=False):
        self.group_name = group_name
        self.tests = tests
        self.visibility = visibility
        self.max_score = max_score
        self.valgrind = valgrind

    def run(self):
        for test in self.tests:
            msg = test.run()


class TestRunner(object):
    def __init__(self, target, test_name, input, output):
        self.test_name = test_name

    def run(self):
        pass
