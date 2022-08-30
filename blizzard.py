#!/usr/bin/env python3

from datetime import datetime
from pymongo import MongoClient
import json
import os
from inspect import Parameter
from inspect import signature

import requests
from time import sleep
client = MongoClient('mongodb://localhost:27017/')
db = client['scuffers']

__q  = list()

def logger(func):
    SAFETY = 10
    REQUEST_PER_HR  = 3_600 - SAFETY
    REQUEST_PER_SEC = 100   - SAFETY

    def inner(self, *args):
        r = func(self, *args)
        log = {
            'date_time': datetime.now(),
            'func_name': func.__name__,
            'args': args,
            'status': r.status_code
        }
        try:
            log['type']='json'
            return_me =  r.json()
        except ValueError as e:
            log['type']='content'
            return_me = r.content
        db['blizzard_logs'].insert_one(log)
        return return_me
    return inner

class Blizzard:
    def __init__(self):
        CLIENT = os.environ['B_CLIENT']
        SECRET = os.environ['B_SECRET']
        r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'}, auth=(CLIENT, SECRET))
        self.access_token = json.loads(r.text)['access_token']

    @logger
    def mythic_keystone_dungeons_index(self) -> json:
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def mythic_keystone_leader_board(self, dungeon_id: int, period: int, cr_id: int) -> json:
        return requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/mythic-leaderboard/{str(dungeon_id)}/period/{str(period)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def generic_call_with_token(self, url: str):
        return requests.get(f'{url}&access_token={self.access_token}')
    
    @logger
    def journal_instances_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/journal-instance/index?namespace=static-us&locale=en_US&access_token={self.access_token}')
    
    @logger
    def journal_instance_media(self, ji_id: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/journal-instance/{str(ji_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def generic_call_without_token(self, url: str):
        return requests.get(url)
    
    @logger
    def wow_token(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def mythic_keystone_dungeons(self, index: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/{str(index)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def mythic_keystone_period_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/period/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def guild(self, guild_name: str, server: str) -> json:
        return requests.get(f'https://us.api.blizzard.com/data/wow/guild/{server}/{guild_name}/roster?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def playable_class_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/index?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def playable_class(self, class_id: int) -> json:
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def playable_class_media(self, class_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def playable_specialization(self, spec_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/{str(spec_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def playable_specialization_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def mythic_keystone_seasons_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

    @logger
    def item(self, item_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def item_media(self, item_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')

    @logger
    def character_equipment(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/equipment?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def character_profession(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/professions?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def character_profile(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def character_pvp(self, name, server, bracket):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/pvp-bracket/{bracket}?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def character_media(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/character-media?namespace=profile-us&locale=en_US&access_token={self.access_token}')

    @logger
    def auction_house(self, cr_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')

if __name__ == '__main__':
    pass
