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
from functions.embeds import error_embed, arguments_error_embed
from functions.logs import log

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command(aliases=["clear", 'c'], enabled=True, description="Clear messages from a channel.", usage="<number>")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        am = amount or 5

        await ctx.channel.purge(limit=am)
        await ctx.send(f'👍, ``{am}`` messages deleted.')



def setup(client):
    client.add_cog(Mod(client))
