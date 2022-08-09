#!/usr/bin/env python3

import pymongo
from blizzard import Blizzard

blizzard = Blizzard()

dungeon_indexes = blizzard.game_mythic_keystone_dungeons_index()
season_indexes = blizzard.game_mythic_keystone_seasons_index()
current_season = season_indexes['current_season']['id']
current_season_periods = blizzard.generic_call(season_indexes['current_season']['key']['href'])['periods']

dungeon_times = {}
for dungeon_index in dungeon_indexes['dungeons']:
    dungeon_time = blizzard.game_mythic_keystone_dungeons(dungeon_index['id'])
    dungeon_times[dungeon_time['name']] = dungeon_time['keystone_upgrades']

start_period = current_season_periods[0]['id']
current_period = current_season_periods[-1]['id']

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['scuffers']
collection = db['m_plus_season_' + str(current_season)]

if collection.count_documents({}) == 0:
    start_period = current_season_periods[0]['id']
else:
    start_period = collection.find_one(sort=[('period', pymongo.DESCENDING)])
    start_period = start_period['period']

for period in range(start_period, current_period + 1):
    for dungeon_index in dungeon_indexes['dungeons']:
        insert_me = blizzard.game_mythic_keystone_leader_board(dungeon_index['id'], period)
        if collection.find_one({'period': period, 'map_challenge_mode_id': dungeon_index['id']}):
            print('replacing {} : {}'.format(period, dungeon_index['name']))
            collection.replace_one({
                'period': period,
                'map_challenge_mode_id': dungeon_index
                }, insert_me)
        else:
            try:
                if insert_me['leading_groups']:
                    print('inserting {} : {}'.format(period, dungeon_index['name']))
                    collection.insert_one(insert_me)
            except Exception as e:
                print('nothing found for {} : {}'.format(period, dungeon_index['name']))
