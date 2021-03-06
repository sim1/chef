import requests
import unicodedata
import os

class Zomato:
    def get(self):
        r = requests.get(
            f'https://developers.zomato.com/api/v2.1/dailymenu?res_id={self.zomato_id}',
            headers={'user_key': os.getenv('CHEF_ZOMATO_API_KEY')},
            timeout=60,
        )
        r.raise_for_status()

        meals = []

        for i, meal in enumerate(r.json()['daily_menus'][0]['daily_menu']['dishes']):
            meal = self.filter(meal['dish']['name'])
            if meal:
                meals.append((meal, {'veg': self.is_vegetarian(meal, i)}))

        return meals

    def filter(self, meal):
        return meal

    def is_vegetarian(self, meal, number):
        return False
