from pycaption import SRTWriter, WebVTTReader
import os
import glob

def convert_vtt_to_srt(dir):
    for vtt_file in glob.glob(os.path.join(dir, "*.vtt")):
        with open(os.path.splitext(vtt_file)[0] + '.srt', 'w') as srt:
            vtt = open(vtt_file, 'r')
            vttsub = vtt.read().decode('UTF-8')
            srtsub = SRTWriter().write(WebVTTReader().read(vttsub))
            srt.write(srtsub.encode('UTF-8'))
            vtt.close()
            os.remove(vtt_file)