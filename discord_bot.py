#!/usr/bin/env python3

import os
from discord import member
import pymongo
import discord
import subprocess
from discord.ext import commands
import matplotlib.pyplot as plt

TOKEN = os.getenv('DISCORD_TOKEN')

my_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = my_client['hyjal']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print("{} is here. You're welcome".format(bot.user.name))

@bot.command(name='wa_sound')
async def wa_sound(ctx, s: str):
    """ 
    Example: #wa_sound something
    will create a ogg audio file that says \"something\"
    """ 
    if s.isalpha():
        with open('/tmp/{}'.format(s), 'w') as f:
            subprocess.run(['espeak', s, '--stdout'], stdout=f)
        subprocess.run(['oggenc', '-q', '5', '/tmp/{}'.format(s), '-o', '/tmp/{}.ogg'.format(s)])
        await ctx.send(file=discord.File('/tmp/{}.ogg'.format(s)))
        os.remove('/tmp/{}'.format(s))
        os.remove('/tmp/{}.ogg'.format(s))
    else:
        await ctx.send('letters only please')

@bot.command(name='covenant')
async def covenant(ctx):
    collection = db['guild_members']
    covenant_color = {
        'Necrolord': 'green',
        'Kyrian': 'lightblue',
        'Venthyr': 'red',
        'Night Fae': 'blue',
    }

    all_players = []
    for player in collection.find({'is_main': True}):
        if 'covenant' in player:
            all_players.append(player['covenant'])

    labels = sorted(list(set(all_players)))
    size = []
    colors = []
    for label in labels:
        size.append(collection.count_documents({'covenant': label, 'is_main': True}) / len(all_players))
        colors.append(covenant_color[label])

    explode = []
    for _ in labels:
        explode.append(0.1)

    _, ax1 = plt.subplots()
    ax1.pie(size, labels=labels, colors=colors, shadow=True, autopct='%1.1f%%', explode=explode, normalize=True)
    ax1.axis('equal')
    plt.title('Current covenants for player mains')
    plt.savefig('/tmp/my_chart.jpg')
    await ctx.send(file=discord.File('/tmp/my_chart.jpg'))
    os.remove('/tmp/my_chart.jpg')

@bot.command(name='m_plus')
async def m_plus(ctx, name: str=None):
    print(ctx.message.author.id)
    print(ctx.message.author.mention)
    print(ctx.message.author.name)

    collection = db['m_plus_season_5']

    dungeons = collection.find( { }).distinct('name')
    compleated_dungeons = {}
    for dungeon in dungeons:
        compleated_dungeons[dungeon] = False
    for player in collection.find( { 'discord': name }, {'_id': 0, 'name': 1} ):
        result = collection.find_one( {
            'leading_groups.members.'
        }
    )

@bot.command(name="get_discord_users")
async def get_discord_users(ctx):
    for user in ctx.guild.members:
        print(user.name)
        print(user.id)
        print(user.roles)



bot.run(TOKEN)



    # name = "opprobrious"
    # compleated_dungeons = {}
    # dungeons = collection.find( { }).distinct('name')
    # for dungeon in dungeons:
    #     compleated_dungeons[dungeon] = False
    # for player in collection.find( { 'discord': name }, {'_id': 0, 'name': 1} ):
    #     print(player['name'])
    #     somethign = db['m_plus_season_5'].count_documents( { 
    #         'leading_groups.members.profile.name': re.compile(player['name'], re.IGNORECASE),
    #         'leading_groups.keystone_level': { '$gte': 15 },
    #         'leading_groups': { '$lte': { 'duration': 'dungeon_time.0.qualifying_duration' } }
    #         } )
    #     print(somethign)

    # results = db['m_plus_achievement'].find_one( {'name': name} )
    # send_me = '' # "target_player" + ' ( ' + "player"['b_tag'] + ' )\n'
    # send_me += '-' * 27
    # send_me += '\n'
    # for dungeon in results['dungeons']:
    #     send_me += dungeon
    #     send_me += ' ' * (22 - len(dungeon))
    #     send_me += ' | '
    #     if results['dungeons'][dungeon]:
    #         send_me += '\U00002705'
    #     else:
    #         send_me += '\U0000274C'
    #     send_me += '\n'
    #     send_me = '```' + send_me + '```'
    # await ctx.send(send_me)




# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     elif message.content.startswith('#m_plus'):
#         author =  message.author.name
#         current_message = message.content.split(' ')[1:]
#         if len(current_message) > 0:
#             for player in current_message:
#                 m_plus_achivment(player)
#         else:
#             print("SDFSDFSF")
#             m_plus_achivment(message.author.name)
        # if collection.find_one( { 'discord': author} ):
        #     my_message = m_plus_achivment(author)
        # if collection.find_one( { 'name': author }, { '_id': 0, 'discord': 1 } ):
        #     print(discord)
        # print(my_message)
            # print(send_me)
            # await message.channel.send(send_me)


bot.run(TOKEN)
