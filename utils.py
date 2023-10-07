import json
import copy
from datetime import datetime, timedelta




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



def calculate_metrics(product_id, fbo_id, week_dict, 
                      every_day_dict, yesterday_sales, two_days_ago_sales, 
                      three_days_ago_sales, four_days_ago_sales, five_days_ago_sales, six_days_ago_sales, today):
    
    week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
    week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
    total_week_metrics = [x + y for x, y in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo)]
    
    every_day_metrics_for_fbs = every_day_dict[today.strftime('%Y-%m-%d')].get(str(product_id), [0, 0])
    every_day_metrics_for_fbo = every_day_dict[today.strftime('%Y-%m-%d')].get(str(fbo_id), [0, 0])
    total_every_day_metrics = [x + y for x, y in zip(every_day_metrics_for_fbs, every_day_metrics_for_fbo)]
    
    yesterday_sales_for_fbs = yesterday_sales.get(str(product_id), [0, 0])
    yesterday_sales_for_fbo = yesterday_sales.get(str(fbo_id), [0, 0])
    total_yesterday_sales = [x + y for x, y in zip(yesterday_sales_for_fbs, yesterday_sales_for_fbo)]
    
    two_days_ago_sales_for_fbs = two_days_ago_sales.get(str(product_id), [0, 0])
    two_days_ago_sales_for_fbo = two_days_ago_sales.get(str(fbo_id), [0, 0])
    total_two_days_ago_sales = [x + y for x, y in zip(two_days_ago_sales_for_fbs, two_days_ago_sales_for_fbo)]
    
    three_days_ago_sales_for_fbs = three_days_ago_sales.get(str(product_id), [0, 0])
    three_days_ago_sales_for_fbo = three_days_ago_sales.get(str(fbo_id), [0, 0])
    total_three_days_ago_sales = [x + y for x, y in zip(three_days_ago_sales_for_fbs, three_days_ago_sales_for_fbo)]
    
    four_days_ago_sales_for_fbo = four_days_ago_sales.get(str(product_id), [0, 0])
    four_days_ago_sales_for_fbs = four_days_ago_sales.get(str(fbo_id), [0, 0])
    total_four_days_ago_sales = [x + y for x, y in zip(four_days_ago_sales_for_fbo, four_days_ago_sales_for_fbs)]
    
    five_days_ago_sales_for_fbo = five_days_ago_sales.get(str(product_id), [0, 0])
    five_days_ago_sales_for_fbs = five_days_ago_sales.get(str(fbo_id), [0, 0])
    total_five_days_ago_sales = [x + y for x, y in zip(five_days_ago_sales_for_fbo, five_days_ago_sales_for_fbs)]
    
    six_days_ago_sales_for_fbo = six_days_ago_sales.get(str(product_id), [0, 0])
    six_days_ago_sales_for_fbs = six_days_ago_sales.get(str(fbo_id), [0, 0])
    total_six_days_ago_sales = [x + y for x, y in zip(six_days_ago_sales_for_fbo, six_days_ago_sales_for_fbs)]
    
    return (total_week_metrics, total_every_day_metrics, 
            total_yesterday_sales, total_two_days_ago_sales, total_three_days_ago_sales,
            total_four_days_ago_sales, total_five_days_ago_sales, total_six_days_ago_sales)



def get_yesterday_sales(file_path, date):
    with open(file_path, 'r', encoding='utf-8') as file:
        sales_data = json.load(file)
    yesterday = date.strftime('%Y-%m-%d')
    sales_for_yesterday = sales_data.get(yesterday, {})
    return sales_for_yesterday
    

def get_first_week_sales(file_path, today):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    start_day = today - timedelta(days=14)
    end_day = start_day + timedelta(days=6)
    
    total_sales = {}
    current_date = start_day
    while current_date <= end_day:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            total_sales[product_id] += metrics[1]
        current_date = current_date + timedelta(days=1)
    return total_sales


