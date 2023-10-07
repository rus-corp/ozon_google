from datetime import datetime, timedelta
import json
# from pprint import pprint
# import copy
# import aiofiles
# import aiohttp
# import asyncio
# import os

# from conf import base_url
# from utils import load_json_file, every_day_analitic_dict
# from conf import ALL_OZON_HEADERS


# async def get_every_day_analitic(session, client_id, api_key, today):
#     date_to = today.strftime('%Y-%m-%d')
#     print(f'Every day report {date_to} - {date_to}')
#     data = {
#         'date_from': date_to,
#         'date_to': date_to,
#         'dimension': [
#             'sku'
#         ],
#         'filters': [],
#         'limit': 1000,
#         'metrics': [
#             'revenue',
#             'ordered_units',
#         ]
#     }
#     headers = {
#         'Client-Id': client_id,
#         'Api-Key': api_key
#     }
#     method_url = '/v1/analytics/data'
#     url = base_url + method_url
#     response = await session.post(url=url, headers=headers, json=data)
#     result = await response.json()
#     async with aiofiles.open('get_every_day_analitics.json', 'w', encoding='utf-8') as file:
#         await file.write(json.dumps(result['result']['data'], indent=2, ensure_ascii=False))




# async def get_analitics(client_id, api_key, today):
#     async with aiohttp.ClientSession() as session:
#         every_day_analitic = await get_every_day_analitic(session, client_id, api_key, today)
        


# def analitics_main(client_id, api_key, today):
#     asyncio.run(get_analitics(client_id, api_key, today))





