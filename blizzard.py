#!/usr/bin/env python3

import json
import os
import requests

class Blizzard:
    _l = list()
    def __init__(self):
        CLIENT = os.environ['B_CLIENT']
        SECRET = os.environ['B_SECRET']
        r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'}, auth=(CLIENT, SECRET))
        self.access_token = json.loads(r.text)['access_token']
        
    def game_professions_index(self):
        r =  (f'https://us.api.blizzard.com/data/wow/profession/index?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json
    
    def game_profession(self, n):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/profession/{str(n)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_mythic_keystone_dungeons_index(self):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_mythic_keystone_dungeons(self, index):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/{str(index)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_mythic_keystone_period_index(self):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/period/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_mythic_keystone_leader_board(self, dungeon_id, period, cr_id=57):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/mythic-leaderboard/{str(dungeon_id)}/period/{str(period)}?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_guild(self, guild_name: str, server: str) -> json:
        r = requests.get(f'https://us.api.blizzard.com/data/wow/guild/{server}/{guild_name}/roster?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_playable_class_index(self):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/index?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_playable_class(self, class_id: int) -> json:
        r = requests.get(f'https://us.api.blizzard.com/data/wow/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_playable_class_media(self, class_id):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/media/playable-class/{str(class_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_playable_specialization(self, spec_id):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/{str(spec_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_playable_specialization_index(self):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_mythic_keystone_seasons_index(self):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_item(self, item_id):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def game_item_media(self, item_id):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/media/item/{str(item_id)}?namespace=static-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def profile_character_equipment(self, name, server):
        r = requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/equipment?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json()

    def profile_character_profession(self, name, server):
        r = requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/professions?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json() 

    def profile_character_profile(self, name, server):
        r = requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json() 

    def profile_character_pvp(self, name, server, bracket):
        r = requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/pvp-bracket/{bracket}?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json() 

    def profile_character_media(self, name, server):
        r = requests.get(f'https://us.api.blizzard.com/profile/wow/character/{server}/{name}/character-media?namespace=profile-us&locale=en_US&access_token={self.access_token}')
        return r.json() 

    def profile_specialization(self, url):
        r = requests.get(url)
        return r.json() 

    def generic_call(self, url):
        r = requests.get(f'{url}&access_token={self.access_token}')
        return r.json() 

    def auction_house(self, cr_id=57):
        r = requests.get(f'https://us.api.blizzard.com/data/wow/connected-realm/{str(cr_id)}/auctions?namespace=dynamic-us&locale=en_US&access_token={self.access_token}')
        return r.json()

if __name__ == '__main__':
    obj = Blizzard()
    a = obj.game_mythic_keystone_seasons_index()
    print(a)
