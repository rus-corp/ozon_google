import json
import gspread
from gspread import Client, Spreadsheet, Worksheet

from conf import credentials, column_mapping

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/12Dpdg_OEQCrWNcMP977-tfhFUX69eHRM7pP_FblMNCk/edit#gid=0'


def show_worksheets(sh: Spreadsheet):
    worksheet = sh.worksheets()



def insert_data(ws: Worksheet):
    with open('product_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    header_rows = ws.row_values(1)
    data_matrix = []
    for item in data:
        row_data = [''] * len(header_rows)
        for key, value in item.items():
            if key in header_rows:
                col_index = header_rows.index(key)
                row_data[col_index] = value
        data_matrix.append(row_data)
    start_row = 2
    ws.insert_rows(data_matrix, start_row)
    


def main():
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet_list = sh.worksheets()
    data = sh.worksheet('DATA')
    insert_data(data)


if __name__ == '__main__':
    main()