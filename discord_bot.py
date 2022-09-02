#!/usr/bin/env python3

import os
import pymongo
from discord.ext import commands
from discord.ui import Button, View
import calendar
import json
import discord
from datetime import datetime
from blizzard import Blizzard
import plotly.graph_objects as go
TOKEN = os.getenv('DISCORD_TOKEN')

blizzard = Blizzard()

my_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = my_client['scuffers']

intents = discord.Intents.all()
guild = discord.Guild

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is here. You\'re welcome')

@bot.command(name='wow_token')
async def wow_token(ctx, days=30):
    '''
    | Get the price chart of a WOW Token.
    '''
    BLIZZARD_SECONDS = 1_000
    collection = db['wow_token']
    now = datetime.now()
    blizzard_now = int(now.timestamp() * BLIZZARD_SECONDS)
    last = blizzard_now - (60 * 60 * 24 * days * BLIZZARD_SECONDS)
    results = collection.find( {
        'last_updated_timestamp': {
            '$gt': last,
            '$lt': blizzard_now
            }
        }
    )
    x = list()
    y = list()
    for result in results:
        time = int(result['last_updated_timestamp'])
        x.append(datetime.fromtimestamp(time / BLIZZARD_SECONDS))
        y.append(result['price'] / 10_000) # Gold Conversion
    fig = go.Figure(
        data=go.Scatter(x=x, y=y),
        )
    fig.update_layout(
    title = {
        'text': f'WOW Token Price, Last Update: {x[-1]} GMT',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        }
    )
    fig.write_image('/tmp/wow_token.png')
    await ctx.send(file=discord.File('/tmp/wow_token.png'))


@bot.command(name='add_character')
async def wa_sound(ctx, name: str, server: str='illidan'):
    '''
    | Add a character to opps_bot.
    | #add_character <name> <server>
    '''
    async def button_callback(interaction):
        if not db['guild_members'].find_one({'discord_id': str(ctx.message.author.id)}):
            insert_me = {
                'discord_id': ctx.message.author.id,
                'discord_name': ctx.message.author.name,
                'characters': [
                    {
                        'name': name,
                        'server': server
                    },
                ],
            }
            db['guild_members'].insert_one(insert_me)
            my_message = f'{name} has been added.'
        else:
            my_message = 'Okay, Try again.'
        await interaction.response.edit_message(content=my_message)
    
    media = blizzard.character_media(name, server)
    media = media['assets'][1]['value']
    button_yes = Button(label='Yes', style=discord.ButtonStyle.green)
    button_no   = Button(label='No', style=discord.ButtonStyle.red)
    view = View()
    view.add_item(button_yes)
    view.add_item(button_no)
    await ctx.send(media)
    await ctx.send('Is this you?', view=view)

    button_yes.callback = button_callback
    button_no.callback = button_callback

bot.run(TOKEN)
