import os
from .utils import run_subprocess, make_test_obj


class TreeSubmission(object):
    def __init__(self, name='List Submission Files', visibility='visible', max_score=0.01):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score

    def tree_cmd(self):
        if os.system('tree >/dev/null 2>/dev/null') == 0:
            return 'tree'
        else:
            return "find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'"

    def run(self):
        out, _, _, _ = run_subprocess(self.tree_cmd())
        msg = 'Extracted submission files:\n' + out.decode()
        return make_test_obj(self.max_score, self.name, self.max_score, msg, visibility=self.visibility)
