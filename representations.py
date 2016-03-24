from html import HTML
from time import ctime

def write_html(classes, digest_filename):
    time = ctime().split()
    del time[-2] # Don't really need the time, we want to highlight only the date.
    h = HTML()
    h.h1("Digest for " + " ".join(time))
    for cls in classes:
        h.h2(cls + ":")
        unordered_list = h.ul
        for item in classes[cls]:
            unordered_list.li(item)
    f = open(digest_filename, "w")
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'.encode('utf-8'))
    f.write(h.__unicode__().encode('utf-8'))
    f.close()
