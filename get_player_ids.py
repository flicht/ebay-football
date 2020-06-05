import requests
from bs4 import BeautifulSoup
import re
import json


base_url =  'https://www.ebay.co.uk/e/special-events/nhs-'
teams = ['afc-bournemouth', 'arsenal', 'aston-villa', 'brighton-and-hove', \
            'burnley', 'chelsea', 'crystal-palace', 'everton', 'leicester-city', \
            'liverpool', 'manchester-city', 'manchester-united', 'newcastle-united', \
            'norwich-city', 'sheffield-united', 'southampton', 'tottenham-hotspur', 'watford', \
            'west-ham-united', 'wolverhampton-wanderers']




with open('player_ids.json', 'w+') as f:
    dict_ids = {}
    for team in teams:
        res = requests.get(base_url + team)
        soup = BeautifulSoup(res.text, features="html.parser")
        player_ids = soup.find_all('div', class_='s-item__image')
        # print(player_ids)
        hrefs =[ a['href'] for b in player_ids for a in b.find_all('a') ]
        # id_regex = re.compile('(4022)([0-9]{8,8})')
        ids = [re.findall('4022[0-9]{8}', link) for link in hrefs ]
        flat_list = [item for sublist in ids for item in sublist]
        dict_ids[team] = flat_list
    
    json.dump(dict_ids, f, indent=4)
