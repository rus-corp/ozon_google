import json
from pprint import pprint
import copy





with open('get_week_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
    week_analitics = json.load(file)

with open('get_month_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
    month_analitics = json.load(file)

with open('product_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


month_dict = {}
for item in month_analitics:
    key = item[0]
    value = item[1]
    month_dict[key] = value
    
week_dict = {}
for item in week_analitics:
    key = item[0]
    value = item[1]
    week_dict[key] = value


data_to_data_sheet = copy.deepcopy(data)
data_to_total_sheet = copy.deepcopy(data)

for product_item in data_to_data_sheet:
    product_name = product_item['Наименование товара']
    if product_name in week_dict:
        values = week_dict[product_name]
        product_item['Заказов за неделю'] = values[0]
        product_item['Общая конверсия в корзину (за неделю)'] = values[1]
        product_item['Уникальные посетители с просмотром карточки товара'] = values[2]
        product_item['Уникальные посетители, всего'] = values[3]
    if product_name in month_analitics:
        values = month_analitics[product_name]
        product_item['Заказов за последний месяц'] = values[0]

for product_item in data_to_total_sheet:
    product_name = product_item['Наименование товара']
    if product_name in month_dict:
        values = month_dict[product_name]
        product_item['Оборот за 30 дней руб'] = values[2]


with open('data_to_data_sheet.json', 'a+', encoding='utf-8') as file:
        json.dump(data_to_data_sheet, file, indent=2, ensure_ascii=False)

with open('data_to_total_sheet.json', 'a+', encoding='utf-8') as file:
        json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
    
