from .utils import run_subprocess


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
    def __init__(self, target, test_name, arguments, tester, return_value=0):
        self.target = target
        self.test_name = test_name
        self.arguments = arguments
        self.tester = tester
        self.return_value = self.return_value

    def run(self):
        # get the argument
        # run the code

        # get the output
        # Diff Test
        # if diff test, then compare the outputt file and expected file in a certain way.
        # Unit Test
        # check if the return value is

        msg = ''
        cmd = './%s %s' % (self.target, self.arguments.getArg())
        out, err, return_code, isKilled = run_subprocess(cmd)

        #
        # msg += self.tester.generate_msg(out, err, return_code)

        if return_code != self.return_value:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d]\n' % (
                self.target, return_code, self.return_value)

        if len(msg) > 0:
            return msg

        return 'PASS - Test \"%s\" passed successfully' % (self.test_name)


class ArgumentArray(object):
    def __init__(self, text='', arg_type='', autograder_mount='', local_mount=''):
        self.text = text
        self.arg_type = arg_type
        self.autograder_mount = autograder_mount
        self.local_mount = local_mount

    def getArg(self):
        return self.text


class Argument(object):
    def __init__(self, arg, arg_type):
        self.arg = arg
        self.arg_type = arg_type


class DiffTester(object):
    def __init__(self):
        self.
