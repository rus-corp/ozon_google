import json
import gspread
from gspread import Client, Spreadsheet, Worksheet
from pprint import pprint
from gspread.utils import rowcol_to_a1
import logging
from datetime import datetime, timedelta

from data import credentials, column_indexes_for_data, column_indexes_for_total, bot_token
from utils import data_to_write_data_sheet, total_sheet_data, write_to_total_sheet

logger = logging.getLogger('ozon.google')

from data import SPREADSHEET_URL


def update_header_row():
    logger.info('меняю строки на листе DATA')
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(SPREADSHEET_URL)
    ws = sh.worksheet('DATA')
    header_row = ws.row_values(1)
    today = datetime.now()
    date_list = [today - timedelta(days=i) for i in range(1, 8)]
    header_row[25:] = [date.strftime('%d-%m-%Y') for date in date_list]
    ws.update('A1', [header_row])
    


def write_to_data_list(ws: Worksheet):
    logger.info('пишу данные в DATA')
    sheet_data = ws.get_all_values()
    with open('data_to_data_sheet.json', 'r', encoding='utf-8') as file:
        new_data = json.load(file)
    batches = []
    for i in range(1, len(new_data) + 1):
        for name, index in column_indexes_for_data.items():
            values = new_data[i-1].get(name, '')
            addr = rowcol_to_a1(i + 1, index)
            batch = {
                'range': addr,
                'values': [[values]]
            }
            batches.append(batch)


    ws.batch_update(batches)
    


def write_to_total_list():
    logger.info('пишу данные в TOTAL')
    real_column = column_indexes_for_total
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(SPREADSHEET_URL)
    total = sh.worksheet('TOTAL')
    sheet_data = total.get_all_values()
    with open('data_to_total_sheet.json', 'r', encoding='utf-8') as file:
        new_data = json.load(file)
    batches = []
    for i in range(1, len(new_data) + 1):
        for name, index in real_column.items():
            values = new_data[i-1].get(name, '')
            addr = rowcol_to_a1(i + 1, index)
            batch = {
                'range': addr,
                'values': [[values]]
            }
            batches.append(batch)

    total.batch_update(batches)
        
                

                
def google_main():
    logging.info(f'готовлю данные для записи в гугл')
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(SPREADSHEET_URL)
    data = sh.worksheet('DATA')
    write_to_data_list(data)
    total_sheet_data()           # готовим данные для записи в тотал
    write_to_total_list()

