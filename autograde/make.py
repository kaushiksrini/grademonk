from .utils import make_test_obj, run_subprocess, wrap_message
import time


class TestMakeCommand(object):
    def __init__(self, target, name, visibility='visible', max_score=0.01):
        self.target = target
        self.name = name
        self.visibility = visibility
        self.max_score = max_score

    def run_cmd(self, cmd):
        out, err, return_code, _ = run_subprocess(cmd)

        if return_code != 0:
            msg = ('FAIL -- "make %s" failed; make returned %d\n\n'
                   % (self.target, return_code)) + \
                wrap_message(out, 'make output') + \
                wrap_message(err, 'make error')
            return make_test_obj(0, self.name, self.max_score, msg, self.visibility)
        elif err != None and len(err.strip()) > 0:
            msg = ('SUSPICIOUS -- "make %s" returned 0, but printed warnings' % self.target) + \
                wrap_message(out, 'make output') + \
                wrap_message(err, 'make error')
            return make_test_obj(0, self.name, self.max_score, msg, self.visibility)
        time.sleep(1)

        msg = 'PASS -- "make %s" succeeded without warnings or errors\n Output:\n %s' % (
            self.target, out)

        return msg

    def run(self):
        msg = ''

        if isinstance(self.target, str):
            cmd = 'make %s' % self.target
            msg = self.run_cmd(cmd)
        elif isinstance(self.target, list):
            for target in self.target:
                cmd = 'make %s' % target
                msg += self.run_cmd(cmd)

        return make_test_obj(self.max_score, self.name, self.max_score, msg, self.visibility)


class TestMakeClean(TestMakeCommand):
    def __init__(self, target='clean', name='Make Clean', visibility='visible', max_score=0.01):
        TestMakeCommand.__init__(
            self, target, name=name, visibility=visibility, max_score=max_score)


class TestMakeFiles(TestMakeCommand):
    def __init__(self, targets, name='Make Files', visibility='visible', max_score=0.01):
        TestMakeCommand.__init__(
            self, targets, name=name, visibility=visibility, max_score=max_score)
