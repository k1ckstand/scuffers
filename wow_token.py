#!/usr/bin/env python3

from blizzard import Blizzard
from pymongo import MongoClient

def main() -> None:
    try:
        wow_token = blizzard.wow_token()
        del wow_token['_links']
        if not collection.find_one({'last_updated_timestamp': wow_token['last_updated_timestamp']}):
            collection.insert_one(wow_token)
            print('DONE!')
    except ValueError as v:
        print('BAD REQUEST')
        print(v)
    except Exception as e:
        print('Something went wrong ¯\_(⊙︿⊙)_/¯')
        print(e)

if __name__ == '__main__':
    blizzard = Blizzard()

    my_client = MongoClient('mongodb://localhost:27017/')
    db = my_client['scuffers']
    collection = db['wow_token']

    main()
