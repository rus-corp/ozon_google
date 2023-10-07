import json
import os
import aiofiles
import aiohttp
import asyncio

from datetime import datetime, timedelta


from conf import base_url, sum_metrix




month_analitics = []
week_analitics = []
two_weeks_analitics = []

async def get_month_analitics_for_data_list(session, client_id, api_key):
    """ Собираем аналитику(количество продаж) за месяц дя записи в data лист"""
    today = datetime.now() - timedelta(days=1)
    start_day = today - timedelta(days=30)
    date_from = start_day.strftime('%Y-%m-%d')
    date_to = today.strftime('%Y-%m-%d')
    print(f'Даты отчета month: {date_from} - {date_to}')
    data = {
        'date_from': date_from,
        'date_to': date_to,
        'dimension': [
          'spu'  
        ],
        'filters': [],
        'limit': 1000,
        'metrics': [
            'ordered_units',
            'revenue'
        ]
    }
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    method_url = '/v1/analytics/data'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    async with aiofiles.open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))



async def get_week_analitics_for_data_list(session, client_id, api_key):
    # global week_analitics
    """ Собираем аналитику за неделю дя записи в data лист
    заказы в шт, конверсия в корзину из карточки, уникальные посетители с просмотром карточки, уникальные посетители всего
    """
    today = datetime.now() - timedelta(days=1)
    date_to = today.strftime('%Y-%m-%d')
    start_day = datetime.now() - timedelta(days=7)
    date_from = start_day.strftime('%Y-%m-%d')
    print(f'Даты отчета week: {date_from} - {date_to}')
    data = {
        'date_from': date_from,
        'date_to': date_to,
        'dimension': [
          'spu'  
        ],
        'filters': [],
        'limit': 1000,
        'metrics': [       
            'ordered_units',       # заказано шт
            'conv_tocart_pdp',     # конверсия в корзину из карточки
            'session_view_pdp',    # уникальные посетители с просмотром карточки
            'session_view',        # уникальные посетители всего
            'position_category',
        ]
    }
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    method_url = '/v1/analytics/data'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    async with aiofiles.open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))

    
    


async def get_two_week_analitics(session, client_id, api_key):
    """Сбор аналитики по продажам за 2 недели"""
    today = datetime.now() - timedelta(days=5)
    date_to = today.strftime('%Y-%m-%d')
    start_day = today - timedelta(days=13)
    date_from = start_day.strftime('%Y-%m-%d')
    print(date_from, date_to)
    data = {
        'date_from': date_from,
        'date_to': date_to,
        'dimension': [
          'sku',
          'day',
        ],
        'filters': [],
        'limit': 1000,
        'metrics': [
            'revenue'
        ]
    }
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    method_url = '/v1/analytics/data'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    async with aiofiles.open('get_two_week_analitics.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
    
    

            
            
async def get_analitics(client_id, api_key):
    async with aiohttp.ClientSession() as session:
        month_analitics_for_data = await get_month_analitics_for_data_list(session, client_id, api_key)
        await asyncio.sleep(70)
        week_analitics_for_data = await get_week_analitics_for_data_list(session, client_id, api_key)
        await asyncio.sleep(70)
        two_weeks_ananlitic = await get_two_week_analitics(session, client_id, api_key)
        




def analitics_main(client_id, api_key):
    asyncio.run(get_analitics(client_id, api_key))
    # month = 'get_month_analitics_for_data_list.json'
    # week = 'get_week_analitics_for_data_list.json'
    # two_week = 'get_two_week_analitics1'
    
    # if os.path.exists(month):
    #     with open('get_month_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
    #         analitic_month = json.load(file)
    #     analitic_month.extend(month_analitics)
    # else:
    #     analitic_month = month_analitics
    # with open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
    #     json.dump(analitic_month, file, indent=2, ensure_ascii=False)
    # month_analitics.clear()
    
    # if os.path.exists(week):
    #     with open('get_week_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
    #         week_analitic = json.load(file)
    #     week_analitic.extend(week_analitics)
    # else:
    #     week_analitic = week_analitics
    # with open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
    #     json.dump(week_analitic, file, indent=2, ensure_ascii=False)
    # week_analitics.clear()
    
    # if os.path.exists(two_week):
    #     with open('get_two_week_analitics.json', 'r', encoding='utf-8') as file:
    #         week_two_analitic = json.load(file)
    #     week_two_analitic.extend(two_weeks_analitics)
    # else:
    #     week_two_analitic = two_weeks_analitics
    # with open('get_two_week_analitics.json', 'w', encoding='utf-8') as file:
    #     json.dump(week_two_analitic, file, indent=2, ensure_ascii=False)
    # two_weeks_analitics.clear()



# if __name__ == '__main__':
#     client_id = '37611'
#     api_key = 'cc9e2151-f99e-46d4-8ce5-97f2a8c58d2c'
#     analitics_main(client_id, api_key)
    
