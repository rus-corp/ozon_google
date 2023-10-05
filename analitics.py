import json
import os
import aiofiles
import aiohttp
import asyncio

from datetime import datetime, timedelta


from conf import base_url, sum_metrix




month_analitics = []
week_analitics = []


async def get_month_analitics_for_data_list(session, client_id, api_key):
    global month_analitics
    """ Собираем аналитику(количество продаж) за месяц дя записи в data лист"""
    today = datetime.now() - timedelta(days=1)
    start_day = today - timedelta(days=30)
    date_from = start_day.strftime('%Y-%m-%d')
    date_to = today.strftime('%Y-%m-%d')
    data = {
        'date_from': date_from,
        'date_to': date_to,
        'dimension': [
          'sku'  
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
    try:
        data_to_file = sum_metrix(result['result']['data'])
    except Exception as e:
        print('===========')
        print(e)
    try:
        month_analitics = [(key, value) for key, value in data_to_file.items()]
        return month_analitics
    except:
        print('Не полчил месячную аналитику')
        


        
        

async def get_week_analitics_for_data_list(session, client_id, api_key):
    global week_analitics
    """ Собираем аналитику за неделю дя записи в data лист
    заказы в шт, конверсия в корзину из карточки, уникальные посетители с просмотром карточки, уникальные посетители всего
    """
    today = datetime.now() - timedelta(days=1)
    date_to = today.strftime('%Y-%m-%d')
    start_day = datetime.now() - timedelta(days=7)
    date_from = start_day.strftime('%Y-%m-%d')
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
    try:
        data_to_file = sum_metrix(result['result']['data'])
    except Exception as e:
        print('===========')
        print(e)
    try:
        week_analitics = [(key, value) for key, value in data_to_file.items()]
        return week_analitics
    except:
        print('не получил недельную аналитику')

    
    
    
async def get_two_week_analitics(session, client_id, api_key):
    """Сбор аналитики по продажам за 2 недели"""
    today = datetime.now() - timedelta(days=1)
    date_to = today.strftime('%Y-%m-%d')
    start_day = datetime.now() - timedelta(days=14)
    date_from = start_day.strftime('%Y-%m-%d')
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
    a = 3
    async with aiofiles.open('get_two_week_analitics_for_total_list3.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
    
    
async def get_every_day_analitics(session, client_id, api_key):
    """Сбор аналитики по продажам за 2 недели"""
    today = datetime.now() - timedelta(days=1)
    date_to = today.strftime('%Y-%m-%d')
    start_day = datetime.now() - timedelta(days=2)
    date_from = start_day.strftime('%Y-%m-%d')
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
    a = 3
    async with aiofiles.open('get_two_week_analitics_for_total_list4.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False)) 
    
    
    
    

            
            
async def get_analitics(client_id, api_key):
    async with aiohttp.ClientSession() as session:
        month_analitics_for_data = await get_month_analitics_for_data_list(session, client_id, api_key)
        week_analitics_for_data = await get_week_analitics_for_data_list(session, client_id, api_key)
        # week_analitics_for_total = await get_week_analitics_for_total_list(session, client_id, api_key)
        return month_analitics_for_data
    



def analitics_main(client_id, api_key):
    asyncio.run(get_analitics(client_id, api_key))
    month = 'get_month_analitics_for_data_list.json'
    week = 'get_week_analitics_for_data_list.json'
    if os.path.exists(month):
        with open('get_month_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.extend(month_analitics)
    else:
        data = month_analitics
    with open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    if os.path.exists(week):
        with open('get_week_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.extend(month_analitics)
    else:
        data = week_analitics
    with open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)





# if __name__ == '__main__':
#     main()
    
