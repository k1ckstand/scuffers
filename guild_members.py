#!/usr/bin/env python3

import re
import time
import urllib
import pymongo
import threading
from blizzard import Blizzard

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection = db['guild_members']

def get_profile(name: str, server: str, discord: str, my_main: bool, raid_lead: bool, n=3) -> None:
    IMG_PATH = '/mnt/disk0/media/player/'
    character_profile = blizzard.profile_character_profile(name, server)
    assets = blizzard.profile_character_media(name, server)

    if character_profile is not None and assets is not None:
        insert_me = {
        'name': name,
        'server': server,
        'discord': discord,
        'is_main': my_main,
        'is_raid_lead': raid_lead,
        'gender': character_profile['gender']['name'],
        'race': character_profile['race']['name'],
        'class_name': character_profile['character_class']['name'],
        'class_id': character_profile['character_class']['id'],
        'level': character_profile['level'],
        'item_level': character_profile['equipped_item_level']
        }
        if 'covenant_progress' in character_profile.keys():
            insert_me['covenant'] = character_profile['covenant_progress']['chosen_covenant']['name']
            insert_me['renown'] = character_profile['covenant_progress']['renown_level']

        for asset in assets['assets']:
            full_file_path = IMG_PATH + insert_me['name'] + '_' + asset['key'] + '.jpg'
            urllib.request.urlretrieve(asset['value'], full_file_path)
            insert_me[asset['key']] = full_file_path
        print('Inserting: {}'.format(name))
        collection.insert_one(insert_me)
    else:
        print('ERROR: {}'.format(name))
        if n > 0:
            time.sleep(2)
            get_profile(name, server, discord, my_main, raid_lead, n-1)

def main():
    collection.delete_many({})
    with open('guild_members.txt', 'r') as f:
        threads = []
        for line in f:
            if re.match('^[a-z],*', line.lower()):
                line = line.split(' ')
                name = line[0].lower().strip()
                server = line[1].lower().strip()
                discord = line[2].lower().strip()
                if line[3].lower().strip() == 'true': my_main = True
                else: my_main = False
                if line[4].lower().strip() == 'true': raid_lead = True
                else: raid_lead = False

                t = threading.Thread(target=get_profile, args=[name, server, discord, my_main, raid_lead])
                t.start()
                threads.append(t)
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    blizzard = Blizzard()
    main()