def get_second_week_sales(file_path, today):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    start_day = today - timedelta(days=7)
    end_day = start_day + timedelta(days=6)
    
    total_sales = {}
    current_date = start_day
    while current_date <= end_day:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            total_sales[product_id] += metrics[1]
        current_date = current_date + timedelta(days=1)
    return total_sales


def get_first_week_sales_to_thursday(file_path, today):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    start_day = today - timedelta(days=14)
    end_day = start_day + timedelta(days=3)
    
    total_sales = {}
    current_date = start_day
    while current_date <= end_day:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            total_sales[product_id] += metrics[1]
        current_date = current_date + timedelta(days=1)
    return total_sales

    
    
def get_second_week_sales_to_thursday(file_path, today):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    start_day = today - timedelta(days=7)
    end_day = start_day + timedelta(days=3)
    
    total_sales = {}
    current_date = start_day
    while current_date <= end_day:
        current_date_str = current_date.strftime('%Y-%m-%d')
        daily_sales = data.get(current_date_str, {})
        for product_id, metrics in daily_sales.items():
            if product_id not in total_sales:
                total_sales[product_id] = metrics[0]
            total_sales[product_id] += metrics[1]
        current_date = current_date + timedelta(days=1)
    return total_sales

################## Подготовка для записи данных на листы таблицы ##########################


def data_to_write_data_sheet(file_path, today):
    ############## Читам недельную аналитику ################
    week_analitics = load_json_file('get_week_analitics_for_data_list.json')
    ############## Читам месячную аналитику ################
    month_analitics = load_json_file('get_month_analitics_for_data_list.json')    
    ############## Читам продукты ################
    data = load_json_file('product_data.json')    
    ############## Читам двух недельную аналитику ################
    every_day_analitics = load_json_file('get_every_day_analitics.json')
    
    ###################### копии данных для записи на разные листы ######################
    data_to_data_sheet = copy.deepcopy(data)
    data_to_total_sheet = copy.deepcopy(data)
    
    ###################### недельные метрики для записи ##########################
    week_dict = metrics_dict(week_analitics)
    month_dict = metrics_dict(month_analitics)
    every_day_dict = every_day_analitic_dict(file_path, every_day_analitics, today)

    yesterday = today - timedelta(days=1)
    two_day = today - timedelta(days=2)
    three_day = today - timedelta(days=3)
    four_day = today - timedelta(days=4)
    five_day = today - timedelta(days=5)
    six_day = today - timedelta(days=6)
    
    yesterday_sales = get_yesterday_sales(file_path, yesterday)
    two_days_ago_sales = get_yesterday_sales(file_path, two_day)
    three_days_ago_sales = get_yesterday_sales(file_path, three_day)
    four_days_ago_sales = get_yesterday_sales(file_path, four_day)
    five_days_ago_sales = get_yesterday_sales(file_path, five_day)
    six_days_ago_sales = get_yesterday_sales(file_path, six_day)

    ###################### проходимся по данным для запси в DATA SHEET ################
    for product in data_to_data_sheet:
        product_id = product['Ozon Product ID']
        fbo_id = product['fbo_sku']
        (total_week_metrics, 
         total_every_day_metrics, total_yesterday_sales, 
         total_two_days_ago_sales, total_three_days_ago_sales, total_four_days_ago_sales, 
         total_five_days_ago_sales, total_six_days_ago_sales) = calculate_metrics(
            product_id, fbo_id, week_dict, every_day_dict, 
            yesterday_sales, two_days_ago_sales, three_days_ago_sales, four_days_ago_sales, 
            five_days_ago_sales, six_days_ago_sales, today)
        
        product['Заказов за неделю'] = total_week_metrics[0]
        product['Уникальные посетители, всего'] = total_week_metrics[3]
        product['Уникальные посетители с просмотром карточки товара'] = total_week_metrics[2]
        product['Общая конверсия в корзину (за неделю)'] = total_week_metrics[1]
        product['Позиция в поиске и каталоге'] = round(total_week_metrics[4], 2)
        product['Заказов за последний месяц'] = total_month_metrics[0]
        product['Продано 1 день назад'] = total_every_day_metrics[1]         # это мы получаем из текущей аналитики
        product['Продано 2 дня назад'] = total_yesterday_sales[1]            # это и все остальные, нужно брать из файла
        product['Продано 3 дня назад'] = total_two_days_ago_sales[1]
        product['Продано 4 дня назад'] = total_three_days_ago_sales[1]
        product['Продано 5 дней назад'] = total_four_days_ago_sales[1]
        product['Продано 6 дней назад'] = total_five_days_ago_sales[1]
        product['Продано 7 дня назад'] = total_six_days_ago_sales[1]
        
    
    # if today.weekday() == 0:
    sales_to_thursday_first = get_first_week_sales_to_thursday(file_path, today)
    sales_to_thersday_second = get_second_week_sales_to_thursday(file_path, today)
    first_week_sales = get_first_week_sales(file_path, today)
    # second_week_sales = get_second_week_sales(file_path, today)
        
        
    ###################### проходимся по данным для запси в TOTAL SHEET ################   
    for product_item in data_to_total_sheet:
        product_id = str(product_item['Ozon Product ID'])
        fbo_id = str(product_item['fbo_sku'])
        month_metrics_for_product_fbs = month_dict.get(product_id, [0, 0])
        month_metrics_for_product_fbo = month_dict.get(fbo_id, [0, 0])
        total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
        product_item['Оборот за 30 дней руб'] = total_month_metrics[1]
        sales_to_thersday_first_week_fbs = sales_to_thursday_first.get(product_id, 0)
        sales_to_thersday_first_week_fbo = sales_to_thursday_first.get(fbo_id, 0)
        product_item['Продажи пн-чт 1 неделя'] = sales_to_thersday_first_week_fbo + sales_to_thersday_first_week_fbs
        
        sales_to_thersday_second_week_fbs = sales_to_thersday_second.get(product_id, 0)
        sales_to_thersday_second_week_fbo = sales_to_thersday_second.get(fbo_id, 0)
        product_item['Продажи пн-чт 2 неделя'] = sales_to_thersday_second_week_fbo + sales_to_thersday_second_week_fbs
        sales_first_week_fbs = first_week_sales.get(product_id, 0)
        sales_first_week_fbo = first_week_sales.get(fbo_id, 0)
        product_item['Продажи пн-вскр 1 неделя'] = sales_first_week_fbs + sales_first_week_fbo
        # product_item['Продажи пн-вскр 2 неделя'] = 
        
        
        

    with open('data_to_data_sheet.json', 'a+', encoding='utf-8') as file:
            json.dump(data_to_data_sheet, file, indent=2, ensure_ascii=False)

    with open('data_to_total_sheet.json', 'a+', encoding='utf-8') as file:
            json.dump(data_to_total_sheet, file, indent=2, ensure_ascii=False)
            
            
            
            

























