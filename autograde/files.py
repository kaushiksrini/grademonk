import os
from .utils import make_test_obj


class TestFiles(object):
    def __init__(self, expected_files, name='Required Files Found', visibility='visible', max_score=0.01):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.expected_files = expected_files

    def get_msg(self):
        return '', 0

    def run(self):
        msg, score = self.get_msg()
        return make_test_obj(score, self.name, self.max_score, msg, self.visibility)


class TestRequiredFiles(TestFiles):
    def __init__(self, expected_files, name='Required Files Found', visibility='visible', max_score=0.01):
        TestFiles.__init__(self, expected_files=expected_files,
                           name=name, visibility=visibility, max_score=max_score)

    def get_msg(self):
        msg = ''
        for f in self.expected_files:
            if not os.path.exists(f):
                msg += 'FAIL -- "%s" not found\n' % f

        if len(msg) == 0:
            return 'PASS -- All required files found', self.max_score
        return msg, 0


class TestUnexpectedFiles(TestFiles):
    def __init__(self, expected_files, name='Required Files Found', visibility='visible', max_score=0.01):
        TestFiles.__init__(self, expected_files=expected_files,
                           name=name, visibility=visibility, max_score=max_score)

    def run(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for fn in self.expected_files:
            if fn in files:
                files.remove(fn)
                assert fn not in files
        if len(files) > 0:
            return 'FAIL -- Did not expect these files to be present: '\
                + str(files), 0
        return 'PASS -- No unexpected files found', self.max_score
