from login.credentials import get_settings
from api.wow_api import json_openener

key, _ = get_settings()


def get_item(id):
    url = 'https://eu.api.battle.net/wow/item/{}?locale=en_US&apikey={}'.format(id, key)
    dict_item = json_openener(url)

    return dict_item


def get_craft(id):
    url = 'https://eu.api.battle.net/wow/recipe/{}?locale=en_US&apikey={}'.format(id, key)
    dict_item = json_openener(url)
    return dict_item
    # 'https://eu.api.battle.net/wow/recipe/252352?locale=en_GB&apikey=g4s923e95jgmyq5w24cra8gpc746b7rt'
