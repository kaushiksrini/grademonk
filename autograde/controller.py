from .utils import wrap_message


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
                msg += 'FAIL -- Test ran but produced incorrect output\n' + wrap_message(out, target + ' output') + \
                    wrap_message(err, target + ' error')

        return msg
