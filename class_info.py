#!/usr/bin/env python3

import pymongo
import requests
from blizzard import Blizzard

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection = db['class_info']

spec_type = {
    62:  'range',
    63:  'range',
    64:  'range',
    65:  'range',
    66:  'melee',
    70:  'melee',
    71:  'melee',
    72:  'melee',
    73:  'melee',
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
    581: 'melee',
}

gear_type = {
    1:  'plate',
    2:  'plate',
    3:  'mail',
    4:  'leather',
    5:  'cloth',
    6:  'plate',
    7:  'mail',
    8:  'cloth',
    9:  'cloth',
    10: 'leather',
    11: 'leather',
    12: 'leather',
}

class_color = {
    'warrior':      '#C79C6E',
    'mage':         '#40C7EB',
    'rogue':        '#FFF569',
    'druid':        '#FF7D0A',
    'warlock':      '#8787ED',
    'shaman':       '#0070DE',
    'monk':         '#00FF96',
    'hunter':       '#A9D271',
    'paladin':      '#F58CBA',
    'demon hunter': '#A330C9',
    'death knight': '#C41F3B',
    'priest':       '#FFFFFF'
}

def main() -> None:
    collection.delete_many({})

    class_indexes = blizzard.playable_class_index()

    for class_index in class_indexes['classes']:
        current_class = blizzard.playable_class(class_index['id'])
        print(current_class['name'])
        class_dict = dict()   
        class_dict[current_class['name']] = {
            'id': current_class['id'],
            'color': class_color[current_class['name'].lower()], 
            'gear_type': gear_type[current_class['id']],
            'specialization': dict()
        } 

        class_media = current_class['_links']['self']['href']
        class_media = blizzard.generic_call_with_token(class_media)
        class_media = class_media['media']['key']['href']
        class_media = blizzard.generic_call_with_token(class_media)
        class_media = class_media['assets'][0]['value']
        r = requests.get(class_media)
        class_dict[current_class['name']]['image']=r.content

        for specialization in current_class['specializations']:
            current_specialization = blizzard.playable_specialization(specialization['id'])
            print(f"\t{current_specialization['name']}")
            
            specialization_dict = {
            'specialization_id ': current_specialization['id'],
            'role': current_specialization['role']['name'],
            'role_type': spec_type[current_specialization['id']],
            }

            spec_media = current_specialization['media']['key']['href']
            spec_media = blizzard.generic_call_without_token(spec_media)
            spec_media = spec_media['assets'][0]['value']
            r = blizzard.generic_call_without_token(spec_media)
            specialization_dict['image'] = r.content
            class_dict[current_class['name']]['specialization'][current_specialization['name']]=specialization_dict
        collection.insert_one(class_dict)
    print('DONE')

if __name__ == '__main__':
    blizzard = Blizzard()
    main()
