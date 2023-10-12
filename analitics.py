import json
import os
import aiofiles
import aiohttp
import asyncio
import logging
import logging

from datetime import datetime, timedelta


from data import base_url

logger = logging.getLogger('ozon.analitics')


async def get_month_analitics_for_data_list(session, client_id, api_key, today, name):
    """ Собираем аналитику(количество продаж) за месяц дя записи в data лист"""
    start_day = today - timedelta(days=30)
    date_from = start_day.strftime('%Y-%m-%d')
    date_to = today.strftime('%Y-%m-%d')
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
    while True:
        logger.info(f'month analitic for date {date_from} - {date_to} for {name}')
        response = await session.post(url=url, headers=headers, json=data)
        result = await response.json()
        if 'result' in result and 'data' in result['result']:
            async with aiofiles.open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
                await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
            break
        else:
            logger.info('не смог получить аналитику за месяц')
            await asyncio.sleep(60)


async def get_week_analitics_for_data_list(session, client_id, api_key, today, name):
    # global week_analitics
    """ Собираем аналитику за неделю дя записи в data лист
    заказы в шт, конверсия в корзину из карточки, уникальные посетители с просмотром карточки, уникальные посетители всего
    """
    date_to = today.strftime('%Y-%m-%d')
    start_day = today - timedelta(days=6)
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
    while True:
        logger.info(f'недельная аналитика за даты {date_from} - {date_to} for {name}')
        response = await session.post(url=url, headers=headers, json=data)
        result = await response.json()
        if 'result' in result and 'data' in result['result']:
            async with aiofiles.open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
                await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
            break
            
        else:
            logger.info('не смог получить аналитику за неделю')
            await asyncio.sleep(60)



async def get_every_day_analitic(session, client_id, api_key, today, name):
    date_to = today.strftime('%Y-%m-%d')
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
    while True:
        logger.info(f'ежедневная аналитика за даты {date_to} - {date_to} for {name}')
        response = await session.post(url=url, headers=headers, json=data)
        result = await response.json()
        if 'result' in result and 'data' in result['result']:
            async with aiofiles.open('get_every_day_analitics.json', 'w', encoding='utf-8') as file:
                await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
            break
        else:
            logger.info('не смог получить аналитику за день')
            await asyncio.sleep(60)
    

            
async def get_analitics(client_id, api_key, today, name):
    async with aiohttp.ClientSession() as session:
        month_analitic = await get_month_analitics_for_data_list(session, client_id, api_key, today, name)
        week_analitic = await get_week_analitics_for_data_list(session, client_id, api_key, today, name)
        every_day_analitic = await get_every_day_analitic(session, client_id, api_key, today, name)
        




def analitics_main(client_id, api_key, today, name):
    asyncio.run(get_analitics(client_id, api_key, today, name))

    
