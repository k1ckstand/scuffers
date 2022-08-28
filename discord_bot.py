#!/usr/bin/env python3

import os
from discord import member
import pymongo
import discord
import subprocess
from discord.ext import commands 
from discord import message 
import matplotlib.pyplot as plt
from discord.ui import Button, View
import calendar
from datetime import date
from blizzard import Blizzard

TOKEN = os.getenv('DISCORD_TOKEN')

blizzard = Blizzard()

my_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = my_client['scuffers']

intents = discord.Intents.all()
guild = discord.Guild

bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is here. You\'re welcome')

@bot.command(name='wa_sound')
async def wa_sound(ctx, s: str):
    """ 
    Example 1: #wa_sound something
    will create a ogg audio file that says \"something\"
    Example 2: #wa_sound \"run away\"
    Create an ogg audio file that plays \"run away\"
    """ 
    if s.isalpha():
        with open(f'/tmp/{s}', 'w') as f:
            subprocess.run(['espeak', s, '--stdout'], stdout=f)
        # subprocess.run([f'oggenc', '-q', '5', '/tmp/{s}', '-o', f'/tmp/{s}.ogg'])
            subprocess.run(['VLC', '-I', 'dummy', s, '--sout="#transcode{acodec=mpga, ab=192}:standard{access=file,mux=ogg,dst=a.oog}', 'vlc://quit'])
        await ctx.send(file=discord.File(f'/tmp/a.ogg'))
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
        user_collection = {
        'name': user.name,
        'id': user.id,
        'role': user.roles
        }
    db['discord_users'].insert_one(user_collection)

@bot.command(name='button_test')
async def button_test(ctx):

    RAID_NIGHTS = ['Wednesday', 'Thursday']
    found_dates = list()
    d = date.today()
    j = d.toordinal()
    while len(found_dates) != len(RAID_NIGHTS):
        d = date.fromordinal(j)
        x = calendar.day_name[d.weekday()]
        if x in RAID_NIGHTS:
            found_dates.append(d)
        j += 1
    for d in found_dates:

        button_yes  = Button(label='Yes', custom_id=d.strftime('%A'), style=discord.ButtonStyle.green) 
        button_late = Button(label='late', style=discord.ButtonStyle.secondary) 
        button_no   = Button(label='no', style=discord.ButtonStyle.red) 
        view = View()
        view.add_item(button_yes)
        view.add_item(button_late)
        view.add_item(button_no)
        await ctx.send(d.strftime("%A, %B %d"))
        await ctx.send(view=view)

import json
@bot.command(name='player_lookup')
async def player_lookup(ctx, message):
    '''player_name server_name'''
    await ctx.message('something goes here', reason=None)
    await create_thread("something")
    # name = name.lower().strip()
    # server = name.lower().strip()
    # print(f'{name} : {server}')
    # try:
    #     profile = blizzard.profile_character_profile(name, server)
    #     await ctx.send(json.dumps(profile, indent=2))
    # except Exception as e:
    #     await ctx.send()


bot.run(TOKEN)
