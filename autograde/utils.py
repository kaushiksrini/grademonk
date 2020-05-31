import os
import subprocess
from threading import Timer, Event
import signal


def make_test_obj(score, name, max_score, output, visibility, tags=''):
    return {
        "score": score,
        "name": name,
        "max_score": max_score,
        "output": output,
        "tags": tags,
        "visibility": visibility
    }

# Subprocess communicate with a timeout
# Returns the output, error, and the return code


def communicate(p, test_input=None, timeout=None):
    if timeout is None or timeout == 0:
        out, err = p.communicate(input=test_input)
        return out, err, p.returncode, False

    had_to_kill = Event()

    def kill(p):
        had_to_kill.set()
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)

    timer = Timer(timeout, kill, [p])
    out, err = None, None

    try:
        timer.start()
        out, err = p.communicate(input=test_input)
    finally:
        timer.cancel()
        if had_to_kill.isSet():
            return None, None, -1, True
        return out, err, p.returncode, False


# Run the given command
# Returns the output, error, return code, and whether or not it was killed


def run_subprocess(cmd, test_input=None, timeout=None):
    p = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return communicate(p, test_input, timeout)


# Wrap a given message for cleaner output
def wrap(out, err, name):
    return wrap_message(out, name + ' output') + wrap_message(err, name + ' output')


def wrap_message(msg, name):
    if msg and len(msg.strip()) > 0:
        return '\n=== begin %s ===\n%s\n=== end %s ===\n\n' % \
               (name, msg.strip(), name)
    return ''
