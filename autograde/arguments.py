from .utils import get_file_path


class ArgumentArray(object):
    def __init__(self, io=False, cla=[], file=''):
        self.cla = cla
        self.io = io
        self.file = file

    def read_label(self):
        pass

    def getArg(self):
        cmd = ''
        for c in self.cla:
            if isinstance(c, FileArgument):
                cmd += '%s ' % (c.get_mount())
            else:
                cmd += '%s ' % c

        if self.io:
            if isinstance(self.file, str):
                return '%s < %s > %s' % (cmd, get_file_path('input', self.file),
                                         get_file_path('output', self.file))
            elif isinstance(self.file, FileArgument):
                return '%s < %s > %s' % (cmd, self.file.get_mount('input'),
                                         self.file.get_mount('output'))
        else:
            return cmd


class Argument(object):
    def __init__(self, arg, arg_type):
        self.arg = arg
        self.arg_type = arg_type


class FileArgument(object):
    def __init__(self, folder='', file=''):
        self.folder = folder
        self.file = file

    def get_mount(self, folder=''):
        if folder:
            return '../%s/%s' % (folder, self.file)
        else:
            return '../%s/%s' % (self.folder, self.file)
