class DigestDirNotWritable:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Digest directory path '" + self.path + "' is not writable or is not a directory."


class MeditationException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
