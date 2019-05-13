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
RANGE_NAME_CR = 'クリア率!B27'
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
parser.add_argument('clear_ratio', nargs='?', type=argparse.FileType('r'),
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


# クリア率の自動更新は一旦保留
# cr = csv.reader(args.clear_ratio, delimiter = '\t')
# cr_data = list(cr)
# cr_body = {
#     "range": RANGE_NAME_CR,
#     "majorDimension": MAJOR_DIMENSION,
#     "values": cr_data
# }
# resource.update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_CR,
#                 valueInputOption='USER_ENTERED', body=cr_body).execute()