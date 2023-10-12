import asyncio
import os
import schedule
from datetime import datetime, timedelta
from ozon_async import ozon_main
from analitics import analitics_main
from utils import write_to_file
from google_sheet import google_main
import logging, logging.handlers
import json
import time


from data import ALL_OZON_HEADERS
from utils import total_sheet_data, write_to_total_sheet
from google_sheet import write_to_total_list, update_header_row




def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(filename='ozon_log.log', maxBytes=100000, backupCount=5)
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.debug('loger was initialized')





def main():
    init_logger('ozon')
    update_header_row()
    today = datetime.now() - timedelta(days=1)
    for name, key in ALL_OZON_HEADERS.items():
        match name:
            case 'Voyor':
                file_path = 'store_sales/voyor_store.json'
            case '2BE':
                file_path = 'store_sales/2be_store.json'
            case 'Arris':
                file_path = 'store_sales/arris_store.json'
            case 'NemoCAM':
                file_path = 'store_sales/nemocam_store.json'
            case 'Tabi':
                file_path = 'store_sales/tabi_store.json'
            case 'UniStellar':
                file_path = 'store_sales/unistellar_store.json'
            case 'PUFFER':
                file_path = 'store_sales/puffer_store.json'
            case 'Metalscan':
                file_path = 'store_sales/metalscan_store.json'
                    
        product_data = asyncio.run(ozon_main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
        
        analitics_main(client_id=key['Client-Id'], api_key=key['Api-Key'], today=today, name=name)
        google_main(file_path, today)
        write_to_total_sheet(file_path, today)      # компануем данные и продажи 
    
        files = ['data_to_data_sheet.json', 
                'get_month_analitics_for_data_list.json', 'get_week_analitics_for_data_list.json',
                'get_every_day_analitics.json', 'product_data.json']
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError as e:
                print(e)
            except Exception as ex:
                print(ex)
    
       
    total_sheet_data()           # готовим данные для записи в тотал
    write_to_total_list()        # записываем данные в тотал
    google_files = ['counter_data.json', 'for_total_sheet.json', 'data_to_total_sheet.json']
    for file in google_files:
        try:
            os.remove(file)
        except FileNotFoundError as e:
            print(e)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()