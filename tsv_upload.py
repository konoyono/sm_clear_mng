#!/usr/bin/env python
# coding:utf-8
from apiclient import discovery
import oauth2client
from oauth2client import file
from oauth2client import tools
import httplib2
import argparse
import csv
import sys
 
SPREADSHEET_ID = '1IbQuBNPa6jWRpgO-MQr56SUExnU5qc-WHzmz2tNcq8k'
RANGE_NAME_RT = 'メインシート!A2'
RANGE_NAME_NC = '未クリア曲!A2'
RANGE_NAME_INIT = '未クリア曲!A2:D500'
MAJOR_DIMENSION = 'ROWS'
 
CLIENT_SECRET_FILE = '/Users/okada-toshiki/Downloads/client_secret_596362052363-ag8g6o8ufmi9ao3l6vt3cuig0blcugj4.apps.googleusercontent.com.json'
CREDENTIAL_FILE = "./credential.json"
APPLICATION_NAME = 'TSV Appender'
 
store = oauth2client.file.Storage(CREDENTIAL_FILE)
credentials = store.get()
if not credentials or credentials.invalid:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())
    credentials = oauth2client.tools.run_flow(flow, store, flags)
 
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
resource = service.spreadsheets().values()
 
parser = argparse.ArgumentParser()
parser.add_argument('result_table', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
parser.add_argument('not_cleared', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
args = parser.parse_args(sys.argv[1:])
 
rt = csv.reader(args.result_table, delimiter = '\t')
rt_data = list(rt) 
rt_body = {
    "range": RANGE_NAME_RT,
    "majorDimension": MAJOR_DIMENSION,
    "values": rt_data
}
resource.update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_RT,
                valueInputOption='USER_ENTERED', body=rt_body).execute()

init_data = list()
# 既に存在するデータ数ぶんだけ初期化要素を append
data = resource.get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_INIT).execute()
for i in range(len(data["values"])):
    init_data.append([" "," "," "," "])

init_body = {
    "range": RANGE_NAME_INIT,
    "majorDimension": MAJOR_DIMENSION,
    "values": init_data
}
resource.update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_INIT,
                valueInputOption='USER_ENTERED', body=init_body).execute()

nc = csv.reader(args.not_cleared, delimiter = '\t')
nc_data = sorted(list(nc), key=lambda x: int(x[0]))

nc_body = {
    "range": RANGE_NAME_NC,
    "majorDimension": MAJOR_DIMENSION,
    "values": nc_data
}
resource.update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_NC,
                valueInputOption='USER_ENTERED', body=nc_body).execute()