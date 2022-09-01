#!/usr/bin/env python3

from pymongo import MongoClient
from datetime import datetime
from blizzard import Blizzard

client = MongoClient('mongodb://localhost:27017/')
db = client['scuffers']

def get_ah_data(realm_id: int=57) -> set:
    current_time = datetime.now()
    ah_data = blizzard.auction_house(realm_id)
    for item in ah_data['auctions']:
        item['date_time'] = current_time
        db['auction_house'].insert_one(item)

    new_items = db['auction_house'].find({}).distinct('item.id')
    total = len(new_items) - len(db['items'].find({}).distinct('id'))
    i = 0
    for item_id in new_items:
        if not db['items'].find_one({'id': item_id}):
            print(f'{i}/{total}: Item: {item_id}')
            i += 1
            item = blizzard.item(item_id)
            try:
                item['date_time'] = current_time
                image_url = item['media']['key']['href']
                image_url = blizzard.generic_call_with_token(image_url)
                image_url = image_url['assets'][0]['value']
                image = blizzard.generic_call_without_token(image_url)
                if image is not None:
                    item['image'] = image
                    db['items'].insert_one(item)
            except Exception as e:
                print(f'There was a problem with item: {item_id}')
                print(e)

if __name__ == '__main__':
    blizzard = Blizzard()
    get_ah_data()
