import json

def write_to_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f'Data was writing to {filename}')
    except Exception as e:
        print(f'Error writing: {str(e)}')
        
        
        
        
def data_to_write_data_sheet():
    with open('get_week_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
        week_analitics = json.load(file)
    
    with open('get_month_analitics_for_data_list.json', 'r', encoding='utf-8') as file:
        month_analitics = json.load(file)

    with open('product_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for product_item in data:
        product_name = product_item['Наименование товара']
        if product_name in week_analitics:
            values = week_analitics[product_name]
            product_item['Уникальные посетители, всего'] = values[3]
            product_item['Уникальные посетители с просмотром карточки товара'] = values[2]
            product_item['Общая конверсия в корзину (за неделю)'] = values[1]
            product_item['Заказов за неделю'] = values[0]
        if product_name in month_analitics:
            values = month_analitics[product_name]
            product_item['Заказов за последний месяц'] = values[0]
    with open('data_to_data_sheet.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
  
  
        
def data_to_write_total_sheet():
    with open('get_week_analitics_for_total_list.json', 'r', encoding='utf-8') as file:
        week_analitics = json.load(file)
    
    with open('get_month_analitics_for_total_list.json', 'r', encoding='utf-8') as file:
        month_analitics = json.load(file)

    with open('product_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        
    for product_item in data:
        product_name = product_item['Наименование товара']
        if product_name in month_analitics:
            values = month_analitics[product_name]
            product_item['Оборот за 30 дней руб'] = values[0]
    with open('data_to_total_sheet.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)