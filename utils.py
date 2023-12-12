import json
import copy
from datetime import datetime, timedelta
import logging
from itertools import zip_longest




logger = logging.getLogger('ozon.utils')


def load_every_day_analitic_to_file(file_path, data):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            day_data = json.load(file)
        day_data.update(data)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(day_data, file, indent=2, ensure_ascii=False)   
    except:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def data_to_load_total_sheet(file_path, extend_data):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.extend(extend_data)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(extend_data, file, indent=2, ensure_ascii=False)



def total_sheet_data():
    with open('for_total_sheet.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data_dict = {}
    for item in data:
        article = item['Артикул']
        if article in data_dict:
            data_dict[article]['Оборот за 30 дней руб'] += item['Оборот за 30 дней руб']
            data_dict[article]['Продажи пн-чт 1 неделя'] += item['Продажи пн-чт 1 неделя']
            data_dict[article]['Продажи пн-чт 2 неделя'] += item['Продажи пн-чт 2 неделя']
            
            data_dict[article]['Продажи пн-вскр 1 неделя'] += item['Продажи пн-вскр 1 неделя']
            data_dict[article]['Продажи пн-вскр 2 неделя'] += item['Продажи пн-вскр 2 неделя']
        else:
            data_dict[article] = {
                'Оборот за 30 дней руб': item['Оборот за 30 дней руб'],
                'Продажи пн-чт 1 неделя': item['Продажи пн-чт 1 неделя'],
                'Продажи пн-чт 2 неделя': item['Продажи пн-чт 2 неделя'],
                'Продажи пн-вскр 1 неделя': item['Продажи пн-вскр 1 неделя'],
                'Продажи пн-вскр 2 неделя': item['Продажи пн-вскр 2 неделя']
            }
    
    total_data = []
    for articl, values in data_dict.items():
        data_entry = {
            'Артикул': articl,
            'Оборот за 30 дней руб': values.get('Оборот за 30 дней руб', 0),
            'Продажи пн-чт 1 неделя': values.get('Продажи пн-чт 1 неделя', 0),
            'Продажи пн-чт 2 неделя': values.get('Продажи пн-чт 2 неделя', 0),
            'Продажи пн-вскр 1 неделя': values.get('Продажи пн-вскр 1 неделя', 0),
            'Продажи пн-вскр 2 неделя': values.get('Продажи пн-вскр 2 неделя', 0)
        }
        total_data.append(data_entry)
    
    with open('data_to_total_sheet.json', 'w', encoding='utf-8') as file:
        json.dump(total_data, file, indent=2, ensure_ascii=False)



def write_to_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Error writing: {str(e)}')
        


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
        

def metrics_dict(data):
    data_dict = {}
    for item in data:
        product_id = item['dimensions'][0]['id']
        if product_id:
            data_dict[product_id] = item.get('metrics', [])
    return data_dict
            
            
def every_day_analitic_dict(file_path, data, today):
    every_day_dict = {today.strftime('%Y-%m-%d'): {}}
    for every_day_data in data:
        product_id = every_day_data['dimensions'][0]['id']
        if product_id:
            metrics = every_day_data.get('metrics', [])
            if any(metric != 0 for metric in metrics):
                every_day_dict[today.strftime('%Y-%m-%d')][product_id] = metrics
    load_every_day_analitic_to_file(file_path, every_day_dict)
    return every_day_dict



def get_yesterday_sales(file_path, date):
    with open(file_path, 'r', encoding='utf-8') as file:
        sales_data = json.load(file)
    yesterday = date.strftime('%Y-%m-%d')
    sales_for_yesterday = sales_data.get(yesterday, {})
    return sales_for_yesterday



def calculate_metrics(product_id, fbo_id, sku, data_dict, today=None):
    default_value = 0
    metrics_for_product_fbs = data_dict.get(str(product_id), ([0] * 5))
    metrics_for_product_fbo = data_dict.get(str(fbo_id), ([0] * 5))
    metrics_for_product_sku = data_dict.get(str(sku), ([0] * 5))
    total_metrics = [sum(x) for x in zip_longest(metrics_for_product_fbs, metrics_for_product_fbo, metrics_for_product_sku, fillvalue=default_value)]
    return total_metrics


# ============================== Недельные продажи ============================
def get_first_week_sales(file_path, day):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    current_day_of_week = day.weekday()
    if current_day_of_week == 0:
        pass
    else:
        correction = timedelta(days=current_day_of_week)
        day -= correction
    
    start_day = day - timedelta(days=14)
    end_day = start_day + timedelta(days=6)
    logger.info(f' Формирую продажи за 1 неделю (пн-вс) для листа TOTAL за {start_day} - {end_day}')
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


def get_second_week_sales(file_path, day):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    current_day_of_week = day.weekday()
    if current_day_of_week == 0:
        pass
    else:
        correction = timedelta(days=current_day_of_week)
        day -= correction
        
    start_day = day - timedelta(days=7)
    end_day = start_day + timedelta(days=6)
    logger.info(f' Формирую продажи за неделю (пн-вс) для листа TOTAL за {start_day} - {end_day}')
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


def get_first_week_sales_to_thursday(file_path, day):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    current_day_of_week = day.weekday()
    days_to_last_week = current_day_of_week + 7
    start_day = day - timedelta(days=days_to_last_week)
    end_day = start_day + timedelta(days=3)
    logger.info(f' Формирую продажи (пн-чт) для листа TOTAL за {start_day} - {end_day}')
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

    
    
def get_second_week_sales_to_thursday(file_path, day):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    current_day_of_week = day.weekday()
    if current_day_of_week == 0:
        start_day = day
    else:
        start_day = day - timedelta(days=current_day_of_week)
        
    if 0 < current_day_of_week < 4:
        end_day = day
    elif current_day_of_week == 0:
        end_day = day
    else:
        end_day = start_day + timedelta(days=3)
        
    logger.info(f' Формирую продажи (пн-чт) для листа TOTAL за {start_day} - {end_day}')
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

################## Подготовка для записи данных на листы таблицы ##########################


def data_to_write_data_sheet(file_path, today, product_data: list):
    ############## Читам недельную аналитику ################
    week_analitics = load_json_file('get_week_analitics_for_data_list.json')
    ############## Читам месячную аналитику ################
    month_analitics = load_json_file('get_month_analitics_for_data_list.json')
    ############## Читам продукты ################
    # data = load_json_file('product_data.json')
    ############## Читам двух недельную аналитику ################
    every_day_analitics = load_json_file('get_every_day_analitics.json')
    
    ###################### копии данных для записи на разные листы ######################
    # data_to_data_sheet = copy.deepcopy(product_data)
    
    ###################### недельные метрики для записи ##########################
    week_dict = metrics_dict(week_analitics)
    month_dict = metrics_dict(month_analitics)
    every_day_dict = every_day_analitic_dict(file_path, every_day_analitics, today)

    
    two_day = today - timedelta(days=1)
    three_day = today - timedelta(days=2)
    four_day = today - timedelta(days=3)
    five_day = today - timedelta(days=4)
    six_day = today - timedelta(days=5)
    seven_day = today - timedelta(days=6)

    today_sales = get_yesterday_sales(file_path, today)
    two_days_ago_sales = get_yesterday_sales(file_path, two_day)
    three_days_ago_sales = get_yesterday_sales(file_path, three_day)
    four_days_ago_sales = get_yesterday_sales(file_path, four_day)
    five_days_ago_sales = get_yesterday_sales(file_path, five_day)
    six_days_ago_sales = get_yesterday_sales(file_path, six_day)
    seven_days_ago_sales = get_yesterday_sales(file_path, seven_day)
    logger.info('готовлю данные для записи в data sheet')
    ###################### проходимся по данным для запси в DATA SHEET ################
    for product in product_data:
        product_id = product['Ozon Product ID']
        fbo_id = product['fbo_sku']
        sku = product['SKU']
        total_week_metrics = calculate_metrics(product_id, fbo_id, sku, week_dict)
        total_month_metrics = calculate_metrics(product_id, fbo_id, sku, month_dict)
        total_every_day_metrics = calculate_metrics(product_id, fbo_id, sku, today_sales)
        total_two_days_ago_sales = calculate_metrics(product_id, fbo_id, sku, two_days_ago_sales)
        total_three_days_ago_sales = calculate_metrics(product_id, fbo_id, sku, three_days_ago_sales)
        total_four_days_ago_sales = calculate_metrics(product_id, fbo_id, sku, four_days_ago_sales)
        total_five_days_ago_sales = calculate_metrics(product_id, fbo_id, sku, five_days_ago_sales)
        total_six_days_ago_sales = calculate_metrics(product_id, fbo_id, sku, six_days_ago_sales)
        total_seven_day_ago_sales = calculate_metrics(product_id, fbo_id, sku, seven_days_ago_sales)
        
        product['Заказов за неделю'] = total_week_metrics[0]
        product['Уникальные посетители, всего'] = total_week_metrics[3] if len(total_week_metrics) > 3 else 0
        product['Уникальные посетители с просмотром карточки товара'] = total_week_metrics[2] if len(total_week_metrics) > 2 else 0
        product['Общая конверсия в корзину (за неделю)'] = total_week_metrics[1] if len(total_week_metrics) > 1 else 0
        if len(total_week_metrics) > 4:
            product['Позиция в поиске и каталоге'] = round(total_week_metrics[4], 2) 
        else:
            product['Позиция в поиске и каталоге'] = 0
        product['Заказов за последний месяц'] = total_month_metrics[0]
        product['Продано 1 день назад'] = total_every_day_metrics[1]         # это мы получаем из текущей аналитики
        product['Продано 2 дня назад'] = total_two_days_ago_sales[1]            # это и все остальные, нужно брать из файла
        product['Продано 3 дня назад'] = total_three_days_ago_sales[1]
        product['Продано 4 дня назад'] = total_four_days_ago_sales[1]
        product['Продано 5 дней назад'] = total_five_days_ago_sales[1]
        product['Продано 6 дней назад'] = total_six_days_ago_sales[1]
        product['Продано 7 дней назад'] = total_seven_day_ago_sales[1]
        
        
    total_data = data_to_load_total_sheet('data_to_data_sheet.json', product_data) # здесь создаются дубли!!!!!

    
    


def write_to_total_sheet(file_path, today, product_data):
    # data = load_json_file('product_data.json')
    month_analitics = load_json_file('get_month_analitics_for_data_list.json')
    month_dict = metrics_dict(month_analitics)
    sales_to_thursday_first = get_first_week_sales_to_thursday(file_path, today)
    sales_to_thersday_second = get_second_week_sales_to_thursday(file_path, today)
    
    first_week_sales = get_first_week_sales(file_path, today)
    second_week_sales = get_second_week_sales(file_path, today)
        
    logger.info('готовлю данные для записи в total sheet')
    ###################### проходимся по данным для запси в TOTAL SHEET ################   
    for product_item in product_data:
        product_id = str(product_item['Ozon Product ID'])
        fbo_id = str(product_item['fbo_sku'])
        sku = str(product_item['SKU'])
        month_metrics_for_product_fbs = month_dict.get(product_id, [0, 0])
        month_metrics_for_product_fbo = month_dict.get(fbo_id, [0, 0])
        month_metrics_for_product_sku = month_dict.get(sku, [0, 0])
        total_month_metrics = [sum(x) for x in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo, month_metrics_for_product_sku)]
        product_item['Оборот за 30 дней руб'] = total_month_metrics[1]   
        sales_to_thersday_first_week_fbs = sales_to_thursday_first.get(product_id, 0)
        sales_to_thersday_first_week_fbo = sales_to_thursday_first.get(fbo_id, 0)
        sales_to_thersday_first_week_sku = sales_to_thursday_first.get(sku, 0)
        product_item['Продажи пн-чт 1 неделя'] = sales_to_thersday_first_week_fbs + sales_to_thersday_first_week_fbo + sales_to_thersday_first_week_sku
        
        sales_to_thersday_second_week_fbs = sales_to_thersday_second.get(product_id, 0)
        sales_to_thersday_second_week_fbo = sales_to_thersday_second.get(fbo_id, 0)
        sales_to_thersday_second_week_sku = sales_to_thersday_second.get(sku, 0)
        product_item['Продажи пн-чт 2 неделя'] = sales_to_thersday_second_week_fbs + sales_to_thersday_second_week_fbo + sales_to_thersday_second_week_sku
        
        sales_first_week_fbs = first_week_sales.get(product_id, 0)
        sales_first_week_fbo = first_week_sales.get(fbo_id, 0)
        sales_first_week_sku = first_week_sales.get(sku, 0)
        product_item['Продажи пн-вскр 1 неделя'] = sales_first_week_fbs + sales_first_week_fbo + sales_first_week_sku
        
        sales_second_week_fbs = second_week_sales.get(product_id, 0)
        sales_second_week_fbo = second_week_sales.get(fbo_id, 0)
        sales_second_week_sku = second_week_sales.get(sku, 0)
        product_item['Продажи пн-вскр 2 неделя'] = sales_second_week_fbs + sales_second_week_fbo + sales_second_week_sku

    
    total_data = data_to_load_total_sheet('for_total_sheet.json', product_data) # здесь создаются дубли!!!!!




def clean_sales(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    three_week_ago_date = datetime.now() - timedelta(days=21)
    stop_date = three_week_ago_date + timedelta(days=6)
    
    while three_week_ago_date <=stop_date:
        current_data = three_week_ago_date.strftime('%Y-%m-%d')
        try:
            data.pop(current_data)
        except:
            logger.info(f'при удалении старых продаж, нет продаж за {current_data} for {file_path}')
        three_week_ago_date += timedelta(days=1)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    
    
    
    
    