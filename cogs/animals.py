"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore
from colorama import Style
import requests
from data.utils.messages import error_message

from functions.logs import log

class Animals(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command(enabled=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def dog(self, ctx):

        try:
            url = f'https://random.dog/woof.json'
            r = requests.get(url).json()

            embed = discord.Embed(title=f'Random doggo image', color=0x303136)
            embed.set_image(url=r['url'])
            await ctx.reply(embed=embed, mention_author=False)

        except Exception as e:
            log('error', f'Error in {ctx.command} command: {e}')
            embed = discord.Embed(description=error_message, color=0x303136)
            await ctx.send(embed=embed)
    

    @commands.command(enebled=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def duck(self, ctx):
        try:
            url = f'https://random-d.uk/api/random'
            r = requests.get(url).json()

            embed = discord.Embed(title=f'Random ducky image', color=0x303136)
            embed.set_image(url=r['url'])
            embed.set_footer(text=r['message'])
            await ctx.reply(embed=embed, mention_author=False)

        except Exception as e:
            log('error', f'Error in {ctx.command} command: {e}')
            embed = discord.Embed(description=error_message, color=0x303136)
            await ctx.send(embed=embed)

    @commands.command(enebled=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def cat(self, ctx):
        try:
            url = f'https://api.thecatapi.com/v1/images/search'
            r = requests.get(url).json()

            embed = discord.Embed(title=f'Random cat image', color=0x303136)
            embed.set_image(url=r[0]['url'])
            await ctx.reply(embed=embed, mention_author=False)

        except Exception as e:
            log('error', f'Error in {ctx.command} command: {e}')
            embed = discord.Embed(description=error_message, color=0x303136)
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Animals(client))
