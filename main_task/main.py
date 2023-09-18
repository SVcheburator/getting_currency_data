import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta


def get_links(days_range):
    link_base = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    links = []
    now = datetime.now()

    for d in range(days_range):
        date = (now - timedelta(days=d)).strftime('%d.%m.%Y')
        link = link_base + date
        links.append(link)
    
    return links



async def main_func(links, currencies):

    async with aiohttp.ClientSession() as session:
        result = []
        for link in links:
            print(link)

            async with session.get(link) as response:
                try:
                    if response.status == 200:
                        json_resp = await response.json()
                        date = link[-10:]
                        vrapper_dct = {}
                        vrapper_dct[date] = {}
                        

                        for cur_data in json_resp['exchangeRate']:
                            if cur_data['currency'] in currencies:
                                vrapper_dct[date][cur_data['currency']] = {'sale': cur_data['saleRate'], 'purchase': cur_data['purchaseRate']}

                        result.append(vrapper_dct)
                        
                    else:
                        print(f"Error status: {response.status}")
                except aiohttp.ClientConnectorError as err:
                    print(f'Connection error:', str(err))
            
        return result
            

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    days = int(input('How many days to show?(1-10) >>> '))
    if 1 <= days <= 10:
        links = get_links(days)
        currencies = ['EUR', 'USD']
        r = asyncio.run(main_func(links, currencies))
        print(r)
    else:
        print('I can only show you info for last 10 days!')