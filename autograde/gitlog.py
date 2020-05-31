import os
from .utils import make_test_obj


class TestGitlog(object):

    def __init__(self, name='Gitlog is Well-Formed', visibility='visible', max_score=0.01, minimum_commits=4):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.minimum_commits = minimum_commits

    def check_gitlog(self):
        return ''

    def run(self):
        if not os.path.exists('gitlog.txt'):
            msg = 'FAIL -- \'gitlog.txt\' does not exist'
        else:
            msg = self.check_gitlog()

        if msg.startswith('FAIL'):
            return make_test_obj(0, self.name, self.max_score, msg, self.visibility)
        else:
            return make_test_obj(self.max_score, self.name, self.max_score, msg, self.visibility)


class TestGitlogFormat(TestGitlog):
    def __init__(self, name='Gitlog is Well-Formed', visibility='visible', max_score=0.01, minimum_commits=4):
        TestGitlog.__init__(self, name=name, visibility=visibility,
                            max_score=max_score, minimum_commits=minimum_commits)

    def check_gitlog(self):
        import re
        with open('gitlog.txt') as fh:
            data = fh.read()

        commits = re.findall(
            r"commit .{40}\n(Merge: .* .*\n|)Author: .*\nDate:   \w{3} \w{3} \d{1,2} \d\d:\d\d:\d\d \d{4} -\d{4}", data)
        if len(commits) <= self.minimum_commits:
            return 'FAIL -- \'gitlog.txt\' is malformed or has less than %d commits recorded' % (self.minimum_commits)

        return 'PASS -- \'gitlog.txt\' exists and is well formed\n'


class TestGitlogContributions(TestGitlog):
    def __init__(self, name='Gitlog - Equal Contribution', visibility='hidden', max_score=0.01, minimum_commits=8):
        TestGitlog.__init__(self, name=name, visibility=visibility,
                            max_score=max_score, minimum_commits=minimum_commits)

    def check_gitlog(self):
        import re
        with open('gitlog.txt') as fh:
            data = fh.read()

        authors = re.findall("<.*>", data)
        counts = {name: authors.count(name) for name in set(authors)}
        author_str = ''
        moreThanX = True

        for name, count in counts.items():
            if count < self.minimum_commits:
                moreThanX = False
            author_str += '%s: %d commits\n' % (name, count)

        if not moreThanX:
            return 'FAIL -- in \' gitlog.txt \' a student does not have more than 10 git commits\n' + author_str
        else:
            return 'PASS -- in \'gitlog.txt\' all students have atleast 10 git commits\n' + author_str

        return False
