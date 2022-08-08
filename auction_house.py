#!/usr/bin/env python3

import urllib
import pymongo
from PIL import Image
from datetime import datetime
from blizzard import Blizzard
import time
import io

blizzard = Blizzard()

current_time = datetime.now()

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']

def get_ah_data() -> None:
    ah_data = blizzard.auction_house()
    distinct_current_items = set()
    for item in ah_data['auctions']:
        item_n = item['item']['id']
        distinct_current_items.add(item_n)
        item['date_time'] = current_time
        db['auction_house_data'].insert_one(item)

    # @TODO just compare distinct ah_items with distinct ah_data ids
    # @TODO handle urllib timeouts. 
    distinct_ah_items = [x for x in db['auction_house_items'].distinct('id')]
    for distinct_current_item in distinct_current_items:
        if distinct_current_item not in distinct_ah_items:
            print(f'Getting item info for {distinct_current_item}')
            current_item = blizzard.game_item(item_n)
            image = current_item['media']['key']['href']
            image = blizzard.generic_call(image)
            image = image['assets'][0]['value']
            img_bytes   = io.BytesIO()
            urllib.request.urlretrieve(image, f'/tmp/{item_n}.jpg')
            Image.open(f'/tmp/{item_n}.jpg')
            with Image.open(f'/tmp/{item_n}.jpg') as im:
                im.save(img_bytes, format='JPEG')
                current_item['image']= img_bytes.getvalue()
                db['auction_house_items'].insert_one(current_item)
            time.sleep(1.5) #This is not ideal but going to hit the rate limit anyways.

if __name__ == '__main__':
    get_ah_data()
