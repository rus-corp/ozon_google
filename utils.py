import json
import copy
from datetime import datetime, timedelta




def write_to_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f'Data was writing to {filename}')
    except Exception as e:
        print(f'Error writing: {str(e)}')
        


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
        

        
def calculate_sales_by_week(sales_data):
    weekly_sales = {'week1': {}, 'week2': {}}
    all_dates = []
    ####################### добавляем даты для последующего взятия первой даты чтоб разделить по неделям ################
    for sale in sales_data:
        date_str = sale['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        all_dates.append(date_obj)
        
    all_dates.sort()
    first_date = all_dates[0]
    seven_date = first_date + timedelta(days=6)
        
    ######################### формируем даты для разделоения родаж по неделям #############################
    for sale in sales_data:
        product_id = sale['product_id']
        date_str = sale['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')   
        sales = sale['sales'][0]
        
        if first_date <= date_obj <= seven_date:
            week_key = 'week1'
        else:
            week_key = 'week2'
        if product_id not in weekly_sales[week_key]:
            weekly_sales[week_key][product_id] = 0
        weekly_sales[week_key][product_id] += sales
    return weekly_sales

    
    
def calcualte_sales_from_monday_to_thursday(sales_data):
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
    for sale in sales_data:
        product_id = sale['product_id']
        date_str = sale['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')   
        sales = sale['sales'][0]
        if first_date <= date_obj <= four_day_first_week:
            week_key = 'week1'
        elif seven_date < date_obj <= four_day_second_week:
            week_key = 'week2'
        else:
            continue
        
        if product_id not in weekly_sales[week_key]:
            weekly_sales[week_key][product_id] = 0
        weekly_sales[week_key][product_id] += sales
    return weekly_sales
    
    
    
################## Подготовка для записи данных на листы таблицы ##########################
def data_to_write_data_sheet():
    ############## Читам недельную аналитику ################
    week_analitics = load_json_file('get_week_analitics_for_data_list.json')
    ############## Читам месячную аналитику ################
    month_analitics = load_json_file('get_month_analitics_for_data_list.json')    
    ############## Читам продукты ################
    data = load_json_file('product_data.json')    
    ############## Читам двух недельную аналитику ################
    two_weeks_analitics = load_json_file('get_two_week_analitics.json')
    
    ################## достаем даты из двух недельной аналитики ###############
    sales_data = []
    filtered_sales_data = [item for item in two_weeks_analitics if item.get('metrics', [0])[0] != 0]
    
    for two_week_analitic_data in filtered_sales_data:
        dimensions = two_week_analitic_data.get('dimensions', [])
        if dimensions:
            product_id = dimensions[0]['id']
            date = dimensions[1]['id']
            sales = two_week_analitic_data['metrics']
            sales_data.append(
                {
                    'product_id': product_id,
                    'date': date,
                    'sales': sales
                }
            )
    weekly_sales = calculate_sales_by_week(sales_data)
    weekly_sales_to_thursday = calcualte_sales_from_monday_to_thursday(sales_data)
    ###################### копии данных для записи на разные листы ######################
    data_to_data_sheet = copy.deepcopy(data)
    data_to_total_sheet = copy.deepcopy(data)
    ###################### недельные метрики для записи ##########################
    week_dict = {}
    for week_data in week_analitics: 
        product_id = week_data['dimensions'][0]['id']
        if product_id:
            week_dict[product_id] = week_data.get('metrics', [])

    ###################### месячные метрики для записи ##########################
    month_dict = {}
    for month_data in month_analitics:
        product_id = month_data['dimensions'][0]['id']
        if product_id:
            month_dict[product_id] = month_data.get('metrics', [])
    ###################### проходимся по данным для запси в DATA SHEET ################
    for product in data_to_data_sheet:
        product_id = product['Ozon Product ID']
        fbo_id = product['fbo_sku']
        ################### данные за 30 дней для записи в DATA SHEET #################
        month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
        month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
        total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
        ################### данные за 7 дней для записи в DATA SHEET #################
        week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
        week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
        total_week_metrics = [x + y for x, y in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo)]
        product['Заказов за неделю'] = total_week_metrics[0]
        product['Уникальные посетители, всего'] = total_week_metrics[3]
        product['Уникальные посетители с просмотром карточки товара'] = total_week_metrics[2]
        product['Общая конверсия в корзину (за неделю)'] = total_week_metrics[1]
        product['Позиция в поиске и каталоге'] = round(total_week_metrics[4], 2)
        product['Заказов за последний месяц'] = total_month_metrics[0]
        
    ###################### проходимся по данным для запси в TOTAL SHEET ################   
    for product_item in data_to_total_sheet:
        product_id = str(product_item['Ozon Product ID'])
        fbo_id = str(product_item['fbo_sku'])
        month_metrics_for_product_fbs = month_dict.get(product_id, [0, 0])
        month_metrics_for_product_fbo = month_dict.get(fbo_id, [0, 0])
        total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
        product_item['Оборот за 30 дней руб'] = total_month_metrics[1]
        
        if product_id in weekly_sales['week1']:
            product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(product_id, 0)
        elif product_id in weekly_sales['week2']:
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(product_id, 0)
        else:
            product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        if fbo_id in weekly_sales['week1']:
            product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(fbo_id, 0)
        elif fbo_id in weekly_sales['week2']:
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(fbo_id, 0)
        else:
            product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        if product_id in weekly_sales_to_thursday['week1']:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
        elif product_id in weekly_sales_to_thursday['week2']:
            product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        else:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
            product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = 0
            
        if fbo_id in weekly_sales_to_thursday['week1']:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(fbo_id, 0)
        elif fbo_id in weekly_sales_to_thursday['week2']:
            product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(fbo_id, 0)
        else:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
            product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = 0
        
            
            
            
            
            
            
            
    
        
        # if product_id in weekly_sales['week1'] or fbo_id in weekly_sales['week1']:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(product_id, 0)      
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(product_id, 0)
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        # if fbo_id in weekly_sales['week1'] or fbo_id in weekly_sales['week2']:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(product_id, 0)
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0


        if product_id in weekly_sales_to_thursday['week1'] or product_id in weekly_sales_to_thursday['week2']:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
            product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        else:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        if fbo_id in weekly_sales_to_thursday['week1'] or fbo_id in weekly_sales_to_thursday['week2']:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        else:
            product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
            product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
        






    with open('data_to_data_sheet.json', 'a+', encoding='utf-8') as file:
            json.dump(data_to_data_sheet, file, indent=2, ensure_ascii=False)

    with open('data_to_total_sheet.json', 'a+', encoding='utf-8') as file:
            json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
            
            
            
            
