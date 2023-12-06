import json
import pprint
import asyncio
import aiofiles
from aiohttp import ClientSession
import os





# def calculate(week_dict):
#   week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
#   week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
#   week_metrics_for_product_sku = week_dict.get(str(sku), ([0] * 5))
#   total_week_metrics = [sum(x) for x in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo, week_metrics_for_product_sku)]
#   print(total_week_metrics)



# data_dict = metrics_dict(data)


# calculate(data_dict)

# print(data_dict)



def every_day_analitic_dict(file_path, data, today):
    every_day_dict = {today.strftime('%Y-%m-%d'): {}}
    for every_day_data in data:
        product_id = every_day_data['dimensions'][0]['id']
        if product_id:
            metrics = every_day_data.get('metrics', [])
            if any(metric != 0 for metric in metrics):
                every_day_dict[today.strftime('%Y-%m-%d')][product_id] = metrics
    # load_every_day_analitic_to_file(file_path, every_day_dict)
    return every_day_dict


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
      

def calculate_metrics(product_id, fbo_id, sku, data_dict, today=None):
    if today:
        metrics_for_fbs = data_dict[today.strftime('%Y-%m-%d')].get(str(product_id), ([0] * 5))
        metrics_for_fbo = data_dict[today.strftime('%Y-%m-%d')].get(str(fbo_id), ([0] * 5))
        metrics_for_sku = data_dict[today.strftime('%Y-%m-%d')].get(str(sku), ([0] * 5))
        total_metrics = [sum(x) for x in zip(metrics_for_fbs, metrics_for_fbo, metrics_for_sku)]
    else:
        metrics_for_product_fbs = data_dict.get(str(product_id), ([0] * 5))
        metrics_for_product_fbo = data_dict.get(str(fbo_id), ([0] * 5))
        metrics_for_product_sku = data_dict.get(str(sku), ([0] * 5))
        total_metrics = [sum(x) for x in zip(metrics_for_product_fbs, metrics_for_product_fbo, metrics_for_product_sku)]
    return total_metrics

def data_to_load_total_sheet(extend_data):
    try:
        with open('for_total_sheet.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.extend(extend_data)
        with open('for_total_sheet.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        with open('for_total_sheet.json', 'w', encoding='utf-8') as file:
            json.dump(extend_data, file, indent=2, ensure_ascii=False)

from datetime import datetime, timedelta

# def get_first_week_sales_to_thursday(file_path):
#     # with open(file_path, 'r', encoding='utf-8') as file:
#     #     data = json.load(file)
#     today = datetime.now()
#     current_day_of_week = today.weekday()
#     days_to_last_week = current_day_of_week + 7
#     start_day = today - timedelta(days=days_to_last_week)
#     end_day = start_day + timedelta(days=3)
    
#     total_sales = {}
#     current_date = start_day
#     while current_date <= end_day:
#         current_date_str = current_date.strftime('%Y-%m-%d')
#         daily_sales = data.get(current_date_str, {})
#         for product_id, metrics in daily_sales.items():
#             if product_id not in total_sales:
#                 total_sales[product_id] = metrics[0]
#             else:
#                 total_sales[product_id] += metrics[0]
#         current_date = current_date + timedelta(days=1)
#     return total_sales

    
    
def get_second_week_sales_to_thursday(file_path, day):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    today = datetime.now()
    current_day_of_week = today.weekday()
    if current_day_of_week == 0:
        start_day = today - timedelta(days=7)
    else:
        start_day = today - timedelta(days=current_day_of_week)
    
    if 0 < current_day_of_week < 4:
        end_day = today
    else:
        end_day = start_day + timedelta(days=3)
    
    total_sales = {}
    current_date = start_day
    while current_date <= end_day:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            else:
                total_sales[product_id] += metrics[0]
        current_date = current_date + timedelta(days=1)
    return total_sales
  



import pprint
  
  
if __name__ == '__main__':
  with open('for_total_sheet.json', 'r', encoding='utf-8') as file:
      data = json.load(file)
  
#   print(data)
  data2 = data.copy()
  print(data==data2)
  pprint.pprint(data2)