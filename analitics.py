import json
import os
import aiofiles
import aiohttp
import asyncio
import logging
import logging

from datetime import timedelta

from data import bot_token
from telegram_bot import telegram_notify
from data import base_url


logger = logging.getLogger('ozon.analitics')


async def get_month_analitics_for_data_list(session, client_id, api_key, today, name, users):
    """ Собираем аналитику(количество продаж) за месяц дя записи в data лист"""
    try:
        start_day = today - timedelta(days=30)
        date_from = start_day.strftime('%Y-%m-%d')
        date_to = today.strftime('%Y-%m-%d')
        message = f'Собираю месячную аналитику за даты: {date_from} - {date_to} для магазина {name}'
        logger.info(message)
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)
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
        while True:
            response = await session.post(url=url, headers=headers, json=data)
            result = await response.json()
            if 'result' in result and 'data' in result['result']:
                async with aiofiles.open('get_month_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
                break
            else:
                logger.info('не смог получить аналитику за месяц')
                await asyncio.sleep(5)
    except Exception as e:
        logger.error('!!!!!!!! Произошла ошибка при сборе недельной аналитики', str(e))
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)


async def get_week_analitics_for_data_list(session, client_id, api_key, today, name, users):    
    """ Собираем аналитику за неделю дя записи в data лист
    заказы в шт, конверсия в корзину из карточки, уникальные посетители с просмотром карточки, уникальные посетители всего
    """
    try:
        date_to = today.strftime('%Y-%m-%d')
        start_day = today - timedelta(days=6)
        date_from = start_day.strftime('%Y-%m-%d')
        message = f'Недельная аналитика за даты {date_from} - {date_to} для {name}'
        logger.info(message)
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)
        data = {
            'date_from': date_from,
            'date_to': date_to,
            'dimension': [
            'sku'
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
            response = await session.post(url=url, headers=headers, json=data)
            result = await response.json()
            if 'result' in result and 'data' in result['result']:
                async with aiofiles.open('get_week_analitics_for_data_list.json', 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
                break
                
            else:
                logger.info('не смог получить аналитику за неделю')
                # bot_send_message(bot, text='не смог получить аналитику за неделю')
                await asyncio.sleep(5)
    except Exception as e:
        logger.error('!!!!!!!! Произошла ошибка при сборе недельной аналитики', str(e))
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)
            



async def get_every_day_analitic(session, client_id, api_key, today, name, users):
    try:
        date_to = today.strftime('%Y-%m-%d')
        message = f'Ежедневная аналитика за даты {date_to} - {date_to} для {name}'
        logger.info(message)
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)
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
            response = await session.post(url=url, headers=headers, json=data)
            result = await response.json()
            if 'result' in result and 'data' in result['result']:
                async with aiofiles.open('get_every_day_analitics.json', 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))
                break
            else:
                logger.info('не смог получить аналитику за день')
                # bot_send_message(bot, text='не смог получить аналитику за день')
                await asyncio.sleep(5)
    except Exception as e:
        logger.info(f'!!!!!! Произошла ошибка при сборе ежедневной аналитики {str(e)}')
        for user in users:
            await telegram_notify(message=message, token=bot_token, chat_id=user)
        

            
async def get_analitics(client_id, api_key, today, name):
    with open('users.txt') as file:
        users = file.readlines()
    async with aiohttp.ClientSession() as session:
        month_analitic = await get_month_analitics_for_data_list(session, client_id, api_key, today, name, users)
        week_analitic = await get_week_analitics_for_data_list(session, client_id, api_key, today, name, users)
        every_day_analitic = await get_every_day_analitic(session, client_id, api_key, today, name, users)
        