# def calculate_sales_by_week(sales_data):
#     weekly_sales = {'week1': {}, 'week2': {}}
#     all_dates = []
#     ####################### добавляем даты для последующего взятия первой даты чтоб разделить по неделям ################
#     for sale in sales_data:
#         date_str = sale['date']
#         date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#         all_dates.append(date_obj)
        
#     all_dates.sort()
#     first_date = all_dates[0]
#     seven_date = first_date + timedelta(days=6)
        
#     ######################### формируем даты для разделоения родаж по неделям #############################
#     for sale in sales_data:
#         product_id = sale['product_id']
#         date_str = sale['date']
#         date_obj = datetime.strptime(date_str, '%Y-%m-%d')   
#         sales = sale['sales'][0]
        
#         if first_date <= date_obj <= seven_date:
#             week_key = 'week1'
#         else:
#             week_key = 'week2'
#         if product_id not in weekly_sales[week_key]:
#             weekly_sales[week_key][product_id] = 0
#         weekly_sales[week_key][product_id] += sales
#     return weekly_sales



    ################## достаем даты из двух недельной аналитики ###############
    # sales_data = []
    # filtered_sales_data = [item for item in two_weeks_analitics if item.get('metrics', [0])[0] != 0]
    
    # for two_week_analitic_data in filtered_sales_data:
    #     dimensions = two_week_analitic_data.get('dimensions', [])
    #     if dimensions:
    #         product_id = dimensions[0]['id']
    #         date = dimensions[1]['id']
    #         sales = two_week_analitic_data['metrics']
    #         sales_data.append(
    #             {
    #                 'product_id': product_id,
    #                 'date': date,
    #                 'sales': sales
    #             }
    #         )
    # weekly_sales = calculate_sales_by_week(sales_data)
    # weekly_sales_to_thursday = calcualte_sales_from_monday_to_thursday(sales_data)
    
    
    
    
    
    
        # if product_id in weekly_sales['week1']:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(product_id, 0)
        # elif product_id in weekly_sales['week2']:
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        # if fbo_id in weekly_sales['week1']:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (позапрошлая) деньги', 0) + weekly_sales['week1'].get(fbo_id, 0)
        # elif fbo_id in weekly_sales['week2']:
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи ПН- ВСКР (прошлая) деньги', 0) + weekly_sales['week2'].get(fbo_id, 0)
        # else:
        #     product_item['Продажи ПН- ВСКР (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        # if product_id in weekly_sales_to_thursday['week1']:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
        # elif product_id in weekly_sales_to_thursday['week2']:
        #     product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
        #     product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = 0
            
        # if fbo_id in weekly_sales_to_thursday['week1']:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(fbo_id, 0)
        # elif fbo_id in weekly_sales_to_thursday['week2']:
        #     product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(fbo_id, 0)
        # else:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
        #     product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = 0

        # if product_id in weekly_sales_to_thursday['week1'] or product_id in weekly_sales_to_thursday['week2']:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
        #     product_item['Продажи Текущая ПН-ЧТ (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
            
        # if fbo_id in weekly_sales_to_thursday['week1'] or fbo_id in weekly_sales_to_thursday['week2']:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = product_item.get('Продажи Прошлая ПН-ЧТ (позапрошлая) деньги', 0) + weekly_sales_to_thursday['week1'].get(product_id, 0)
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = product_item.get('Продажи Текущая ПН-ЧТ (прошлая) деньги', 0) + weekly_sales_to_thursday['week2'].get(product_id, 0)
        # else:
        #     product_item['Продажи Прошлая ПН-ЧТ (позапрошлая) деньги'] = 0
        #     product_item['Продажи ПН- ВСКР (прошлая) деньги'] = 0
        
        
    # for week_data in week_analitics: 
    #     product_id = week_data['dimensions'][0]['id']
    #     if product_id:
    #         week_dict[product_id] = week_data.get('metrics', [])
    # for month_data in month_analitics:
    #     product_id = month_data['dimensions'][0]['id']
    #     if product_id:
    #         month_dict[product_id] = month_data.get('metrics', [])
    
    
        #     ################### данные за 30 дней для записи в DATA SHEET #################
        # month_metrics_for_product_fbs = month_dict.get(str(product_id), [0, 0])
        # month_metrics_for_product_fbo = month_dict.get(str(fbo_id), [0, 0])
        # total_month_metrics = [x + y for x, y in zip(month_metrics_for_product_fbs, month_metrics_for_product_fbo)]
        # ################### данные за 7 дней для записи в DATA SHEET #################
        # week_metrics_for_product_fbs = week_dict.get(str(product_id), ([0] * 5))
        # week_metrics_for_product_fbo = week_dict.get(str(fbo_id), ([0] * 5))
        # total_week_metrics = [x + y for x, y in zip(week_metrics_for_product_fbs, week_metrics_for_product_fbo)]
        
        # every_day_metrics_for_fbs = every_day_dict[today.strftime('%Y-%m-%d')].get(str(product_id), [0, 0])
        # every_day_metrics_for_fbo = every_day_dict[today.strftime('%Y-%m-%d')].get(str(fbo_id), [0, 0])
        # total_every_day_metrics = [x + y for x, y in zip(every_day_metrics_for_fbs, every_day_metrics_for_fbo)]