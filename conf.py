base_url = "https://api-seller.ozon.ru"


ALL_OZON_HEADERS = {
    'Voyor': {"Client-Id": "129047", "Api-Key": '06ef9d66-b383-4498-b75d-b5df7df4ce19'},
    '2BE': {"Client-Id": "37611", "Api-Key": 'cc9e2151-f99e-46d4-8ce5-97f2a8c58d2c'},
    # 'Arris': {"Client-Id": "54420", "Api-Key": 'de08b0be-46c5-4c58-a9e2-629257488100'},
    # 'NemoCAM': {"Client-Id": "959685", "Api-Key": 'f29d59fa-d40f-49d7-b6f9-50036014c6a0'},
    # 'Tabi': {"Client-Id": "1173379", "Api-Key": 'd18d07ad-6e0a-460f-9226-d03dfb7b4e61'},
    # 'UniStellar': {"Client-Id": "638885", "Api-Key": '19841499-7918-4952-983b-5619f5f128e3'},
}


SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1ukxmf8Y8OTbLeJ43cnv2hhX4GKzYAjK2kJ6uIomgceU/edit#gid=0'

credentials = {
  "type": "service_account",
  "project_id": "ozon-12345",
  "private_key_id": "61d56c24ef03eefe4f90f21d81ea142a6c9abd33",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCepnpMzuCF8Zro\nXeCiufVMMVijjDdoAO1WzJPV5UQyPqZIPniQ+juJeWT797lNpikQfbIK+SA5OWo1\nInowNj9zE8pcMaXxs6DWu7FUJ1J9XpDS/nYqHF5X6jJnDI0p3PC1Nx9ykbhynJgM\nahf2GDKgl51AnrV6RpHWDLjLNkqa8Ilces7EeJxfz+57HbhFtGHji4dW7phELYcO\noHFEoVgTSHftAPMasEPiGvQkKN5Jah9X88jQDuEa+MmcXtMslvV4oOaYKdkq42Sk\nrII5Iczo0RdMYQg472m5reQ9zlI6qrAHHjUGVzw9w2hA42ECVB/0pWDSyKsvk/fa\nA0CIkiVtAgMBAAECggEAJZ+pZUmyaVFwwSZyPWUITTduo+p+wUVnA6ykapdiYuAE\noyFdilQthl6pmi+XXFjJaEXG0V9fSvLYwx0YCRL0XSAWX2LOzdEhlYsRdLmWkHC6\nu67o6verUAIUTefmGkVxOCiIZq00JsoILPmEETKP3xHVkxuQQh02PKLruBV5/+An\nV965azJ40ztEtFXZTmJ+7vUzsai8qruYv1qr6qBu9KaALOr9qpPix4PjJhS+S7IG\nLSNmN758Aj4Gg3eWNIjAqUCAKdGweoabSR+4v2csvjMX8vbAi4Cygqv3moE1YQzr\npO6IoK1m2s+FlkYFw1AMHzr0+KwZuH7Uqysl17zd6QKBgQDcs+qf3MZZtdF5+on4\n5DTgdgUMk0Wk6vqdwFMhN0zJ77t0aDcOtQX2hH9oxSMMOETMYycZp2qTRjo+ebIu\nv/9Dwr8FGiZYB1+7Ma63NDzABOiCT90qvM9hdL37qaW1lSaO6cPNYS/PggWrdXC6\nepG5qFWGeZk1zoTfxej0urq54wKBgQC4Bf0J4OEBktVgUJHxDhb0q+JYyS/yEogk\nuChL+owJwY3sK/SCwt5L/e4fHvu72y4OWYvUf02ilNWXVSyhls9IQoegbLAnXZMu\nYOwJ9GQ9p/znxWxAzcU1UBBiwawnukPpefP1nAc/RL6vr9CrUWgUSC0gsBJDuWcq\nGS3QjLwEbwKBgQC/i8ry6dqgW4OtuPrsL6uQr/1b16mXI3VVWmkLqAIWNOFde2Fl\ne0jsljw6AvaTEXbsaJWz1zBRF59PP7Gcj3gNKEU/OV3UArpcLhdz23tqMBhXmNbb\n07is3XRRqgAu437uhAYzBslG8JLZJ3kp71zwZB+uMXT+VPnPeOXhGPscfwKBgQCf\nVJgFAI7wlNhofvoNU1yu1U+x/eekWUVFPamuNy0emVYvINOgj+Z2t1J/4Yyl1xzm\nUcPO5bYrSWAxmg59jhzEfM3/KXvPaaawZjyYVeCgvZ0sc3PKHB9ejIbTasqKzyxT\nr0J56nEf536OkNREMMTDosZn4eq+dn2LJqfTRLbZwwKBgQCNKozpuHhouwRQ9M9p\nIPC3SJTzO2tALqrC8XZEyxA62OvwdXE9R7MdqgEpPdsDZOT+GdJkvI03acw/wmGC\nrEN0nLCIo/RWscJ+BI+3jXWRcyEobMZYXVgWuwPcdjMHoAuw+tu2gUJ2VQJkwyn9\nRWYmAFO2QaeTIN+zNEQyvl5roQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "ozon-service@ozon-12345.iam.gserviceaccount.com",
  "client_id": "111002957115872161358",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ozon-service%40ozon-12345.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}




