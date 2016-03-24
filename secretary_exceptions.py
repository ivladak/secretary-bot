class DigestDirNotWritable:
    def __init__(self, path):
        self.path = path
    def __str__(self):
        return "Digest directory path '" + path + "' is not writable or is not a directory."
