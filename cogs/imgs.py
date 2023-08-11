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
from functions.logs import log
from asyncdagpi import Client, ImageFeatures


now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

dagpi = Client("dagpi_token")

class Imgs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pixel(self, ctx):
        try:
            img = await dagpi.image_process(ImageFeatures.pixel(), str(ctx.author.avatar_url))
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            await ctx.send(file=file)
        except Exception as e:
            log('error', f'Error in {ctx.command} command: {e}')

def setup(client):
    client.add_cog(Imgs(client))
