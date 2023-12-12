import asyncio
import os
import schedule
from datetime import datetime, timedelta
from ozon_async import ozon_main
from analitics import analitics_main
from utils import data_to_write_data_sheet
from google_sheet import google_main
import logging, logging.handlers
import json
import time


from data import ALL_OZON_HEADERS
from utils import write_to_total_sheet, clean_sales
from google_sheet import update_header_row




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
    # update_header_row()
    today = datetime.now() - timedelta(days=1)
    for name, key in ALL_OZON_HEADERS.items():
        match name:
            case 'Voyor':
                file_path = 'store_sales/voyor_store.json'
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
        
        
        data_to_write_data_sheet(file_path, today, product_data)
        write_to_total_sheet(file_path, today, product_data)
        
        # if datetime.now().weekday() == 1:
        #     clean_sales(file_path)
            
        files = [ 'get_month_analitics_for_data_list.json', 'get_week_analitics_for_data_list.json',
                'get_every_day_analitics.json']
        
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError as e:
                print(e)
            except Exception as ex:
                print(ex)
    
    google_main()
    google_files = ['for_total_sheet.json', 'data_to_total_sheet.json', 'data_to_data_sheet.json']
    for file in google_files:
        try:
            os.remove(file)
        except FileNotFoundError as e:
            print(e)
        except Exception as ex:
            print(ex)



if __name__ == '__main__':
    main()