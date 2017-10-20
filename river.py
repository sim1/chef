# -*- coding: utf8 -*-
from pprint import pprint as pp

import arrow
import requests


class River(object):

    def __init__(self, api_key):
        super(River, self).__init__()
        self.api_key = api_key

    def _parse(self, line, price_fallback=None, soup=False):
        parts = line.split(' ')
        if soup:
            return ' '.join(parts[1:-1]), 0
        name = ' '.join(parts[2:-2])
        try:
            price = int(parts[-2].split(',')[0])
        except Exception:
            if price_fallback:
                price = price_fallback.split('\xa0')[0]
            else:
                raise

        return name, price

    def get(self):
        response = requests.get(
            'https://developers.zomato.com/api/v2.1/dailymenu?res_id=16507073',
            headers={'user_key': self.api_key},
            timeout=60
        ).json()

        if response.get('status') != 'success':
            return {}

        soups = []
        for soup in response['daily_menus'][0]['daily_menu']['dishes'][:1]:
            name, price = self._parse(soup['dish']['name'], soup=True)
            soups.append({
                'name': name,
                'price': price,
            })

        dishes = []
        pp(response)
        i = 0
        for dish in response['daily_menus'][0]['daily_menu']['dishes'][1:]:
            if dish['dish']['name'].startswith('Týdenní menu'):
                break
            if len(dish['dish']['name']) < 10:
                continue
            try:
                name, price = self._parse(dish['dish']['name'], price_fallback=dish['dish']['price'])
            except Exception:
                continue

            dishes.append({
                'name': name,
                'price': price,
                'vege': i == 3,
            })
            i += 1

        daily_menu = {
            'start_date': arrow.get('1337-05-11T10:30'),
            'end_date': arrow.get('1337-05-11T15:00'),
            'soups': soups,
            'dishes': dishes
        }

        return daily_menu


if __name__ == '__main__':
    response = River(api_key='API-KEY').get()
    pp(response)
