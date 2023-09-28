'''
Voyor  129047  06ef9d66-b383-4498-b75d-b5df7df4ce19
2BE  37611  cc9e2151-f99e-46d4-8ce5-97f2a8c58d2c
Arris  54420  de08b0be-46c5-4c58-a9e2-629257488100
NemoCAM  959685  f29d59fa-d40f-49d7-b6f9-50036014c6a0
Tabi  1173379  d18d07ad-6e0a-460f-9226-d03dfb7b4e61
UniStellar  638885  19841499-7918-4952-983b-5619f5f128e3

'''
# OZON_HEADERS = {"Client-Id": "129047", "Api-Key": '06ef9d66-b383-4498-b75d-b5df7df4ce19'}
ALL_OZON_HEADERS = {
    'Voyor': {"Client-Id": "129047", "Api-Key": '06ef9d66-b383-4498-b75d-b5df7df4ce19'},
    # '2BE': {"Client-Id": "37611", "Api-Key": 'cc9e2151-f99e-46d4-8ce5-97f2a8c58d2c'},
    # 'Arris': {"Client-Id": "54420", "Api-Key": 'de08b0be-46c5-4c58-a9e2-629257488100'},
    # 'NemoCAM': {"Client-Id": "959685", "Api-Key": 'f29d59fa-d40f-49d7-b6f9-50036014c6a0'},
    # 'Tabi': {"Client-Id": "1173379", "Api-Key": 'd18d07ad-6e0a-460f-9226-d03dfb7b4e61'},
    # 'UniStellar': {"Client-Id": "638885", "Api-Key": '19841499-7918-4952-983b-5619f5f128e3'},
}
# for key, value in ALL_OZON_HEADERS.items():

######## Вот это для получения информации о всех товарах в магазине (Артикулы, product ids и остатки) ########
data_for_stocks = {
    "filter": {"visibility": "ALL"},
    "last_id": "",
    "limit": 100,
}