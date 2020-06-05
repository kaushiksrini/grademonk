from autograde.autograder import Autograder
from autograde.tree import TreeSubmission
from autograde.compiler import TestCompileFiles, TestCleanBinaries
from autograde.gitlog import TestGitlogFormat
from autograde.files import TestRequiredFiles, TestUnexpectedFiles
from autograde.tests import TestGroup, TestRunner, ArgumentArray
from autograde.controller import DiffTester

CONFIG = {
    "settings": {
        "autograder": True,
        "version": "0.1.0",
        "locationMount": "submission/",
        "foldersReq": ["input", "output", "expected"]
    },
    "test": {
        "tests": [
            TreeSubmission(),
            TestGitlogFormat(),
            TestRequiredFiles(['one.c']),
            TestCleanBinaries(['one']),
            TestCompileFiles(targets=['one']),
            TestGroup("Equality", [
                TestRunner(
                    target='one',
                    test_name='Check Equality',
                    arguments=ArgumentArray(),
                    tester=DiffTester('Testing 123')
                ),
                TestRunner(
                    target='one',
                    test_name='Check Equality',
                    arguments=ArgumentArray(),
                    tester=DiffTester('Testing 1234')
                )
            ])
        ]
    }

}

if __name__ == "__main__":
    Autograder(CONFIG, autograder=False).run()
