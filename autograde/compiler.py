import os
from .utils import run_subprocess, wrap, make_test_obj


class TestCompileFiles(object):
    def __init__(self, targets, name='File Compiles', visibility='visible', max_score=0.01, gcc_args='-std=c99 -Wall -Wextra -pedantic -lm'):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.targets = targets
        self.gcc_args = gcc_args

    def compile(self):
        msg = ''
        for file in self.targets:
            if not os.path.exists(file + '.c'):
                msg += 'FAIL -- "%s.c" does not exist\n' % file
                continue
            if os.path.exists(m):
                msg += 'FAIL -- "%s" binary already exists\n' % file
                continue

            out, err, return_code, _ = run_subprocess(
                'gcc -o %s %s.c %s' % (file, file, self.gcc_args))

            if return_code != 0:
                msg += ('FAIL -- "%s.c" failed to compile; gcc returned %d\n\n'
                        % (file, return_code)) + wrap(out, err, file)
            elif len(err.strip()) > 0:
                msg += ('SUSPICIOUS -- "%s.c" compiled, but with warnings' %
                        file) + wrap(out, err, file)

        if len(msg) > 0:
            return msg, 0

        return ('PASS -- %s compile(s) without warnings or errors' % ', '.join(map(lambda x: x + '.c', self.targets))), self.max_score

    def run(self):
        msg, score = self.compile()
        return make_test_obj(score, self.name, self.max_score, msg, self.visibility)


class TestCleanBinaries(object):
    def __init__(self, targets, name='Delete Existing Binaries', visibility='visible', max_score=0.01):
        self.name = name
        self.visibility = visibility
        self.max_score = max_score
        self.targets = targets

    def clean_executables(self):
        files_removed = []
        for file in self.targets:
            if os.path.exists(file):
                os.remove(file)
                files_removed.append(file)

        if files_removed:
            return ('PASS -- %s binaries removed.' % (", ".join(files_removed))), self.max_score
        else:
            return ('PASS -- no binaries needed to be removed'), self.max_score

    def run(self):
        msg, score = self.clean_executables()
        return make_test_obj(score, self.name, self.max_score, msg, self.visibility)
