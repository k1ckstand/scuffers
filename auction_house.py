#!/usr/bin/env python3

from pymongo import MongoClient
from PIL import Image
from datetime import datetime
from blizzard import Blizzard
from time import sleep
import base64
import requests

blizzard = Blizzard()

client = MongoClient('mongodb://localhost:27017/')
db = client['scuffers']

def log_me() -> None:
    pass # @TODO

def get_ah_data(realm_id: int=57) -> set:
    current_time = datetime.now()
    ah_data = blizzard.auction_house(realm_id)
    for item in ah_data['auctions']:
        item['date_time'] = current_time
        db['auction_house_data'].insert_one(item)

    for item_id in db['auction_house_data'].find({}).distinct('item.id'):
        print(f'Getting item for {item_id}')
        if not db['items'].find_one({'id': item_id}):
            item = blizzard.game_item(item_id)
            item['date_time'] = current_time
            db['items'].insert_one(item)
            sleep(.5)

    for item_id in db['items'].find({}).distinct('id'):
        item = db['items'].find_one({ 'id': item_id })
        if item:
            image_url = item['media']['key']['href']
            image_url = blizzard.generic_call(image_url)
            image_url = image_url['assets'][0]['value']
            r = requests.get(image_url)
            image_b64 = r.content
            if r.status_code == 200:
                print(f'Getting icon for {item_id}')
                insert_image = {
                    'date_time': current_time,
                    'id': item_id,
                    'image': image_b64
                }
            db['media'].insert_one(insert_image)
            sleep(.5)

if __name__ == '__main__':
    get_ah_data()
