from .utils import wrap_message, get_file_path
import difflib
from .arguments import FileArgument


class TestController(object):
    def __init__(self):
        pass

    def get_file_diff(self, test_name, file1, file2, is_bytes=False):
        msg = ''
        diffOut = ''

        if is_bytes:
            expectedLines = open(file1, "rb").readlines()
            outputLines = open(file2, "rb").readlines()

            for line in difflib.diff_bytes(difflib.unified_diff, expectedLines, outputLines):
                diffOut += line
        else:
            expectedLines = open(file1).readlines()
            outputLines = open(file2).readlines()

            for line in difflib.unified_diff(expectedLines, outputLines):
                diffOut += line

        if len(diffOut) > 0:
            msg += ('FAIL -- Test %s has different ouput than expected' %
                    (test_name))

            msg += (wrap_message(''.join(expectedLines),
                                 test_name + ' Expected Lines'))
            msg += (wrap_message(''.join(outputLines),
                                 test_name + ' Output Lines'))

        return msg


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


class DiffExpectedFileTester(TestController):
    def __init__(self, file_name='', return_value=0, is_bytes=False):
        self.file_name = file_name
        self.return_value = return_value
        self.is_bytes = is_bytes

    def generate_msg(self, test_name, target, out, err, return_code):
        msg = ''
        if return_code != self.return_value:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d].\n' % (
                target, return_code, self.return_value)

        msg += self.get_file_diff(test_name, get_file_path(
            "expected", self.file_name), get_file_path("output", self.file_name), self.is_bytes)

        if len(msg) > 0:
            return msg

        return ''


class ReturnValueController(TestController):
    def __init__(self, return_value=0, non_zero=False, output_file=''):
        self.return_value = return_value
        self.non_zero = non_zero
        self.output_file = output_file

    def generate_msg(self, test_name, target, out, err, return_code):
        msg = ''
        if self.non_zero and return_code == 0:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of a non-zero value.\n' % (
                target, return_code)
        elif not self.non_zero and self.return_value != return_code:
            msg += 'FAIL (RETURN CODE) -- "%s" compiled successfully but returned [%d] when run instead of [%d].\n' % (
                target, return_code, self.return_value)

        if self.output_file:
            if isinstance(self.output_file, str):
                msg += self.get_file_diff(test_name, get_file_path(
                    "expected", self.output_file), get_file_path("output", self.output_file))

            if isinstance(self.output_file, FileArgument):
                msg += self.get_file_diff(test_name, self.output_file.get_mount(
                    folder='expected'), self.output_file.get_mount(folder='output'))

        if len(msg) > 0:
            return msg

        return ''
