import asyncio
import os
import schedule
from datetime import datetime, timedelta
from ozon_async import ozon_main
from analitics import analitics_main
from utils import write_to_file
from google_sheet import google_main

from conf import ALL_OZON_HEADERS



def main():
    today = datetime.now() - timedelta(days=2)
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
                    
        product_data = asyncio.run(ozon_main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
        analitics_main(client_id=key['Client-Id'], api_key=key['Api-Key'], today=today)
        google_main(file_path, today)
    
    
        files = ['/Users/ruslanprusakov/my_project/ozon_google/data_to_data_sheet.json', '/Users/ruslanprusakov/my_project/ozon_google/data_to_total_sheet.json',
                '/Users/ruslanprusakov/my_project/ozon_google/get_month_analitics_for_data_list.json', '/Users/ruslanprusakov/my_project/ozon_google/get_week_analitics_for_data_list.json',
                '/Users/ruslanprusakov/my_project/ozon_google/product_data.json', 'get_every_day_analitics.json']
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError as e:
                print(e)
            except Exception as ex:
                print(ex)
            
    google_files = ['counter_data.json', 'counter_total.json']
    for file in google_files:
        try:
            os.remove(file)
        except FileNotFoundError as e:
            print(e)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()