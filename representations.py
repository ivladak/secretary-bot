from time import ctime
from subprocess import call

def escape(text):
    esc = [ "\u2014", "=", "-", "`", ":", "'", '"', "~", "^", "_", "*", "+", "#", "<", ">" ]
    for i in esc:
        text = text.replace(i, "\\" + i)
    return text

class rest_builder:
    """A rudimentary reStructuredText builder."""
    def __init__(self):
        self._body = ""

    def title(self, text, underline="======"):
        self._body += "\n" + escape(text)  + "\n" + underline + "\n"

    def subtitle (self, text):
        self.title(text, "------")

    def item(self, text):
        self._body += "- " + escape(text.replace("\n", "\n  ")) + "\n"

    def tofile(self, filename):
        f = open(filename, "w")
        f.write(self._body.encode('utf-8'))
        f.close()


def write_rest(classes, digest_filename):
    time = ctime().split()
    del time[-2] # Don't really need the time, we want to highlight only the date.

    rest = rest_builder()

    rest.title("Digest for " + " ".join(time))
    for cls in classes:
        rest.subtitle(cls + ":")
        for item in classes[cls]:
            rest.item(item)

    rest.tofile(digest_filename)


def write_pdf(rest_fname, out_fname):
    args = ["rst2pdf", rest_fname, "-s", "non-latin.style", "-o", out_fname]
    call(args)
