"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

# Main imports
import discord
from discord.ext import commands

# Console log imports
from colorama import Fore
from colorama import Style

# Command imports
import requests
import datetime
from functions.logs import log, savelog
from functions.embeds import error_embed, arguments_error_embed

now = datetime.datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

class TimestampConverter:
    def __init__(self):
        self.styles = ['t', 'T', 'd', 'D', 'f', 'F', 'R']

    def convert(self, dtm:datetime.datetime, style:str='f'):
        if style not in self.styles:
            raise ValueError("Invalid style")
        if not isinstance(dtm, datetime.datetime):
            raise TypeError("datetime.datetime object is required")
        return f"<t:{round(dtm.timestamp())}:{style}>"

    def get_styles(self):
        return self.styles

tsconv = TimestampConverter()


class Discord(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ui", 'u', 'whois'], enabled=True, usage='<user>', description='Get informations about user.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    async def user(self, ctx, member:discord.Member = None):

        try:
            user = member or ctx.author
            
            date_format = "%a, %d %b %Y"
            
            show_roles = ", ".join(
                [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
            ) if len(user.roles) > 1 else "None"

            date_format_timestamp = '%Y %m %d'

            embed = discord.Embed(title=f'{user}', color=0x303136)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Joined Discord", value=f'{user.created_at.strftime(date_format)}', inline=False)
            embed.add_field(name="Joined Server", value=f'{user.joined_at.strftime(date_format)}', inline=False)
            if len(user.roles) > 1:
                embed.add_field(name='Top role', value=f'<@&{user.top_role.id}>', inline=False)
            else:
                embed.add_field(name='Top role', value=f'{user.top_role}', inline=False)
            embed.add_field(name="Roles", value=show_roles, inline=False)
            embed.set_footer(text=f'ID: {user.id}')
            await ctx.reply(embed=embed, mention_author=False)

        except Exception as e:
            embed = discord.Embed(
                description=f'```Something went wrong: {e}```', color=0x303136)
            await ctx.send(embed=embed, mention_author=False)
            print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
    
    @commands.command(enabled=True, description='Get informations about guild.')
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def guild(self, ctx):

        try:
            bots_in_guild = sum(1 for member in ctx.guild.members if member.bot)
            
            date_format = "%a, %d %b %Y"
            
            embed = discord.Embed(title=f'{ctx.author.guild.name}', color=0x303136)
            if ctx.guild.icon:
                embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.png')
            if ctx.guild.banner:
                embed.set_image(url=f'https://cdn.discordapp.com/banners/{ctx.guild.id}/{ctx.guild.banner}.png')
            embed.add_field(name="Created", value=ctx.guild.created_at.strftime(date_format), inline=False)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=bots_in_guild, inline=True)
            embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=False)
            embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=False)
            embed.set_footer(text=f'ID: {ctx.guild.id}')
            await ctx.reply(embed=embed, mention_author=False)
        except Exception as e:
            embed = discord.Embed(description=f'```Error: {e}```', color=0x303136)
            embed.set_footer(text=f'{time_log}')
            await ctx.send(embed=embed, mention_author=False)
    
    @commands.command(aliases=['guildinv', 'gi', 'ci'], enabled=True, description='Get informations about guild per invite.', usage='<invite>')
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def checkinvite(self, ctx, invite:str = None):
        if invite is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            url = f'https://discordapp.com/api/v9/invites/{invite}?with_counts=true'
            r = requests.get(url).json()

            guild_name = r['guild']['name']
            guild_id = r['guild']['id']
            guild_icon = r['guild']['icon']
            guild_description = r['guild']['description']
            guild_boosts = r['guild']['premium_subscription_count']
            guild_avatar = f'https://cdn.discordapp.com/icons/{guild_id}/{guild_icon}'
            guild_membercount = f'{r["approximate_member_count"]}'

            if guild_description == "null":
                embed = discord.Embed(title=f'{guild_name}', color=0x303136)
            else:
                embed = discord.Embed(title=f'{guild_name}', description=f'{guild_description}', color=0x303136)
            embed.add_field(name='<:members:968882775031701524> **Members:**', value=f'{guild_membercount}', inline=True)
            embed.add_field(name='<:booster:967712095246352415> **Boosts:**', value=f'{guild_boosts}', inline=True)
            embed.add_field(name='<:booster:967712095246352415> **Invite:**', value=f'[discord.gg/{invite}](https://discord.gg/{invite})', inline=True)
            embed.set_footer(text=f'ID: {guild_id}')
            embed.set_thumbnail(url=guild_avatar)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["av"], enabled=True, description='Get user avatar.', usage='<user>')
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        user = member or ctx.author

        try:
            embed = discord.Embed(title=f'Avatar for {user}', description=f'**[WEBP]({user.avatar_url}) | [PNG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=1024) | [JPG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpg?size=1024)**', color=0x303136)
            embed.set_image(url=f'{user.avatar_url}')
            await ctx.send(embed=embed)
        except Exception as e:
            log('error', f'Error in {ctx.command} command: {e}')
            savelog('error', f'Error in {ctx.command} command: {e}')

    @commands.command(aliases=["q"], enabled=True, usage='<message>', description='Send a quote of user message.')
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def quote(self, ctx, message: discord.Message = None):
        if message is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                if message.attachments:
                    if message.content:
                        mc = message.content
                    else:
                        mc = 'No message content'
                    for attachment in message.attachments:
                        embed = discord.Embed(description=f'[{mc}]({message.jump_url})', color=0x303136)
                        embed.set_author(name=f'{message.author.name}', icon_url=message.author.avatar_url)
                        embed.set_footer(text=f'Sent on {message.guild.name}, channel {message.channel.name}')
                        await ctx.reply(embed=embed, mention_author=False)
                        await ctx.send(f'{attachment.url}')
                else:
                    embed = discord.Embed(description=f'[{message.content}]({message.jump_url})', color=0x303136)
                    embed.set_author(name=f'{message.author.name}', icon_url=message.author.avatar_url)
                    embed.set_footer(text=f'Sent on {message.guild.name}, channel {message.channel.name}')
                    await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                log('error', f'Error in {ctx.command} command: {e}')

    @commands.command(enabled=False, hidden=False, description='Translate message to specify langue.', usage='<message> <langue of message> <langue to translate>')
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def translate(self, ctx, langue_target: str = None, langue_source: str = 'en', *, message: str = None, ):
        if message is None or langue_target is None or langue_source is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

            payload = f"q={message}&target={langue_target}&source={langue_source}"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "application/gzip",
                "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
                "X-RapidAPI-Key": "KEY"
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            await ctx.reply(response.text)


def setup(client):
    client.add_cog(Discord(client))