if __name__ == '__main__':
    
    today = datetime.now() + timedelta(days=6)
    print(today)

    # for name, key in ALL_OZON_HEADERS.items():
    #     match name:
    #         case 'Voyor':
    #             file_path = 'store_sales/voyor_store.json'
    #         case '2BE':
    #             file_path = 'store_sales/2be_store.json'
    #         case 'Arris':
    #             file_path = 'store_sales/arris_store.json'
    #         case 'NemoCAM':
    #             file_path = 'store_sales/nemocam_store.json'
    #         case 'Tabi':
    #             file_path = 'store_sales/tabi_store.json'
    #         case 'UniStellar':
    #             file_path = 'store_sales/unistellar_store.json'

    #     analitics_main(client_id=key['Client-Id'], api_key=key['Api-Key'], today=today)
    
    #     every_day_analitics = load_json_file('get_every_day_analitics.json')
    #     every_day_dict = every_day_analitic_dict(file_path, every_day_analitics, today)
    #     os.remove('get_every_day_analitics.json')
    #     print(f'Собрали данные с {name}')
    

    with open('store_sales/unistellar_store.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    start_date = datetime.now() - timedelta(days=12)
    end_date = datetime.now() - timedelta(days=6)
    
    
    total_sales = {}
    current_date = start_date
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            total_sales[product_id] += metrics[1]
        current_date = current_date + timedelta(days=1)
    print(total_sales)









# with open('get_week_analitics_for_data_list3.json', 'r', encoding='utf-8') as file:
#     week_analitics = json.load(file)

# with open('get_month_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
#     month_analitics = json.load(file)

# with open('product_data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)


# with open('get_every_day_analitic2.json', 'r', encoding='utf-8') as file:
#     every_day_analitics = json.load(file)

# today = datetime.now() - timedelta(days=2)

# every_day_dict = {today.strftime('%Y-%m-%d'): {}}
# for every_day_data in every_day_analitics:
#     product_id = every_day_data['dimensions'][0]['id']
#     if product_id:
#         metrics = every_day_data.get('metrics', [])
#         if any(metric != 0 for metric in metrics):
#             every_day_dict[today.strftime('%Y-%m-%d')][product_id] = metrics
    

       
# try:
#     with open('store_sales/2be_store.json', 'r', encoding='utf-8') as file:
#         day_data = json.load(file)
#     day_data.update(every_day_dict)
#     with open('store_sales/2be_store.json', 'w', encoding='utf-8') as file:
#         json.dump(day_data, file, indent=2, ensure_ascii=False)   
# except:
#     with open('store_sales/2be_store.json', 'w', encoding='utf-8') as file:
#         json.dump(every_day_dict, file, indent=2, ensure_ascii=False)

# data_to_data_sheet = copy.deepcopy(data)
# data_to_total_sheet = copy.deepcopy(data)


# week_dict = {}
# for item in week_analitics:
#     product_id = item['dimensions'][0]['id']
#     if product_id:
#         week_dict[product_id] = item.get('metrics', [])


# month_dict = {}
# for item in month_analitics:
#     product_id = item['dimensions'][0]['id']
#     if product_id:
#         month_dict[product_id] = item.get('metrics', [])

# for product in data_to_data_sheet:
#     product_id = product['Ozon Product ID']
#     fbo_id = product['fbo_sku']
    
#     every_day_metrics_for_fbs = every_day_dict[today.strftime('%Y-%m-%d')].get(str(product_id), [0, 0])
#     every_day_metrics_for_fbo = every_day_dict[today.strftime('%Y-%m-%d')].get(str(fbo_id), [0, 0])
#     total_every_day_metrics = [x + y for x, y in zip(every_day_metrics_for_fbs, every_day_metrics_for_fbo)]
    
#     month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
#     month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
#     total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
    
#     week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
#     week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
#     total_week_metrics = [x + y for x, y in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo)]
    
#     product['Заказов за неделю'] = total_week_metrics[0]
#     product['Уникальные посетители, всего'] = total_week_metrics[3]
#     product['Уникальные посетители с просмотром карточки товара'] = total_week_metrics[2]
#     product['Общая конверсия в корзину (за неделю)'] = total_week_metrics[1]
#     product['Позиция в поиске и каталоге'] = round(total_week_metrics[4], 2)
    
#     product['Заказов за последний месяц'] = total_month_metrics[0]
    
#     product['Продано за вчера'] = total_every_day_metrics[1]
#     product['Прдано на сумму'] = total_every_day_metrics[0]
    
    
# for product_item in data_to_total_sheet:
#     product_id = (product_item['Ozon Product ID'])
#     fbo_id = product_item['fbo_sku']
#     month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
#     month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
#     total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
#     product_item['Оборот за 30 дней руб'] = total_month_metrics[1]
#     product_id = str(product_id)
#     fbo_id = str(fbo_id)
#     if product_id in weekly_sales['week1'] or product_id in weekly_sales['week2']:
#         product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = weekly_sales['week1'].get(product_id, 0)
#         product_item['Продажи ПН- ВСКР (прошлая) деньги'] = weekly_sales['week2'].get(product_id, 0)
#     else:
#         product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
#         product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
    
# with open('data_to_total_sheet2.json', 'a+', encoding='utf-8') as file:
#         json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
    
    
    
    




# two_week_dict = {}
# sales_data = []

# for two_week_analitic_data in two_weeks_analitics:
#     for item in two_week_analitic_data:
#         dimensions = item.get('dimensions', [])
#         if dimensions:
#             product_id = dimensions[0]['id']
#             date = dimensions[1]['id']
#             sales = item['metrics'][0]
#             sales_data.append(
#                 {
#                     'product_id': product_id,
#                     'date': date,
#                     'sales': sales
#                 }
#             )
            
            

# weekly_sales = {'week1': {}, 'week2': {}}
# all_dates = []

# for sale in sales_data:
#     date_str = sale['date']
#     date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#     all_dates.append(date_obj)
    
# all_dates.sort()
# first_date = all_dates[0]
# seven_date = first_date + timedelta(days=6)

# four_day_first_week = first_date + timedelta(days=3)
# four_day_second_week = seven_date + timedelta(days=4)
# print(four_day_first_week)
# print(four_day_second_week)


# print(first_date)
# print(seven_date)
        
# for sale in sales_data:
#     product_id = sale['product_id']
#     date_str = sale['date']
#     date_obj = datetime.strptime(date_str, '%Y-%m-%d')   
#     sales = sale['sales']
#     if first_date <= date_obj <= seven_date:
#         week_key = 'week1'
#     else:
#         week_key = 'week2'
#     if product_id not in weekly_sales[week_key]:
#         weekly_sales[week_key][product_id] = 0
#     weekly_sales[week_key][product_id] += sales






