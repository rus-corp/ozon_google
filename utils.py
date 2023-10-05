import json
import copy






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
        

    data_to_data_sheet = copy.deepcopy(data)
    data_to_total_sheet = copy.deepcopy(data)

    for product_item in data_to_data_sheet:
        product_name = product_item['Наименование товара']
        if product_name in week_analitics:
            values = week_analitics[product_name]
            product_item['Заказов за неделю'] = values[0]
            product_item['Общая конверсия в корзину (за неделю)'] = values[1]
            product_item['Уникальные посетители с просмотром карточки товара'] = values[2]
            product_item['Уникальные посетители, всего'] = values[3]
        if product_name in month_analitics:
            values = month_analitics[product_name]
            product_item['Заказов за последний месяц'] = values[0]

    for product_item in data_to_total_sheet:
        product_name = product_item['Наименование товара']
        if product_name in month_analitics:
            values = month_analitics[product_name]
            product_item['Оборот за 30 дней руб'] = values[2]
                    
    with open('data_to_data_sheet.json', 'a+', encoding='utf-8') as file:
        json.dump(data_to_data_sheet, file, indent=2, ensure_ascii=False)
        # try:
        #     existing_data_to_data_sheet = json.load(file)
        # except json.JSONDecodeError:
        #     existing_data_to_data_sheet = []
        # existing_data_to_data_sheet.extend(data_to_data_sheet)
        # file.seek(0)
        # json.dump(existing_data_to_data_sheet, file, indent=2, ensure_ascii=False)

    with open('data_to_total_sheet.json', 'a+', encoding='utf-8') as file:
        json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
        # try:
        #     existing_data_to_total_sheet = json.load(file)
        # except:
        #     existing_data_to_total_sheet = []
        # existing_data_to_total_sheet.extend(data_to_total_sheet)
        # file.seek(0)
        # json.dump(existing_data_to_total_sheet, file, indent=2, ensure_ascii=False)