delivery = {
  "0-1.9": 58,
  "1.901-2.9": 61,
  "2.901-4.9": 63,
  "4.901-5.9": 67,
  "5.901-6.9": 69,
  "6.901-7.9": 71,
  "7.901-8.4": 73,
  "8.401-8.9": 75,
  "8.901-9.4": 76,
  "9.401-9.9": 77,
  "9.901-14.9": 85,
  "14.901-19.9": 111,
  "19.901-24.9": 126,
  "24.901-29.9": 141,
  "29.901-34.9": 166,
  "34.901-39.9": 191,
  "39.901-44.9": 216,
  "44.901-49.9": 231,
  "49.901-54.9": 271,
  "54.901-59.9": 296,
  "59.901-64.9": 321,
  "64.901-69.9": 356,
  "69.901-74.9": 376,
  "74.901-99.9": 406,
  "99.901-124.9": 531,
  "124.901-149.9": 706,
  "149.901-174.9": 906,
  "174.901-999999.0": 1106,
}


column_indexes_for_data = {
    "Магазин": 6,
    "Ozon Product ID": 3,
    "Артикул": 1,
    "Наименование товара": 5,
    "Общее кол-во стоков в ЛК.": 7,
    "Статус": 4,
    "Комиссия + Логистика": 12,
    "Текущая цена продажи": 15,
    "Цена с учётом скидки озон": 14,
    "Уникальные посетители, всего": 18,
    "Уникальные посетители с просмотром карточки товара": 19,
    "Общая конверсия в корзину (за неделю)": 21,
    "Заказов за неделю": 22,
    "Заказов за последний месяц": 23,
    "Позиция в поиске и каталоге": 24,
    "Продано 1 день назад": 26,
    "Продано 2 дня назад": 27,
    "Продано 3 дня назад": 28,
    "Продано 4 дня назад": 29,
    "Продано 5 дней назад": 30,
    "Продано 6 дней назад": 31,
    "Продано 7 дней назад": 32
}


column_indexes_for_total = {
  'Артикул': 1,
  'Оборот за 30 дней руб': 5,
  'Продажи пн-чт 1 неделя': 7,
  'Продажи пн-чт 2 неделя': 8,
  'Продажи пн-вскр 1 неделя': 10,
  'Продажи пн-вскр 2 неделя': 11
}


def volume_range(volume, delivery):
  for key in delivery:
    range_values = key.split('-')
    min_range = float(range_values[0])
    max_range = float(range_values[1])
    if min_range <= volume <= max_range:
      return delivery[key]
  return None
  