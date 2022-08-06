#!/usr/bin/env python3

import urllib
import pymongo
from blizzard import Blizzard

blizzard = Blizzard()

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection = db['class_info']

collection.delete_many({})

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

character_specializations = blizzard.game_playable_specialization_index()
class_indexes = blizzard.game_playable_class_index()

for class_index in class_indexes['classes']:
    current_class = blizzard.game_playable_class(class_index['id'])
    class_dict = {
        'class_name': current_class['name'],
        'class_id': current_class['id'],
        'class_color': class_color[current_class['name'].lower()],
        'class_media': IMG_PATH + current_class['name'] + '.jpg',
        'gear_type': gear_type[current_class['id']]

    }
    class_media = blizzard.game_playable_class_media(current_class['id'])
    class_media = class_media['assets'][0]['value']

    urllib.request.urlretrieve(class_media, IMG_PATH + current_class['name'] + '.jpg')

    specializations = []
    for specialization in current_class['specializations']:
        current_specialization = blizzard.game_playable_specialization(specialization['id'])
        if current_specialization is None:
            print('ERROR: {}'.format(specialization['name']))
        else:
            spec_dict = {
                'specialization_name': current_specialization['name'],
                'specialization_id ': current_specialization['id'],
                'role': current_specialization['role']['name'],
                'role_type': spec_type[current_specialization['id']],
                'spec_media': IMG_PATH + current_specialization['name'] + '.jpg'
            }

            spec_media = current_specialization['media']['key']['href']
            spec_media = blizzard.generic_call(spec_media)
            spec_media = spec_media['assets'][0]['value']
            urllib.request.urlretrieve(spec_media, IMG_PATH + spec_dict['specialization_name'] + '.jpg')

            specializations.append(spec_dict)

    class_dict['specialization'] = specializations
    collection.insert_one(class_dict)

