"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from datetime import datetime
from colorama import Fore
from colorama import Style
import psutil
from platform import python_version
import requests
from config import PREFIX, TOKEN

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

class Bot(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command(aliases=["bot", 'rocki', 'about', 'faq'], enabled=True, description="Info about the bot", usage="")
    # First parametr is how many commands to cooldown, second is the time in seconds, third is the bucket type (user, guild, defoult - command or channel)
    @commands.cooldown(1, 8.0, commands.BucketType.user)
    async def info(self, ctx):

        members = 0

        for guild in self.client.guilds:
            members += guild.member_count

        embed = discord.Embed(title=f"{self.client.user.name}", description=f"Simple private discord bot, made by **[USER#0000](LINK)** \nCurrently on ``{len(self.client.guilds)}`` guilds with ``{members}`` members. \nIf your guild is on whitelist **[click here](LINK)**. \n**prefixes:** ``{', '.join(PREFIX)}`` \n \n**ping:** ``{round(self.client.latency * 1000)}ms`` \n**commands:** ``{len(list(self.client.walk_commands()))}`` \n**python:** ``{python_version()}`` \n**discord.py:** ``{discord.__version__}``", color=0x303136)
        embed.set_thumbnail(url=f'{self.client.user.avatar_url}')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['inv'], enabled=True, description="Invite like.", usage="")
    @commands.cooldown(1, 8.0, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(description=f"If you want to add me to your guild **[click here](HERE YOUR LINK)** \n \n To get wl contact with owner ``USER#0000``", color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=60)

    @commands.command(aliases=["ws", 'latency'], enabled=True, description="Get bot latency.")
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(description=f'``ws:`` {round(self.client.latency * 1000)}ms', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=15)

def setup(client):
    client.add_cog(Bot(client))
