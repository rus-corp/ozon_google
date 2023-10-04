import json
import os
import aiofiles
import aiohttp
import asyncio

from datetime import datetime, timedelta


from conf import base_url, sum_metrix




async def get_month_analitics_for_data_list(session, client_id, api_key):
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
        
    async with aiofiles.open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data_to_file, indent=2, ensure_ascii=False))



async def get_month_analitics_for_total_list(session, client_id, api_key):
    """ Собираем аналитику(сумму продаж) за месяц дя записи в total лист"""
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
            'revenue',
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
    
    async with aiofiles.open('get_month_analitics_for_total_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data_to_file, indent=2, ensure_ascii=False))
             
        
        
        

async def get_week_analitics_for_data_list(session, client_id, api_key):
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
    async with aiofiles.open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data_to_file, indent=2, ensure_ascii=False))
    
    
    
async def get_week_analitics_for_total_list(session, client_id, api_key):
    """ Собираем аналитику (продажи в шт) за неделю дя записи в total лист"""
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
            'ordered_units'
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
    async with aiofiles.open('get_week_analitics_for_total_list.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data_to_file, indent=2, ensure_ascii=False))
            
            
            
            
async def analitics_main(client_id, api_key):
    async with aiohttp.ClientSession() as session:
        month_analitics_for_data = await get_month_analitics_for_data_list(session, client_id, api_key)

        month_analitic_for_total = await get_month_analitics_for_total_list(session, client_id, api_key)

        week_analitics_for_data = await get_week_analitics_for_data_list(session, client_id, api_key)

        week_analitics_for_total = await get_week_analitics_for_total_list(session, client_id, api_key)
        return week_analitics_for_total
    
    
    
