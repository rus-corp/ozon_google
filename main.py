from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.





class GoogleSheet:
    SAMPLE_SPREADSHEET_ID = '12Dpdg_OEQCrWNcMP977-tfhFUX69eHRM7pP_FblMNCk'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_RANGE_NAME = 'Data!A2:AV9'    
    service = None
    
    def __init__(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('creds.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('sheets', 'v4', credentials=creds)


    def read_values(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        return values
    
    
    def write_values(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, body=body).execute()
        return result
        






def main():
    g = GoogleSheet()
    test_range = 'A4:B6'
    test_data = [
        [1, 2],
        [4, 5],
        [8, 9]
    ]
    g.write_values(test_range, test_data)
    print(g.read_values())





