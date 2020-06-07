from .utils import run_subprocess, make_test_obj, get_file_path
import os


class TestGroup(object):
    def __init__(self, group_name, tests, visibility='visible', max_score=0.01, valgrind=False):
        self.group_name = group_name
        self.tests = tests
        self.visibility = visibility
        self.max_score = max_score
        self.valgrind = valgrind

    def run(self, group=False):

        failed_msg = ""
        secondary_msg = ""
        result = []

        for test in self.tests:
            msg = test.run()
            if not group:
                score = 0 if msg.startswith('FAIL') else self.max_score
                result.extend(make_test_obj(score, self.group_name,
                                            self.max_score, msg, self.visibility))
            else:
                if msg.startswith('FAIL'):
                    failed_msg += msg
                else:
                    secondary_msg += msg

        if not group:
            return result
        else:
            full_msg = failed_msg + secondary_msg
            score = 0 if len(failed_msg) > 0 else self.max_score
            return make_test_obj(score, self.group_name, self.max_score, full_msg, self.visibility)


class TestRunner(object):
    def __init__(self, target, test_name, arguments, tester, return_value=0, timeout=300):
        self.target = target
        self.test_name = test_name
        self.arguments = arguments
        self.tester = tester
        self.return_value = return_value
        self.timeout = timeout

    def run(self):
        # get the argument
        # run the code

        # get the output
        # Diff Test
        # if diff test, then compare the outputt file and expected file in a certain way.
        # Unit Test
        # check if the return value is

        if not os.path.exists(self.target):
            return 'FAIL -- executable "%s" did not compile or was not found\n' % self.target

        msg = ''
        cmd = './%s %s' % (self.target, self.arguments.getArg())

        out, err, return_code, isKilled = run_subprocess(
            cmd, timeout=self.timeout)

        if isKilled:
            return 'FAIL -- Test \" %s \" took longer than %d seconds to run.\n' % (self.test_name, self.timeout)

        msg += self.tester.generate_msg(self.test_name,
                                        self.target, out, err, return_code)

        if len(msg) > 0:
            return msg

        return 'PASS - Test \"%s\" passed successfully\n' % (self.test_name)
