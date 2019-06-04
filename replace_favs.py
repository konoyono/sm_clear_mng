import glob
import re
import shutil
import datetime
import codecs
import os
import xml.dom.minidom as md
import xml.etree.ElementTree as et
from pathlib import Path

stats_src = "/Users/okada-toshiki/Library/Preferences/StepMania 5/MachineProfile/Stats.xml"
stats_dst = "../Stats/stats_{0:%m%d}_machine.xml".format(datetime.datetime.now())
shutil.copyfile(stats_src, stats_dst)

stats = open(stats_dst)
st_lines = stats.readlines()
# root = et.fromstring(stats.read())
dirname = ""

for st_line in st_lines:
    if "&amp;" in st_line:
        st_line = st_line.replace("&amp;", "&")
    if 'Song Dir=' in st_line and '00fav' in st_line and '/>' not in st_line:
        dirname = re.match("(.*?)Songs(.*?)[^\"]+", st_line).group()[23:]

        for sl in glob.glob("../Songs/*/*"):
            if "00fav" in sl:
                continue
            if dirname in sl + "/":
                st_line = "<Song Dir='" + sl[3:] + "/'>"
    print(st_line, file=codecs.open("../Stats/replaced_stats_machine.xml", 'a', 'utf-8'), end='')