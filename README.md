# Grademonk

A Gradescope customized autograder for C/C++ programming. Used at Johns Hopkins University's core Computer Science course 601.220 - Intermediate Programming.

## Usage

The documentation is far from complete for this repo: it's still a work in progress.

### Structure

There are multiple subclasses each of which run a specific test.

- `autograder.py` - contains the main Autograder class that runs all tthe tests and outputs it to the appropriate file. This is the main driver program.
- `files.py` - contains classes to test whether files exist, (required files exist and not required files do not exist).
- `tree.py` - prints a tree of all the submitted files (usually no autograder points)
- `compiler.py` - contains classes to compile files. Students switch to using Makefiles early in the course.
- `make.py` - For Makefiles. Can run multiple target commands.
- `tests.py` - the main test suite for the program. Contains multiple submodules to assist running the full tests.
  - `arguments.py` - contains a class that helps create the command line argument. It also is modified so that the command line argument can work both locally and in the autograder.
  - `controller.py` - contains a class that verifies the output - checks expected files or return values.
- `utils.py` - this contails extra utility functions that help in various stages of the program.
