from .utils import wrap_message, get_file_path
import difflib


class TestController(object):
    def __init__(self):
        pass


class DiffTester(object):
    def __init__(self, text='', return_value=0, file_name=''):
        self.text = text
        self.return_value = return_value
        self.file_name = file_name

    def generate_msg(self, target, out, err, return_code):
        msg = ''
        if return_code != self.return_value:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d].\n' % (
                target, return_code, self.return_value)

        if isinstance(self.text, str):
            if out != self.text:
                msg += 'FAIL -- Test ran but produced incorrect output\n' + wrap_message(self.text, target + ' expected') + wrap_message(out, target + ' output') + \
                    wrap_message(err, target + ' error')

        return msg


class DiffExpectedFileTester(object):
    def __init__(self, file_name='', return_value=0):
        self.file_name = file_name
        self.return_value = return_value

    def generate_msg(self, test_name, target, out, err, return_code):
        msg = ''
        if return_code != self.return_value:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d].\n' % (
                target, return_code, self.return_value)

        expectedLines = open(get_file_path(
            "expected", self.file_name)).readlines()
        outputLines = open(get_file_path("output", self.file_name)).readlines()

        diffOut = ''

        for line in difflib.unified_diff(expectedLines, outputLines):
            diffOut += line

        if len(diffOut) > 0:
            msg += ('FAIL -- Test %s has different ouput than expected' %
                    (test_name))

            msg += (wrap_message(''.join(expectedLines),
                                 test_name + ' Expected Lines'))
            msg += (wrap_message(''.join(outputLines),
                                 test_name + ' Output Lines'))

        if len(msg) > 0:
            return msg

        return ''

    # now check whether the files are the same


class ReturnValueController(object):
    def __init__(self, return_value=0, non_zero=False):
        self.return_value = return_value
        self.non_zero = non_zero

    def generate_msg(self, test_name, target, out, err, return_code):
        msg = ''
        if self.non_zero and return_code == 0:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of a non-zero value.\n' % (
                target, return_code)
        elif self.return_value != return_code:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d].\n' % (
                target, return_code, self.return_value)

        if len(msg) > 0:
            return msg

        return ''
