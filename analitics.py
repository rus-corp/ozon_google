import json
import os
import aiofiles
import aiohttp
import asyncio

from datetime import datetime, timedelta


from conf import base_url




async def get_month_analitics_for_data_list(session, client_id, api_key, today):
    """ Собираем аналитику(количество продаж) за месяц дя записи в data лист"""
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



async def get_week_analitics_for_data_list(session, client_id, api_key, today):
    # global week_analitics
    """ Собираем аналитику за неделю дя записи в data лист
    заказы в шт, конверсия в корзину из карточки, уникальные посетители с просмотром карточки, уникальные посетители всего
    """
    date_to = today.strftime('%Y-%m-%d')
    start_day = today - timedelta(days=7)
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
    

async def get_every_day_analitic(session, client_id, api_key, today):
    date_to = today.strftime('%Y-%m-%d')
    print(f'Every day report {date_to} - {date_to}')
    data = {
        'date_from': date_to,
        'date_to': date_to,
        'dimension': [
            'sku'
        ],
        'filters': [],
        'limit': 1000,
        'metrics': [
            'revenue',
            'ordered_units',
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
    async with aiofiles.open('get_every_day_analitics.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
    
    



       
            
async def get_analitics(client_id, api_key, today):
    async with aiohttp.ClientSession() as session:
        month_analitic = await get_month_analitics_for_data_list(session, client_id, api_key, today)
        await asyncio.sleep(120)
        week_analitic = await get_week_analitics_for_data_list(session, client_id, api_key, today)
        await asyncio.sleep(120)
        every_day_analitic = await get_every_day_analitic(session, client_id, api_key, today)
        




def analitics_main(client_id, api_key, today):
    asyncio.run(get_analitics(client_id, api_key, today))

# if __name__ == '__main__':
#     client_id = '37611'
#     api_key = 'cc9e2151-f99e-46d4-8ce5-97f2a8c58d2c'
#     analitics_main(client_id, api_key)
    
