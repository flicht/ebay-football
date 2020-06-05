import requests
from bs4 import BeautifulSoup
import json
import datetime
import csv
from time import sleep
from loguru import logger



url = f'https://www.ebay.co.uk/itm/'
n = 0

while n < 100:
    with open('player_ids.json', 'r') as f:
        player_team_ids = json.loads(f.read())
        now = datetime.datetime.now()
        with open(f'data/{now.year}-{now.month}-{now.day}-{now.hour}.csv', 'w+') as d:
            csv_writer = csv.writer(d)
            for team, player_idx in player_team_ids.items():
                sleep(.1)
                for player_id in player_idx:
                    try:
                        res = requests.get(url + player_id)
                        soup = BeautifulSoup(res.text, features="html.parser")
                        sold = soup.find_all("a", class_='vi-txt-underline')
                        number_sold = 0
                        if sold != []:
                            number_sold = int(sold[0].text.split(' ')[0])
                        name = ''
                        if name != []:
                            name = soup.find('title').text.replace('Win An', '').replace('Win A', '').replace('Signed Shirt  | eBay', '').strip().replace(team.upper().replace('-', ' ') , '').strip()
                        logger.info(f'{name} Sold:{number_sold}')
                        csv_writer.writerow([team, player_id, name, number_sold])
                    except AttributeError as e:
                        logger.info(e)
                        print(soup.find('title'))
                        continue


    n+=1
    sleep(2000)






