#!/usr/bin/env python3

import os
import json
import requests
from time import sleep
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection =  db['request_logs']

class Logger:
    __q  = list()
    __last_request = list()
    def logger(func):
        SAFETY = 10
        REQUEST_PER_HR  = 3_600 - SAFETY
        REQUEST_PER_SEC = 100   - SAFETY

        def inner(self, *args):
            try: 
                r = func(self, *args)
            except Exception as e:
                print(e)
                return None
            if r.status_code != 200:
                return_me = None
            else:
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
                collection.insert_one(log)
                return return_me
        # Logger.__q.append(func)
        # while len(Logger.__q) > 0:
        #     now = datetime.now()
        #     try:
        #         sleep(now - Logger.__last_request[-1])
        #     except:
        #         pass
            
        return inner

class Blizzard(Logger):
    def __init__(self):
        CLIENT = os.environ['B_CLIENT']
        SECRET = os.environ['B_SECRET']
        r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'}, auth=(CLIENT, SECRET))
        self.access_token = json.loads(r.text)['access_token']

    @Logger.logger
    def mythic_keystone_dungeons_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def mythic_keystone_leader_board(self, dungeon_id: int, period: int, cr_id: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/mythic-leaderboard/{str(dungeon_id)}/period/{str(period)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def journal_instances_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/journal-instance/index?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)
    
    @Logger.logger
    def journal_instance_media(self, ji_id: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/journal-instance/{str(ji_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def mythic_keystone_dungeons(self, index: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/{str(index)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def mythic_keystone_period_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/period/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def guild(self, guild_name: str, server: str):
        return requests.get(f'https://us.api.blizzard.com/data/wow/guild/{server}/{guild_name}/roster?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def playable_class_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/index?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def playable_class(self, class_id: int):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def playable_class_media(self, class_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def playable_specialization(self, spec_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/{str(spec_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def playable_specialization_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def mythic_keystone_seasons_index(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def item(self, item_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def item_media(self, item_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/media/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def character_equipment(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/equipment?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def character_profession(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/professions?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def character_profile(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def character_pvp(self, name, server, bracket):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/pvp-bracket/{bracket}?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def character_media(self, name, server):
        return requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/character-media?namespace=profile-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def auction_house(self, cr_id):
        return requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def wow_token(self):
        return requests.get(f'https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def generic_call_with_token(self, url: str):
        return requests.get(f'{url}&access_token={self.access_token}', timeout=2)

    @Logger.logger
    def generic_call_without_token(self, url: str):
        return requests.get(url, timeout=2)

if __name__ == '__main__':
    pass
