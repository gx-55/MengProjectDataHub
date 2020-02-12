import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

def googleSheetClient():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('MengProject-738c2d7e4cb5.json', scope)
    client = gspread.authorize(creds)
    return client