from autograde.autograder import Autograder
from autograde.tree import TreeSubmission
from autograde.compiler import TestCompileFiles, TestCleanBinaries
from autograde.gitlog import TestGitlogFormat
from autograde.files import TestRequiredFiles, TestUnexpectedFiles

CONFIG = {
    "settings": {
        "autograder": True,
        "version": "0.1.0",
        "locationMount": "submission/"
    },
    "test": {
        "tests": [
            TreeSubmission(),
            TestGitlogFormat(),
            TestRequiredFiles(['one.c']),
            TestCleanBinaries(['one']),
            TestCompileFiles(targets=['one']),
        ]
    }

}

if __name__ == "__main__":
    Autograder(CONFIG, autograder=False).run()
