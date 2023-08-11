"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

# Main imports
import discord
from discord.ext import commands

# Console log imports
from datetime import datetime
from colorama import Fore
from colorama import Style

# Command imports
import requests
import random
from functions.embeds import error_embed, arguments_error_embed

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")
embed_time_log = now.strftime("[%d/%m/%Y]")

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command(enabled=True, usage='', description='Send a random hug gif.')
    async def hug(self, ctx):
        try:
            url = f'https://nekos.life/api/hug'
            r = requests.get(url).json()

            embed = discord.Embed(title="👩‍❤️‍👨", color=0x303136)
            embed.set_image(url=r['url'])
            await ctx.reply(embed=embed)
        except Exception as e:
            print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
    
    @commands.command(enabled=True, descrtipion='Send a random kiss gif.')
    async def kiss(self, ctx):
        try:
            url = f'https://nekos.life/api/kiss'
            r = requests.get(url).json()

            embed = discord.Embed(title="👩‍❤️‍👨", color=0x303136)
            embed.set_image(url=r['url'])
            await ctx.reply(embed=embed)
        except Exception as e:
            print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
    
    @commands.command(enabled=True, usage='<member>', description='Mad?')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    async def cry(self, ctx, member: discord.Member = None):

        crygifs = {
            "gifs": 
                [
                    "https://c.tenor.com/DXQmhJSu31AAAAAd/pudizu-vtuber.gif",
                    "https://media.discordapp.net/attachments/402911262322720778/933390945624404038/who-asked-me-trying-to-find-who-asked.gif",
                    "https://c.tenor.com/Nbg6A9cVK4gAAAAC/cry-about-it-rickroll.gif",
                    "https://c.tenor.com/5EgBYns_4L4AAAAd/lizard-dancing-lizard.gif",
                    "https://c.tenor.com/2-RzduV0wvYAAAAd/okay-i-will-cry-about-it-moona.gif",
                    "https://cdn.discordapp.com/attachments/856321005235470366/857694421179695144/1622771600740.gif",
                    "https://c.tenor.com/YWxBliBkVHAAAAAC/ok-and.gif",
                    "https://media.discordapp.net/attachments/914190956239134821/927554271040401418/ok-and.gif",
                    "https://media.discordapp.net/attachments/914190956239134821/927554476708085780/ok-and.gif",
                    "https://c.tenor.com/MflDzZwI8qoAAAAd/shaving-head-ok-and.gif",
                    "https://c.tenor.com/vryf32uQU68AAAAM/cry-about-it.gif",
                    "https://c.tenor.com/Q-F-zmdvZ9cAAAAd/cry.gif",
                    "https://i.kym-cdn.com/photos/images/newsfeed/002/130/363/053.gif",
                    "https://c.tenor.com/EE1SLJuxBL4AAAAM/cry-about-it-cry.gif",
                    "https://i.pinimg.com/originals/b2/79/66/b27966140db68d0621628f2309f8a443.gif",
                    "https://c.tenor.com/uNynTqoqOyUAAAAd/cry-about-it-cry.gif",
                    "https://i.kym-cdn.com/photos/images/newsfeed/002/130/364/cb2.gif",
                    "https://c.tenor.com/mugpxHrxsNAAAAAC/cry-about-it-cry.gif",
                    "https://c.tenor.com/lrK3BkjhKlYAAAAd/cry-about-it-cries-about-it.gif",
                    "https://c.tenor.com/nbcrVmO1PZgAAAAM/cry-about-it.gif",
                    "https://www.icegif.com/wp-content/uploads/smile-icegif-3.gif",
                    "https://acegif.com/wp-content/gif/crying-77.gif",
                    "https://acegif.com/wp-content/uploads/2022/4hv9xm/crying-emoji-28.gif"
                ]
        }
        if member == None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:

                gifs_list = crygifs
                gifs = gifs_list["gifs"]
                random_quote = random.randint(0, len(gifs)-1)
                
                embed = discord.Embed(description=f'<@{member.id}> cry about it', color=0x303136)
                embed.set_image(url=gifs[random_quote])
                embed.set_footer(text=f'Image may load slowly. sry!')
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                embed = discord.Embed(description=f'```Error: {e}```', color=0x303136)
                embed.set_footer(text=f'{time_log}')
                await ctx.send(embed=embed, mention_author=False)
    
    @commands.command(aliases=["flip", "coin"], enabled=True, usage='', description='Flip a coin.')
    async def coinflip(self, ctx):
        coinsides = ["Tails", "Eagle"]
        embed = discord.Embed(description=f'🪙 **{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["cr"], enabled=True, usage='<crypto symbol>', description='Sent info about crypto currency.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    async def crypto(self, ctx, symbol: str = None):

        if symbol == None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=pln&symbols={symbol}'
                r = requests.get(url).json()


                embed = discord.Embed(title=r[0]['name'], color=0x303136)
                embed.set_thumbnail(url=r[0]["image"])
                embed.add_field(name='**Price:**', value=f'{r[0]["current_price"]} PLN', inline=False)
                embed.add_field(name='**High price in last 24h:**', value=f'{r[0]["high_24h"]} PLN', inline=False)
                embed.add_field(name='**Low price in last 24h:**', value=f'{r[0]["low_24h"]} PLN', inline=False)
                embed.add_field(name='**Market Cap Rank:**', value=f'{r[0]["market_cap_rank"]}', inline=False)
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                embed = discord.Embed(description=f'```Error: {e}```', color=0x303136)
                embed.set_footer(text=f'{time_log}')
                await ctx.send(embed=embed, mention_author=False)
    

    # I don't know is this API still working. 
    # @commands.command(aliases=["cv"], enabled=True, usage='<country>', description='Sent info about covid stats in specify country.')
    # @commands.cooldown(1, 5.0, commands.BucketType.user)
    # async def covid(self, ctx, country: str = None):

    #     if country == None:
    #         await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
    #     else:
    #         try:
    #             url = f'https://corona.lmao.ninja/v2/countries/{country}'
    #             r = requests.get(url).json()

    #             embed = discord.Embed(title=r['country'], color=0x303136)
    #             embed.set_thumbnail(url=r["countryInfo"]["flag"])
    #             embed.add_field(name='**Today cases:**', value=f'{r["todayCases"]}', inline=False)
    #             embed.add_field(name='**Today deaths:**', value=f'{r["todayDeaths"]}', inline=False)
    #             embed.add_field(name='**All time cases:**', value=f'{r["cases"]}', inline=False)
    #             embed.add_field(name='**All time deaths:**', value=f'{r["deaths"]}', inline=False)
    #             embed.add_field(name='**All time recovered:**', value=f'{r["recovered"]}', inline=False)
    #             embed.add_field(name='**Tests:**', value=f'{r["tests"]}', inline=False)
    #             await ctx.reply(embed=embed, mention_author=False)

    #         except Exception as e:
    #             embed = discord.Embed(description=f'```Error: {e}```', color=0x303136)
    #             embed.set_footer(text=f'{time_log}')
    #             await ctx.send(embed=embed, mention_author=False)
    
    @commands.command(aliases=['cow'], enabled=True, usage='<text>', description='Muuuuuu!')
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def cowsay(self, ctx, *, text: str = None):
        if text == None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                url = f'http://cowsay.morecode.org/say?message={text}&format=text'
                r = requests.get(url).text
                embed = discord.Embed(description=f'```{r}```', color=0x303136)
                embed.set_footer(text=f'{embed_time_log}')
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                embed = discord.Embed(description=f'```Error: {e}```', color=0x303136)
                embed.set_footer(text=f'{time_log}')
                await ctx.send(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Fun(client))
