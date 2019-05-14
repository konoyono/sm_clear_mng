## StepMania クリア管理用スクリプト

### analyse_stats.py
- ローカルに保存されている曲難易度や統計情報を解析し、TSVとして出力するスクリプト

### tsv_upload.tsv
- 解析後、出力されたTSVファイルを Gspread にアップロードするスクリプト

### launch_sm_and_scripts.py
- ステップマニア本体と上記のスクリプト郡を同時起動するためのラッパー
- 統計情報ファイルへの変更を watchdog で検出し、上記のスクリプトを走らせる
- ステップマニア本体終了時にこのスクリプトも自動終了する

## クリア管理のエクセルは[これ](https://docs.google.com/spreadsheets/d/1IbQuBNPa6jWRpgO-MQr56SUExnU5qc-WHzmz2tNcq8k/edit#gid=0)