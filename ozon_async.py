import asyncio
import aiohttp
import json
import logging
import aiofiles
from datetime import datetime, timedelta
from more_itertools import chunked
import os




from conf import ALL_OZON_HEADERS, delivery, volume_range



base_url = "https://api-seller.ozon.ru"



data_dict = {}

product_data = []





async def get_product_data(session, offer_id, product_id, delivery_coast, headers):
    data = {
        'offer_id': offer_id,
        'product_id': product_id
    }
    method_url = '/v2/product/info'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    comission = float(result['result']['commissions'][1]['value'])
    comission_delivery_coast = round((comission + delivery_coast), 2)
    price = float(result['result']['price'])
    marketing_price = float(result['result']['marketing_price'])
    product_data.append(
        {
            'Магазин': name,
            'Ozon Product ID': product_id,
            'Артикул': offer_id,
            'Наименование товара': result['result']['name'],
            'Общее кол-во стоков в ЛК.': result['result']['stocks']['present'],
            'Комиссия + Логистика': comission_delivery_coast,
            'Текущая цена продажи': round(price, 2),
            'Цена с учётом скидки озон': round(marketing_price, 2)
        }
    )
    return product_data



async def get_analitics(session, client_id, api_key):
    today = datetime.now() - timedelta(days=1)
    start_day = today - timedelta(days=30)
    date_from = start_day.strftime('%Y-%m-%d')
    date_to = today.strftime('%Y-%m-%d')
    data = {
        'date_from': date_from,
        'date_to': date_to,
        'dimension': [
          'day',
          'sku'  
        ],
        'filters': [],
        'limit': 1000,
        'metrics': [
            'revenue',
            'ordered_units',
            'hits_view_search',
            'hits_view_pdp',
            'hits_view',
            'session_view_search',
            'session_view_pdp',
            'session_view',
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
    if not os.path.isfile('analitics.json'):
        async with aiofiles.open('analitics.json', 'w', encoding='utf-8') as file:
            await file.write(json.dumps(result['result'], indent=4, ensure_ascii=False))
    else:
        async with aiofiles.open('analitics.json', 'a', encoding='utf-8') as file:
            await file.write(json.dumps(result['result'], indent=2, ensure_ascii=False))
            await file.write('\n')
        
    
    
    



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



async def get_stock(session, client_id, api_key, name):
    data = {
            "filter": {"visibility": "ALL"},
            "last_id": "",
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
                                                    product_id=product['product_id'], headers=headers, delivery_coast=delivery_coast))
        tasks.append(task)
    products = await asyncio.gather(*tasks)
        
       
        
def write_to_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f'Data was writing to {filename}')
    except Exception as e:
        print(f'Error writing: {str(e)}')
            

        

async def main(client_id, api_key, name):
    async with aiohttp.ClientSession() as session:
        data = await get_stock(session, client_id, api_key, name)
        analitics = await get_analitics(session, client_id, api_key)
        return data
        
        
        

if __name__ == '__main__':

    for name, key in ALL_OZON_HEADERS.items():
        asyncio.run(main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
    write_to_file('product_data.json', product_data)
    
    print(len(product_data))
    
    # for name in shops:
    #     write_to_file(f'{name}.json', product_data)
    