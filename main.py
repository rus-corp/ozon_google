import asyncio



from ozon_async import ozon_main
from analitics import analitics_main
from utils import write_to_file
from google import google_main

from conf import ALL_OZON_HEADERS



def main():
    # for name, key in ALL_OZON_HEADERS.items():
    #     product_data = asyncio.run(ozon_main(name=name, client_id=key['Client-Id'], api_key=key['Api-Key']))
    #     analitic_data = asyncio.run(analitics_main(client_id=key['Client-Id'], api_key=key['Api-Key']))
    google_main()


if __name__ == '__main__':
    main()