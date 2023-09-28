import asyncio
import aiohttp
import json
import logging
from more_itertools import chunked

from conf import ALL_OZON_HEADERS



base_url = "https://api-seller.ozon.ru"



data_dict = {}

product_data = []


async def get_product_data(session, offer_id, product_id, volume, headers):
    data = {
        'offer_id': offer_id,
        'product_id': product_id
    }
    method_url = '/v2/product/info'
    url = base_url + method_url
    response = await session.post(url=url, headers=headers, json=data)
    result = await response.json()
    product_data.append(
        {
            'stock': name,
            'product_id': product_id,
            'article': offer_id,
            'name': result['result']['name'],
            'stocks': result['result']['stocks']['present'],
            'commissions': result['result']['commissions'][1]['value'],
            'price': result['result']['price'],
            'marketing_price': result['result']['marketing_price'],
            'volume': volume
        }
    )
    return product_data



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
    return volume



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
    # print(result['result']['items'])
    tasks = []
    for product in result['result']['items']:
        volume = await get_product_param(session=session, offer_id=product['offer_id'], headers=headers)
        task = asyncio.create_task(get_product_data(session, offer_id=product['offer_id'], product_id=product['product_id'], headers=headers, volume=volume))
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
        return data
        
        
        

if __name__ == '__main__':
    for name, key in ALL_OZON_HEADERS.items():
        asyncio.run(main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
    
    print(len(product_data))
    write_to_file('product_data.json', product_data)
    with open('product_data.json', encoding='utf-8') as file:
        data = json.load(file)
    print(len(data))
    