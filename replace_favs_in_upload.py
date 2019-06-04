import glob
import re
import shutil
import datetime
import codecs
import os
import xml.dom.minidom as md
import xml.etree.ElementTree as et
from pathlib import Path

i = 0

for path in glob.glob("/Users/okada-toshiki/Library/Preferences/StepMania 5/Upload/*.xml"):
    f = open(path)
    lines = f.readlines()

    dirname = ''

    for line in lines:
        # print(line, end='')
        if 'Song Dir=' in line and '00fav' in line:
            dirname = re.match("(.*?)Songs(.*?)[^\']+", line).group()[23:]
            # print(dirname)


        for sl in glob.glob("../Songs/*/*"):
            if "00fav" not in line or dirname == '':
                continue
            if dirname in sl + "/":
                line = "<Song Dir='" + sl[3:] + "/'/>\n"
                
        print(line, file=codecs.open("/Users/okada-toshiki/Library/Preferences/StepMania 5/Upload_new/" + os.path.basename(path), 'a', 'utf-8'), end='')
    i += 1
    print(i)