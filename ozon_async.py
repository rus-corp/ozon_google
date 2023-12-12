import asyncio
import aiohttp
import json
import logging
import aiofiles
import logging

from more_itertools import chunked
import os

from data import base_url, volume_range, delivery
from analitics import get_month_analitics_for_data_list, get_week_analitics_for_data_list #, get_week_analitics_for_total_list, get_month_analitics_for_total_list
from utils import write_to_file

logger = logging.getLogger('ozon.product')

product_data = []


async def get_product_data(session, offer_id, product_id, delivery_coast, headers, name):
    # logger.info(f'Собираю параметры продукта для {name}')
    try:
        data = {
            'offer_id': offer_id,
            'product_id': product_id
        }
        method_url = '/v2/product/info'
        url = base_url + method_url
        response = await session.post(url=url, headers=headers, json=data)
        result = await response.json()
        price = float(result['result']['price'])
        price_round = round(price, 2)
        try:
            min_price = float(result['result']['min_price'])
            min_price_round = round(min_price, 2)
        except:
            min_price_round = price_round

        
        last_mile = float(price_round * 0.055)
        try:
            comission_percent = float(result['result']['commissions'][1]['percent'])
        except Exception as e:
            comission_percent = 1
            logging.info(f'Ошибка комиссии товара в магазине {name} - {e} товар:{result["result"]["name"]}')
        
        comission = round(price_round * (comission_percent / 100) + last_mile, 2)
        
        comission_delivery_coast = round((comission + delivery_coast), 2)
        try:
            marketing_price = float(result['result']['marketing_price'])
            marketing_price_round = round(marketing_price, 2)
        except Exception as e:
            logging.info(f'Ошибка цены товара в магазине {name} - {e} товар:{result["result"]["name"]}')
            marketing_price_round = price_round
            
        product_data.append(
            {
                'Магазин': name,
                'Ozon Product ID': result['result']['fbs_sku'],
                'SKU': result['result']['sku'],
                'fbo_sku': result['result']['fbo_sku'],
                'Артикул': offer_id,
                'Наименование товара': result['result']['name'],
                'Общее кол-во стоков в ЛК.': result['result']['stocks']['present'],
                'Статус': result['result']['status']['state_name'],
                'Комиссия + Логистика': comission_delivery_coast,
                'Текущая цена продажи': price_round,
                'Цена с учётом скидки озон': marketing_price_round,
                'Минимальная цена': min_price_round
            }
        )
        return product_data
    except Exception as e:
        logger.error(f'Произошла ошибка при формировании товаров {name}, {str(e)}')



async def get_product_param(session, offer_id, headers):
    method_url = '/v3/products/info/attributes'
    url = base_url + method_url
    data = {
        'filter': {
            'offer_id': [offer_id],
            'visibility': 'ALL'
        },
        'limit': 1000
    }
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    volume = None
    for item in result['result']:
        volume = round((item['depth'] / 1000 * item['height'] / 1000 * item['width'] / 1000) * 1000, 3)
    delivery_coast = volume_range(volume, delivery)
    return delivery_coast



async def get_stock(session, client_id, api_key, name, visibility):
    logger.info(f'Собираю сток для {name}')
    data = {
            "filter": {"visibility": visibility},
            "limit": 1000,}
    headers = {
        'Client-Id': client_id,
        'Api-Key': api_key
    }
    tasks = []
    method_url = '/v3/product/info/stocks'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    tasks = []
    for product in result['result']['items']:
        delivery_coast = float(await get_product_param(session=session, offer_id=product['offer_id'], headers=headers))
        
        task = asyncio.create_task(get_product_data(session, offer_id=product['offer_id'], 
                                                    product_id=product['product_id'], headers=headers, delivery_coast=delivery_coast, name=name))
        tasks.append(task)
    products = await asyncio.gather(*tasks)
        
       
        
        
async def ozon_main(client_id, api_key, name):
    print(f'Собираю товар для {name}')
    product_data.clear()
    async with aiohttp.ClientSession() as session:
        data = await get_stock(session, client_id, api_key, name, 'ALL')
        data_archive = await get_stock(session, client_id, api_key, name, 'ARCHIVED')
        # async with aiofiles.open('product_data.json', 'w', encoding='utf-8') as file:
        #     await file.write(json.dumps(product_data, indent=2, ensure_ascii=False))
        return product_data
        

        
        

