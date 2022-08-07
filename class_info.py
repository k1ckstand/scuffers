#!/usr/bin/env python3

import io
import pymongo
import urllib
from PIL import Image
from blizzard import Blizzard

blizzard = Blizzard()

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection = db['class_info']

spec_type = {
    62: 'range',
    63: 'range',
    64: 'range',
    65: 'range',
    66: 'melee',
    70: 'melee',
    71: 'melee',
    72: 'melee',
    73: 'melee',
    102: 'range',
    103: 'melee',
    104: 'melee',
    105: 'range',
    250: 'melee',
    251: 'melee',
    252: 'melee',
    253: 'range',
    254: 'range',
    255: 'melee',
    256: 'range',
    257: 'range',
    258: 'range',
    259: 'melee',
    260: 'melee',
    261: 'melee',
    262: 'range',
    263: 'range',
    264: 'range',
    265: 'range',
    266: 'range',
    267: 'range',
    268: 'melee',
    269: 'melee',
    270: 'range',
    577: 'melee',
    581: 'melee'
}

gear_type = {
    1: "plate",
    2: "plate",
    3: "mail",
    4: "leather",
    5: "cloth",
    6: "plate",
    7: "mail",
    8: "cloth",
    9: "cloth",
    10: "leather",
    11: "leather",
    12: "leather"
}

class_color = {
    'warrior': '#C79C6E',
    'mage': '#40C7EB',
    'rogue': '#FFF569',
    'druid': '#FF7D0A',
    'warlock': '#8787ED',
    'shaman': '#0070DE',
    'monk': '#00FF96',
    'hunter': '#A9D271',
    'paladin': '#F58CBA',
    'demon hunter': '#A330C9',
    'death knight': '#C41F3B',
    'priest': '#FFFFFF'
}

def init_setup():
    collection.delete_many({})

    class_indexes = blizzard.game_playable_class_index()

    for class_index in class_indexes['classes']:
        current_class = blizzard.game_playable_class(class_index['id'])
        print(f"Getting info for {current_class['name']}")
        class_dict = dict()   
        class_dict[current_class['name']] = {
            'id': current_class['id'],
            'color': class_color[current_class['name'].lower()], 
            'gear_type': gear_type[current_class['id']],
            'specialization': dict()
        } 

        img_bytes   = io.BytesIO()
        class_media = current_class['_links']['self']['href']
        class_media = blizzard.generic_call(class_media)
        class_media = class_media['media']['key']['href']
        class_media = blizzard.generic_call(class_media)
        class_media = class_media['assets'][0]['value']
        urllib.request.urlretrieve(class_media, f"/tmp/{current_class['name']}.jpg")
        with Image.open(f'/tmp/{current_class["name"]}.jpg') as class_img:
            class_img.save(img_bytes, format='JPEG')
            class_dict[current_class['name']]['image']=img_bytes.getvalue()

        for specialization in current_class['specializations']:
            current_specialization = blizzard.game_playable_specialization(specialization['id'])
            print(f"\t{current_specialization['name']}")
            
            specialization_dict = {
            'specialization_id ': current_specialization['id'],
            'role': current_specialization['role']['name'],
            'role_type': spec_type[current_specialization['id']],
            }

            img_bytes  = io.BytesIO()
            spec_media = current_specialization['media']['key']['href']
            spec_media = blizzard.generic_call(spec_media)
            spec_media = spec_media['assets'][0]['value']
            urllib.request.urlretrieve(spec_media, f"/tmp/{current_specialization['name']}")
            with Image.open(f"/tmp/{current_specialization['name']}") as spec_img:
                spec_img.save(img_bytes, format='JPEG')
                specialization_dict['image'] = img_bytes.getvalue()
            class_dict[current_class['name']]['specialization'][current_specialization['name']]=specialization_dict
        collection.insert_one(class_dict)
print('DONE')

if __name__ == '__main__':
    init_setup()
