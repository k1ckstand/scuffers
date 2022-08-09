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
db = my_client['scuffers']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is here. You\'re welcome')

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
