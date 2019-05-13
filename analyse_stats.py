import glob
import re
import shutil
import datetime
import codecs
import os
import xml.dom.minidom as md
import xml.etree.ElementTree as et
from pathlib import Path

# ディレクトリ名の昇順でソート
sl = list()
for path in glob.glob("../Songs/00fav/*"):
    sl.append(path)
sl.sort(key=str.lower)

stats_src = "/Users/okada-toshiki/Library/Preferences/StepMania 5/LocalProfiles/00000000/Stats.xml"
stats_dst = "../Stats/stats_{0:%m%d}.xml".format(datetime.datetime.now())
shutil.copyfile(stats_src, stats_dst)

stats = open(stats_dst)
root = et.fromstring(stats.read())
doc = md.parseString(et.tostring(root, 'utf-8'))
st_lines = doc.toxml().split('\n')

try:
    os.remove("../Analysed/table_{0:%m%d}.tsv".format(datetime.datetime.now()))
    os.remove("../Analysed/clear_ratio_{0:%m%d}.tsv".format(datetime.datetime.now()))
except IOError:
    pass

clear_count = [0] * 8
total_count = [0] * 8
clear_count_raw = [0] * 18

def print_clear_ratio():
    for i in range(0, 8):
        print(str(total_count[i] - clear_count[i]) + 
            "\t" + str(clear_count[i]) + "\t" + str(total_count[i]),
            file=codecs.open("../Analysed/clear_ratio_{0:%m%d}.tsv".format(datetime.datetime.now()), 'a', 'utf-8'))

def format_clear_count():
    sum_u8 = 0
    sum_o15 = 0
    for i in range(0, 8):
        sum_u8 += clear_count_raw[i]
    clear_count[0] = sum_u8
    for i in range(8, 15):
        clear_count[i-7] = clear_count_raw[i]
    for i in range(15, 18):
        sum_o15 += clear_count_raw[i]
    clear_count[7] = sum_o15

def sum_clear_ratio(dif, res):
    for v in dif.values():
        try:
            if   int(v) <= 8:  total_count[0] += 1
            elif int(v) == 9:  total_count[1] += 1
            elif int(v) == 10: total_count[2] += 1
            elif int(v) == 11: total_count[3] += 1
            elif int(v) == 12: total_count[4] += 1
            elif int(v) == 13: total_count[5] += 1
            elif int(v) == 14: total_count[6] += 1
            elif int(v) >= 15: total_count[7] += 1
        except Exception:
            pass
    
    for i in range(1, 18):
        if dif["Beginner"] != "-" and int(dif["Beginner"]) == i and res["Beginner"] != "未" and res["Beginner"] != "F":
            clear_count_raw[i-1] += 1
        if dif["Easy"] != "-" and int(dif["Easy"]) == i and res["Easy"] != "未" and res["Easy"] != "F":
            clear_count_raw[i-1] += 1
        if dif["Medium"] != "-" and int(dif["Medium"]) == i and res["Medium"] != "未" and res["Medium"] != "F":
            clear_count_raw[i-1] += 1
        if dif["Hard"] != "-" and int(dif["Hard"]) == i and res["Hard"] != "未" and res["Hard"] != "F":
            clear_count_raw[i-1] += 1
        if dif["Challenge"] != "-" and int(dif["Challenge"]) == i and res["Challenge"] != "未" and res["Challenge"] != "F":
            clear_count_raw[i-1] += 1

def print_result_table(fcount, dict, dict_res):        
    print(fcount + "\t" + dict["title"] + "\t" 
        + dict["Beginner"] + "\t" + dict_res["Beginner"] + "\t"
        + dict["Easy"] + "\t" + dict_res["Easy"] + "\t"
        + dict["Medium"] + "\t" + dict_res["Medium"] + "\t"
        + dict["Hard"] + "\t" + dict_res["Hard"] + "\t"
        + dict["Challenge"] + "\t" + dict_res["Challenge"] + "\t" + dict["Next"],
        file=codecs.open("../Analysed/table_{0:%m%d}.tsv".format(datetime.datetime.now()), 'a', 'utf-8'))

def has_cleared_high_difficulty(difficulty, org):
    if difficulty != "未" and difficulty != "-" and difficulty != "F" and org == "未": return "--"
    else: return org

def convert_res(res_line):
    if   "Tier01" in res_line: return "AAA"
    elif "Tier02" in res_line: return "AA"
    elif "Tier03" in res_line: return "A"
    elif "Tier04" in res_line: return "B"
    elif "Tier05" in res_line: return "C"
    elif "Tier06" in res_line: return "D"
    elif "Tier07" in res_line: return "E"
    elif "Failed" in res_line: return "F"
    else: return "未"

def has_difficulty(difficulty, org):
    if difficulty == "-": return "-"
    else: return org

