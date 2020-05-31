import os
from .utils import make_test_obj


class TestGitlog(object):
    def __init__(self, name='Gitlog is Well-Formed', visibility='visible', max_score=0.01):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.minimum_commits = 4

    def check_gitlog(self):
        import re
        with open('gitlog.txt') as fh:
            data = fh.read()

        commits = re.findall(
            r"commit .{40}\n(Merge: .* .*\n|)Author: .*\nDate:   \w{3} \w{3} \d{1,2} \d\d:\d\d:\d\d \d{4} -\d{4}", data)
        if len(commits) <= self.minimum_commits:
            return 'FAIL -- \'gitlog.txt\' is malformed or has less than %d commits recorded' % (self.minimum_commits)

        return 'PASS -- \'gitlog.txt\' exists and is well formed\n'

    def run(self):
        if not os.path.exists('gitlog.txt'):
            msg = 'FAIL -- \'gitlog.txt\' does not exist'
        else:
            msg = self.check_gitlog()

        if msg.startswith('FAIL'):
            return make_test_obj(0, self.name, self.max_score, msg, self.visibility)
        else:
            return make_test_obj(self.max_score, self.name, self.max_score, msg, self.visibility)
