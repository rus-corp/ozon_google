import json
import gspread
from gspread import Client, Spreadsheet, Worksheet
from pprint import pprint
from gspread.utils import rowcol_to_a1

from conf import credentials, column_indexes_for_data, column_indexes_for_total
from utils import data_to_write_data_sheet



from conf import SPREADSHEET_URL



# def insert_data(ws: Worksheet):
#     with open('test_data.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     header_rows = ws.row_values(1)
#     data_matrix = []
#     for item in data:
#         row_data = [''] * len(header_rows)
#         for key, value in item.items():
#             if key in header_rows:
#                 col_index = header_rows.index(key)
#                 row_data[col_index] = value
#         data_matrix.append(row_data)
#     start_row = 2
#     ws.update(data_matrix, start_row)



def write_to_data_list(ws: Worksheet):
    try:
        with open('counter_data.json', 'r', encoding='utf-8') as file:
            counter_data = json.load(file)
            counter = counter_data.get('counter_data', 1)
    except FileNotFoundError:
        counter = 1
    sheet_data = ws.get_all_values()
    with open('data_to_data_sheet.json', 'r', encoding='utf-8') as file:
        new_data = json.load(file)
    batches = []
    for i in range(counter + 1, len(new_data) + 1):
        for name, index in column_indexes_for_data.items():
            values = new_data[i-1].get(name, '')
            addr = rowcol_to_a1(i + 1, index)
            batch = {
                'range': addr,
                'values': [[values]]
            }
            batches.append(batch)
        counter += 1
    with open('counter_data.json', 'w', encoding='utf-8') as file:
        json.dump({'counter_data': counter}, file)
    ws.batch_update(batches)
    


def write_to_total_list(ws: Worksheet):
    try:
        with open('counter_total.json', 'r', encoding='utf-8') as file:
            counter_data = json.load(file)
            counter = counter_data.get('counter_total', 1)
    except FileNotFoundError:
        counter = 1
    sheet_data = ws.get_all_values()
    with open('data_to_total_sheet.json', 'r', encoding='utf-8') as file:
        new_data = json.load(file)
    batches = []
    for i in range(counter + 1, len(new_data) + 1):
        for name, index in column_indexes_for_total.items():
            values = new_data[i-1].get(name, '')
            addr = rowcol_to_a1(i + 1, index)
            batch = {
                'range': addr,
                'values': [[values]]
            }
            batches.append(batch)
        counter +=1
    with open('counter_total.json', 'w', encoding='utf-8') as file:
        json.dump({'counter_total': counter}, file)
    ws.batch_update(batches)
        
                
        

def google_main():
    data_to_write_data_sheet()
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet_list = sh.worksheets('DATA')
    data = sh.worksheet('DATA')
    total = sh.worksheet('TOTAL')
    
    write_to_data_list(data)
    write_to_total_list(total)
    
    
    # get_values(data)
    # insert_data(data)


if __name__ == '__main__':
    google_main()
    # with open('analitics.json', encoding='utf-8') as file:
    #     data = json.load(file)
    # pprint(data['data'])
    # for item in data['data']:
    #     pprint(item['metrics'][1])
    
    
    # def get_values(ws):
#     sheet_data = ws.get_all_values()
#     # print(sheet_data)
#     with open('test_data.json', 'r', encoding='utf-8') as file:
#         new_data = json.load(file)
#     batches = []
#     for i in range(1, len(new_data)):
#         for name, index in column_indexes.items():
#             values = new_data[i-1].get(name, '')
#             addr = rowcol_to_a1(i + 1, index)
#             batch = {
#                 'range': addr,
#                 'values': [[values]]
#             }
#             batches.append(batch)
#     ws.batch_update(batches)