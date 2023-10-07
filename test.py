from datetime import datetime, timedelta
import json
# from pprint import pprint
# import copy
# import aiofiles
# import aiohttp
# import asyncio
# import os


# from utils import get_first_week_sales, get_second_week_sales, get_first_week_sales_to_thursday, get_second_week_sales_to_thursday, load_json_file

# import copy



# if __name__ == '__main__':
    
#     today = datetime.now() + timedelta(days=2)
#     data = load_json_file('product_data.json')
#     file_path = 'store_sales/voyor_store.json'
#     data_to_total_sheet = copy.deepcopy(data)
#     sales_to_thursday_first = get_first_week_sales_to_thursday(file_path, today)
#     sales_to_thersday_second = get_second_week_sales_to_thursday(file_path, today)
#     # first_week_sales = get_first_week_sales(file_path, today)
#     # second_week_sales = get_second_week_sales(file_path, today)
    
    
#     for product_item in data_to_total_sheet:
#         product_id = str(product_item['Ozon Product ID'])
#         fbo_id = str(product_item['fbo_sku'])
#         sales_to_thersday_first_week_fbo = sales_to_thursday_first.get(product_id, 0)
#         sales_to_thersday_first_week_fbs = sales_to_thursday_first.get(fbo_id, 0)
#         total_sales_to_thesday_first_week = sales_to_thersday_first_week_fbo + sales_to_thersday_first_week_fbs
#         product_item['Продажи пн-чт 1 неделя'] = total_sales_to_thesday_first_week
#         sales_to_thersday_second_week_fbo = sales_to_thersday_second.get(product_id, 0)
#         sales_to_thersday_second_week_fbs = sales_to_thersday_second.get(fbo_id, 0)
#         product_item['Продажи пн-чт 2 неделя'] = sales_to_thersday_second_week_fbo + sales_to_thersday_second_week_fbs
        
        
        
        # month_metrics_for_product_fbs = month_dict.get(product_id, [0, 0])
        # month_metrics_for_product_fbo = month_dict.get(fbo_id, [0, 0])
        # total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
        # product_item['Оборот за 30 дней руб'] = total_month_metrics[1]
        # week_sales_for_fbs = first_week_sales.get(product_id, 0)
        # week_sales_for_fbo = first_week_sales.get(fbo_id, 0)
        # total_first_week_sales = [x + y for x, y in zip(week_sales_for_fbs, week_sales_for_fbo)]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # a = today.weekday()
    # print(a)
    # if today.weekday() == 5:
    #     print('yes')
    # else:
    #     print('no')

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
    

    # with open('store_sales/unistellar_store.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # start_date = datetime.now() - timedelta(days=12)
    # end_date = datetime.now() - timedelta(days=6)
    
    
    # total_sales = {}
    # current_date = start_date
    # while current_date <= end_date:
    #     current_date_str = current_date.strftime('%Y-%m-%d')
    #     daily_sales = data.get(current_date_str, {})
    #     for product_id, metrics in daily_sales.items():
    #         if product_id not in total_sales:
    #             total_sales[product_id] = metrics[0]
    #         total_sales[product_id] += metrics[1]
    #     current_date = current_date + timedelta(days=1)
    # print(total_sales)









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






