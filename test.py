from datetime import datetime, timedelta
import json
from pprint import pprint
import copy





with open('get_week_analitics_for_data_list1.json', 'r', encoding='utf-8') as file:
    week_analitics = json.load(file)

with open('get_month_analitics_for_data_list1.json', 'r', encoding='utf-8') as file:
    month_analitics = json.load(file)

with open('product_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('get_two_week_analitics.json', 'r', encoding='utf-8') as file:
    two_weeks_analitics = json.load(file)





two_week_dict = {}
sales_data = []

for two_week_analitic_data in two_weeks_analitics:
    for item in two_week_analitic_data:
        dimensions = item.get('dimensions', [])
        if dimensions:
            product_id = dimensions[0]['id']
            date = dimensions[1]['id']
            sales = item['metrics'][0]
            sales_data.append(
                {
                    'product_id': product_id,
                    'date': date,
                    'sales': sales
                }
            )
            
            

weekly_sales = {'week1': {}, 'week2': {}}
all_dates = []

for sale in sales_data:
    date_str = sale['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    all_dates.append(date_obj)
    
all_dates.sort()
first_date = all_dates[0]
seven_date = first_date + timedelta(days=6)

four_day_first_week = first_date + timedelta(days=3)
four_day_second_week = seven_date + timedelta(days=4)
print(four_day_first_week)
print(four_day_second_week)


print(first_date)
print(seven_date)
        
for sale in sales_data:
    product_id = sale['product_id']
    date_str = sale['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')   
    sales = sale['sales']
    if first_date <= date_obj <= seven_date:
        week_key = 'week1'
    else:
        week_key = 'week2'
    if product_id not in weekly_sales[week_key]:
        weekly_sales[week_key][product_id] = 0
    weekly_sales[week_key][product_id] += sales




data_to_data_sheet = copy.deepcopy(data)
data_to_total_sheet = copy.deepcopy(data)


week_dict = {}
for week_data in week_analitics: 
    for item in week_data:
        product_id = item['dimensions'][0]['id']
        if product_id:
            week_dict[product_id] = item.get('metrics', [])


month_dict = {}
for month_data in month_analitics:
    for item in month_data:
        product_id = item['dimensions'][0]['id']
        if product_id:
            month_dict[product_id] = item.get('metrics', [])

for product in data_to_data_sheet:
    product_id = product['Ozon Product ID']
    fbo_id = product['fbo_sku']
    
    month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
    month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
    total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
    
    week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
    week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
    total_week_metrics = [x + y for x, y in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo)]
    
    product['Заказов за неделю'] = total_week_metrics[0]
    product['Уникальные посетители, всего'] = total_week_metrics[3]
    product['Уникальные посетители с просмотром карточки товара'] = total_week_metrics[2]
    product['Общая конверсия в корзину (за неделю)'] = total_week_metrics[1]
    product['Позиция в поиске и каталоге'] = round(total_week_metrics[4], 2)
    
    product['Заказов за последний месяц'] = total_month_metrics[0]
    
    
for product_item in data_to_total_sheet:
    product_id = (product_item['Ozon Product ID'])
    fbo_id = product_item['fbo_sku']
    month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
    month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
    total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
    product_item['Оборот за 30 дней руб'] = total_month_metrics[1]
    product_id = str(product_id)
    fbo_id = str(fbo_id)
    if product_id in weekly_sales['week1'] or product_id in weekly_sales['week2']:
        product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = weekly_sales['week1'].get(product_id, 0)
        product_item['Продажи ПН- ВСКР (прошлая) деньги'] = weekly_sales['week2'].get(product_id, 0)
    else:
        product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
        product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
    
with open('data_to_total_sheet2.json', 'a+', encoding='utf-8') as file:
        json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
    
    
    
    
    
# # weekly_sales = {'week1': {'839380159': 287053, '839277662': 146289, '966214950': 84761, '652943061': 169122, '654844719': 141315}, 
# #                 'week2': {'839277662': 306842, '300717725': 188676, '321563198': 122013}}