def judge_next_level(res):
    if res["Beginner"] == "未" or res["Beginner"] == "F": return "習"
    if res["Easy"] == "未" or res["Easy"] == "F": return "楽"
    if res["Medium"] == "未" or res["Medium"] == "F": return "踊"
    if res["Hard"] == "未" or res["Hard"] == "F": return "激"
    if res["Challenge"] == "未" or res["Challenge"] == "F": return "鬼"
    else: return "-"

fcount = 0
for smf in sl:
    for path in list(Path(smf).glob("*.sm")):
        with open(path) as f:
            fcount += 1
            smlines = f.readlines()
            smline_num = 0
            dict = {"dirname":"sample", "title":"sample", "Beginner":"-", "Easy":"-", "Medium":"-", "Hard":"-", "Challenge":"-", "Next":"-"}
            for smline in smlines:
                if '#TITLE:' in smline:
                    title = re.search(r"(?<=\:).+?(?=\;)", smline)
                    dict["title"] = title.group()
                    dict["dirname"] = smf[3:] + "/"
                if 'dance-single:' in smline:
                    if smlines[smline_num+2].rstrip(':\n').lstrip(' ') == "Beginner":
                        dict["Beginner"] = smlines[smline_num+3].rstrip(':\n').lstrip(' ')
                    elif smlines[smline_num+2].rstrip(':\n').lstrip(' ') == "Easy":
                        dict["Easy"] = smlines[smline_num+3].rstrip(':\n').lstrip(' ')
                    elif smlines[smline_num+2].rstrip(':\n').lstrip(' ') == "Medium":
                        dict["Medium"] = smlines[smline_num+3].rstrip(':\n').lstrip(' ')
                    elif smlines[smline_num+2].rstrip(':\n').lstrip(' ') == "Hard":
                        dict["Hard"] = smlines[smline_num+3].rstrip(':\n').lstrip(' ')
                    elif smlines[smline_num+2].rstrip(':\n').lstrip(' ') == "Challenge":
                        dict["Challenge"] = smlines[smline_num+3].rstrip(':\n').lstrip(' ')
                smline_num += 1

            stline_num = 0
            dict_res = {"dirname":"sample", "Beginner":"未", "Easy":"未", "Medium":"未", "Hard":"未", "Challenge":"未"}
            for st_line in st_lines:
                if "&amp;" in st_line:
                    st_line = st_line.replace("&amp;", "&")
                if 'Song Dir=' in st_line and dict["dirname"] in st_line and '/>' not in st_line:
                    dict_res["dirname"] = dict["dirname"]
                    stline_num_inner = stline_num
                    for st_line in st_lines[stline_num:]:
                        if 'Steps Difficulty="Beginner"' in st_line:
                            dict_res["Beginner"] = convert_res(st_lines[stline_num_inner+4])
                        elif 'Steps Difficulty="Easy"' in st_line:
                            dict_res["Easy"] = convert_res(st_lines[stline_num_inner+4])
                        elif 'Steps Difficulty="Medium"' in st_line:
                            dict_res["Medium"] = convert_res(st_lines[stline_num_inner+4])
                        elif 'Steps Difficulty="Hard"' in st_line:
                            dict_res["Hard"] = convert_res(st_lines[stline_num_inner+4])
                        elif 'Steps Difficulty="Challenge"' in st_line:
                            dict_res["Challenge"] = convert_res(st_lines[stline_num_inner+4])
                        if "</Song>" in st_line:
                            break
                        stline_num_inner += 1
                stline_num += 1

            # そもそもその難易度が存在しなければ　"-" とする
            dict_res["Beginner"] = has_difficulty(dict["Beginner"], dict_res["Beginner"])
            dict_res["Easy"] = has_difficulty(dict["Easy"], dict_res["Easy"])
            dict_res["Medium"] = has_difficulty(dict["Medium"], dict_res["Medium"])
            dict_res["Hard"] = has_difficulty(dict["Hard"], dict_res["Hard"])
            dict_res["Challenge"] = has_difficulty(dict["Challenge"], dict_res["Challenge"])

            # 上の難易度をクリアしていれば、それ以下の難易度は "--" とする
            dict_res["Hard"] = has_cleared_high_difficulty(dict_res["Challenge"], dict_res["Hard"])
            dict_res["Medium"] = has_cleared_high_difficulty(dict_res["Hard"], dict_res["Medium"])
            dict_res["Easy"] = has_cleared_high_difficulty(dict_res["Medium"], dict_res["Easy"])
            dict_res["Beginner"] = has_cleared_high_difficulty(dict_res["Easy"], dict_res["Beginner"])

            # 次に挑戦すべきレベルを判定
            dict["Next"] = judge_next_level(dict_res)

            # 結果をまとめたテーブルを出力
            print_result_table(str(fcount), dict, dict_res)

            sum_clear_ratio(dict, dict_res)

format_clear_count()
print_clear_ratio()