import os
from .utils import make_test_obj


class TestRequiredFiles(object):
    def __init__(self, expected_files, name='Required Files Found', visibility='visible', max_score=0.01):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.expected_files = expected_files

    def get_msg(self):
        msg = ''
        for f in self.expected_files:
            if not os.path.exists(f):
                msg += 'FAIL -- "%s" not found\n' % f

        if len(msg) == 0:
            return 'PASS -- All required files found', self.max_score
        return msg, 0

    def run(self):
        msg, score = self.get_msg()
        return make_test_obj(score, self.name, self.max_score, msg, self.visibility)
