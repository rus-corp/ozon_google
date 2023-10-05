import asyncio
import os
import schedule

from ozon_async import ozon_main
from analitics import analitics_main
from utils import write_to_file
from google_sheet import google_main

from conf import ALL_OZON_HEADERS



def main():
    for name, key in ALL_OZON_HEADERS.items():
        product_data = asyncio.run(ozon_main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
        analitics_main(client_id=key['Client-Id'], api_key=key['Api-Key'])
    google_main()
    # files = ['/Users/ruslanprusakov/my_project/ozon_google/data_to_total_sheet.json', '/Users/ruslanprusakov/my_project/ozon_google/get_month_analitics_for_data_list.json', '/Users/ruslanprusakov/my_project/ozon_google/get_month_analitics_for_total_list.json'
    #          '/Users/ruslanprusakov/my_project/ozon_google/get_week_analitics_for_data_list.json', '/Users/ruslanprusakov/my_project/ozon_google/get_week_analitics_for_total_list.json', '/Users/ruslanprusakov/my_project/ozon_google/product_data.json']
    # for file in files:
    #     try:
    #         os.remove(file)
    #     except FileNotFoundError as e:
    #         print(e)
    #     except Exception as ex:
    #         print(ex)
            
            


if __name__ == '__main__':
    main()