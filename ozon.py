
import requests
import json
from pprint import pprint
from datetime import datetime, timedelta










base_url = "https://api-seller.ozon.ru"

product_data = []




def get_product_data(name, offer_id, product_id, volume, headers):
    
    data = {
        'offer_id': offer_id,
        'product_id': product_id
    }
    method_url = '/v2/product/info'
    url = base_url + method_url
    resp = requests.post(url=url, headers=headers, json=data).json()
    product_data.append(
        {   
            'store': name,
            'article': offer_id,
            'product_id': product_id,
            'name': resp['result']['name'],
            'stock': resp['result']['stocks']['present'],
            'price': resp['result']['price'],
            'ozon_price': resp['result']['marketing_price'],
            'commissions': resp['result']['commissions'],
            'volume': volume
        }
    )
    
    
    
def get_product_param(name, offer_id, product_id, headers):
    method_url = '/v3/products/info/attributes'
    url = base_url + method_url
    data = {
        'filter': {
            'offer_id': [offer_id],
            'visibility': 'ALL'
        },
        'limit': 1000
    }
    
    response = requests.post(url=url, headers=headers, json=data).json()
    volume = None
    for item in response['result']:
        volume = round((item['depth'] / 1000 * item['height'] / 1000 * item['width'] / 1000) * 1000, 3)
    
    get_product_data(name, offer_id, product_id, volume, headers)
    
    
def get_analitic(headers):
    date_before = datetime.now() - timedelta(days=30)
    date_from = date_before.strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    data = {
        'date_from': date_from,
        'date_to': today,
        'dimension': ['sku'],
        'metrics': [
            'revenue',
            'ordered_units',
            'hits_view_search',
            'hits_view_pdp',
            'hits_view',
            'session_view_search',
            'session_view_pdp',
            'session_view',
        ],
        'filters': [],
        'sort': [
            {
                'key': 'ordered_units',
                'order': 'DESC'
            }
        ],
        'limit': 1000,
        'offset': 0
        
    }
    method_url = '/v1/analytics/data'
    url = base_url + method_url
    resp = requests.post(url=url, headers=headers, json=data).json()
    with open ('analitic.json', 'w', encoding='utf-8') as file:
        json.dump(resp, file, indent=4, ensure_ascii=False)
    return resp
    
    
    
    
def get_stock(name, client_id, api_key):
    data = {
            "filter": {"visibility": "ALL"},
            "last_id": "",
            "limit": 1000,}
    headers = {
            "Client-Id": client_id,
            "Api-Key": api_key}
    method_url = '/v3/product/info/stocks'
    url = base_url + method_url
    resp = requests.post(url=url, headers=headers, json=data).json()
    get_analitic(headers=headers)
    for product in resp['result']['items']:
        # get_product_data(name, offer_id=product['offer_id'], product_id=product['product_id'], headers=headers)
        get_product_param(name=name, offer_id=product['offer_id'], product_id=product['product_id'], headers=headers)







# if __name__ == '__main__':
#     for name, key in ALL_OZON_HEADERS.items():
#         get_stock(name, key['Client-Id'], key['Api-Key'])
#     print(len(product_data))
    # with open('data.json', 'w', encoding='utf-8') as file:
    #     json.dump(product_data, file, indent=4, ensure_ascii=False)
         