from subprocess import getoutput
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import subprocess
import schedule
import time
import os
import datetime
    
# StepMania 本体を起動
getoutput("open /Users/okada-toshiki/Desktop/StepMania-5.0.12/StepMania.app")

target_dir = "/Users/okada-toshiki/Library/Preferences/StepMania 5/LocalProfiles/00000000"
target_file = "*.xml*"

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super(FileChangeHandler, self).__init__(patterns=patterns)

    def on_moved(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        subprocess.call(["python3", "analyse_stats.py"])
        subprocess.call(["python3", "tsv_upload.py", 
            "../Analysed/table_{0:%m%d}.tsv".format(datetime.datetime.now()), 
            "../Analysed/not_cleared_{0:%m%d}.tsv".format(datetime.datetime.now())])
        print('%s moved' % filename)

# コマンド実行の確認
if __name__ == "__main__":
    event_handler = FileChangeHandler([target_file])
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()

    while True:
        time.sleep(1)
        # StepMania　本体終了時にループ抜ける
        if getoutput("pgrep Step") == "":
            break
    observer.stop()
    observer.join()