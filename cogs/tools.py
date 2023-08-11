"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

import os
import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore
from colorama import Style
import sqlite3
from asyncio import sleep
from config import OWNER
from functions.embeds import arguments_error_embed
from functions.logs import log

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")
embed_time_log = now.strftime("%H:%M:%S")

db = sqlite3.connect("data/db_main.db")
c = db.cursor()

class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command

    @commands.command(aliases=["r", 'rr'], enabled=True, hidden=True, usage='<extension>', description='Reloads a extenstion.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def reload(self, ctx, extension: str = None):
        if extension is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                self.client.unload_extension(f'cogs.{extension}')
                self.client.load_extension(f'cogs.{extension}')

                embed = discord.Embed(description=f'✅ Reloaded extension ``{extension}.py``', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False)

                print(f'{Fore.MAGENTA}[INFO] {time_log} Reloaded {extension}.py {Style.RESET_ALL}')
            except discord.ext.commands.errors.ExtensionNotLoaded:
                embed = discord.Embed(description=f'Extension ``{extension}`` does not exist', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False, delete_after=5)

    @commands.command(aliases=["massreload", 'ra'], enabled=True, hidden=True, usage='', description='Reload all cogs.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def reloadall(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                    self.client.load_extension(f'cogs.{filename[:-3]}')
                    print(f'{Fore.MAGENTA}[INFO] {time_log} Reloaded extension {filename} {Style.RESET_ALL}')
                except Exception as e:
                    print(f'{Fore.RED}[ERROR] {time_log} Failed to reload plugin {filename}. {e} {Style.RESET_ALL}')
                    embed = discord.Embed(description=f'Failed to reload extension ``{filename}``', color=0x303136)
                    await ctx.reply(embed=embed, mention_author=False, delete_after=5)
                    pass
            
        embed = discord.Embed(description=f'✅ Reloaded all extensions', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(enabled=True, hidden=True, usage='<extension>', descrtipion='Load extension')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def load(self, ctx, extension: str = None):
        if extension is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                self.client.load_extension(f'cogs.{extension}')

                embed = discord.Embed(description=f'✅ Loaded extension ``{extension}.py``', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False)

                print(f'{Fore.MAGENTA}[INFO] {time_log} Loaded {extension}.py {Style.RESET_ALL}')
            except discord.ext.commands.errors.ExtensionNotLoaded:
                embed = discord.Embed(description=f'Extension ``{extension}`` does not exist', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False, delete_after=5)

    @commands.command(enabled=True, hidden=True, usage='<extension>', description='Unloads extension.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def unload(self, ctx, extension: str = None):

        if extension is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                self.client.unload_extension(f'cogs.{extension}')

                embed = discord.Embed(description=f'✅ Unloaded extension ``{extension}.py``', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False)

                print(f'{Fore.MAGENTA}[INFO] {time_log} Loaded {extension}.py {Style.RESET_ALL}')
            except discord.ext.commands.errors.ExtensionNotLoaded:
                embed = discord.Embed(description=f'Extension ``{extension}`` does not exist', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False, delete_after=5)
    
    @commands.command(enabled=True, hidden=True, usage='<query>', aliases=['db'], description='Execute sql query.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def sql(self, ctx, *, arg = None):
        if arg is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                r = c.execute(arg).fetchall()
                db.commit()
                embed = discord.Embed(description=f'```sql\n>>> {arg} \n \n{r}```', color=0x303136)
                embed.set_footer(text=f'{embed_time_log}')
                await ctx.message.add_reaction('<:check:967823940162568303>')
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                embed = discord.Embed(description=f'```sql\n>>> {arg} \n \nError: {e}```', color=0x303136)
                embed.set_footer(text=f'{embed_time_log}')
                embed.set_footer(text=f'{time_log}')
                await ctx.message.add_reaction('<:cross:967762235743150121>')
                await ctx.send(embed=embed, mention_author=False)

    @commands.command(enabled=True, hidden=True, usage='<guild id>', aliases=['exit'], description='The bot leaves from the specific guild.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def leave(self, ctx, *, guild_id: int = None):
        if guild_id is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                guild = self.client.get_guild(guild_id)
                if guild:
                    embed= discord.Embed(description=f'👍, i left from **{guild.name}** (``{guild_id}``)', color=0x303136)
                    await ctx.reply(embed=embed, mention_author=False)
                    if guild.system_channel:
                        await guild.system_channel.send('Leaving from this guild...')
                    else:
                        pass
                    print(f'{Fore.YELLOW}[INFO] {time_log} I left from {guild.name} ({guild_id}) {Style.RESET_ALL}')
                    await self.client.get_guild(guild_id).leave()
                else:
                    embed = discord.Embed(description=f'👎, guild with id ``{guild_id}`` does not exist or im not there.', color=0x303136)
                    await ctx.reply(embed=embed, mention_author=False, delete_after=5)
            except Exception as e:
                await ctx.reply('👎', mention_author=False, delete_after=5)
                print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
                pass
    
    @commands.command(enabled=True, hidden=True, usage='<add|remove> <member> <reason>', aliases=['blacklist', 'removemoron'], description='Add or remove member from blacklist.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def botban(self, ctx, action: str = None, member: discord.Member = None , * , reason: str = 'no reason'):
        def add(user_id: int, reason: str):
            c.execute(f'INSERT INTO blacklist (id, reason) VALUES({user_id}, "{reason}")')
            db.commit()
            print(f'{Fore.YELLOW}[INFO] {time_log} Blacklisted user with id {user_id} {Style.RESET_ALL}')

        def remove(user_id: int):
            c.execute(f'DELETE FROM blacklist WHERE id = ({user_id})')
            db.commit()
            print(f'{Fore.YELLOW}[INFO] {time_log} Removed {user_id} from blacklist. {Style.RESET_ALL}')

        try:
            if action is None or member is None:
                await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
            elif action == 'add':
                if (member.id,) not in c.execute('SELECT id FROM blacklist').fetchall():
                    add(member.id, reason)
                    await ctx.reply(f'👍, Blacklisted **{member}** for ``{reason}``.', mention_author=False)
                else:
                    await ctx.reply(f'👎, User with id ``{member.id}`` is already on blacklist.', mention_author=False)
            elif action == 'remove':
                if (member.id,) in c.execute('SELECT id FROM blacklist').fetchall():
                    remove(member.id)
                    await ctx.reply(f'👍, Removed **{member}** from blacklist.', mention_author=False) 
                else:
                    await ctx.reply(f'👎, User with id ``{member.id}`` is not on blacklist.', mention_author=False)
            
        except Exception as e:
            await ctx.reply('👎', mention_author=False, delete_after=5)
            print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
            pass
        
    @commands.command(enabled=True, hidden=True, usage='<add|remove> <guild id>', aliases=['whitelist', 'addguild'], description='Gives access to the bot for guilds.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def wl(self, ctx, action: str = None, guild_id: int = None):
        def add(guild_id: int):
            c.execute(f'INSERT INTO wl_guilds(id) VALUES({guild_id})')
            db.commit()

        def remove(guild_id: int):
            c.execute(f'DELETE FROM wl_guilds WHERE id = ({guild_id})')
            db.commit()

        try:
            if action is None:
                await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
            elif action == 'add':
                if (guild_id, ) not in c.execute('SELECT id FROM wl_guilds').fetchall():
                    add(guild_id)
                    await ctx.reply(f'👍, Added guild with id ``{guild_id}``to whitelist.', mention_author=False)
                else:
                    await ctx.reply(f'👎, Guild with id ``{guild_id}`` is already on whitelist.', mention_author=False)
            elif action == 'remove':
                if (guild_id, ) in c.execute('SELECT id FROM wl_guilds').fetchall():
                    remove(guild_id)
                    await ctx.reply(f'👍, Removed guild with id ``{guild_id}`` from whitelist.', mention_author=False)
                else:
                    await ctx.reply(f'👎, Guild with id ``{guild_id}`` is not on whitelist.', mention_author=False)
            
        except Exception as e:
            await ctx.reply('👎', mention_author=False, delete_after=5)
            print(f'{Fore.RED}[ERROR] {time_log} {e} {Style.RESET_ALL}')
            pass

    @commands.command(enabled=True, hidden=True, usage='<query>', aliases=['sh', 'terminal'], description='Execute shell command.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def shell(self, ctx, *, query: str = None):
        try:
            if query is None:
                await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
            else:
                r = os.popen(query).read()
                embed = discord.Embed(title=query, description=f'```{r}```', color=0x303136)
                embed.set_footer(text=f'{embed_time_log}')
                embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                await ctx.message.add_reaction('<:check:967823940162568303>')
                await ctx.reply(embed=embed, mention_author=False)
        except Exception as e:
            embed = discord.Embed(title=query, description=f'```{r}```', color=0x303136)
            embed.set_footer(text=f'{embed_time_log}')
            embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            await ctx.reply(embed=embed, mention_author=False, delete_after=5)
            await ctx.message.add_reaction('<:cross:967762235743150121>')
            pass

    @commands.command(enabled=True, hidden=True, usage='<>', description='Sends dm message to user.')
    @commands.cooldown(1, 4.0, commands.BucketType.user)
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User = None, *, message: str = None):
        if user is None or message is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:
            try:
                await user.send(message)
                await ctx.reply(f'👍, Sent message to {user}.', mention_author=False)
            except Exception as e:
                await ctx.reply(f'👎, Failed to send message to {user}.', mention_author=False)
                log('error', f'{e}')
                pass


def setup(client):
    client.add_cog(Tools(client))
