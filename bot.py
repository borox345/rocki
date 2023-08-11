"""
Created by: borox
https://borox.site
Cloned from: https://github.com/borox345/rocki
"""

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import os
from datetime import datetime
from colorama import Fore
from colorama import Style
from config import TOKEN, PREFIX, LOGS, OWNER
from data.utils import messages
import sqlite3
from functions.logs import log
from functions.embeds import arguments_error_embed

intents = discord.Intents.default()
client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER, intents=intents)


date_format = "%a, %d %b %Y"

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

db = sqlite3.connect("data/db_main.db")
c = db.cursor()

@client.event
async def on_guild_join(guild):
    wl = c.execute("SELECT id FROM wl_guilds").fetchall()
    log = client.get_channel(LOGS)

    if (guild.id,) in wl:
        await log.send(f'```asciidoc\n=== NEW GUILD ===\nName:: {guild.name} \nId:: {guild.id} \nMembers:: {guild.member_count - 1} \nCreated at:: {guild.created_at.strftime(date_format)}```')
        return
    else:
        await log.send(f'```asciidoc\n=== GUILD WITHOUT WHITELIST ===\nName:: {guild.name} \nId:: {guild.id} \nMembers:: {guild.member_count - 1} \nCreated at:: {guild.created_at.strftime(date_format)}```')

        if guild.system_channel:
            try:
                await guild.system_channel.send(messages.guildwl_leave)
            except discord.Forbidden:
                pass
        print(f'{Fore.YELLOW}[INFO] {time_log} Leaving from {guild.name} ({guild.id}) {Style.RESET_ALL}')

        await log.send(f'```asciidoc\n=== LEAVING FROM GUILD ===\nName:: {guild.name} \nId:: {guild.id} \nMembers:: {guild.member_count - 1} \nCreated at:: {guild.created_at.strftime(date_format)}```')
        return await guild.leave()

@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f'cogs.{filename[:-3]}')
                print(f'{Fore.MAGENTA}[INFO] {time_log} Loaded extension {filename} {Style.RESET_ALL}')
            except Exception as e:
                print(f'{Fore.RED}[ERROR] {time_log} Failed to load plugin {filename}. {e} {Style.RESET_ALL}')


    print(f'{Fore.YELLOW}[WARNING] {time_log} Checking guilds {Style.RESET_ALL}')
    guild_leave_number = 0
    client.count_of_memnbers = 0
    for guild in client.guilds:
        wl = c.execute("SELECT id FROM wl_guilds").fetchall()

        if (guild.id,) in wl:
            client.count_of_memnbers += guild.member_count
        else:
            log = client.get_channel(LOGS)
            await log.send(f'```asciidoc\n=== GUILD WITHOUT WHITELIST ===\nName:: {guild.name} \nId:: {guild.id} \nMembers:: {guild.member_count - 1} \nCreated at:: {guild.created_at.strftime(date_format)}```')

            if guild.system_channel:
                try:
                    await guild.system_channel.send(messages.guildwl_leave)
                except discord.Forbidden:
                    pass
            print(f'{Fore.YELLOW}[INFO] {time_log} Leaving from {guild.name} ({guild.id}) {Style.RESET_ALL}')
            await log.send(f'```asciidoc\n=== LEAVING FROM GUILD ===\nName:: {guild.name} \nId:: {guild.id} \nMembers:: {guild.member_count} \nCreated at:: {guild.created_at.strftime(date_format)}```')
            return await guild.leave()

    print(f'{Fore.MAGENTA}[INFO] {time_log} Starting client in directory: {os.getcwd()} {Style.RESET_ALL}')
    print(f'{Fore.MAGENTA}[INFO] {time_log} Starting with {len(client.guilds)} guilds and {client.count_of_memnbers} users. {Style.RESET_ALL}')
    print(f'{Fore.GREEN}[INFO] {time_log} Client {client.user.name} is ready. {Style.RESET_ALL}')
    await client.change_presence(activity=discord.Game(name=f"?help"))

@client.check
async def blacklist_check(ctx):
    blacklist = c.execute("SELECT id FROM blacklist").fetchall()
    if (ctx.author.id,) in blacklist:
        reason = c.execute("SELECT reason FROM blacklist WHERE id = ?", (ctx.author.id,)).fetchone()
        await ctx.reply(f'You are banned from using this bot for ``{reason[0]}``', mention_author=False)
        return False
    else:
        return True

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(description=f'<:cross:967762235743150121> <@{ctx.author.id}>: **Try again in** ``{round(error.retry_after)}`` **seconds.**', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)

    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(description=f'<:cross:967762235743150121> <@{ctx.author.id}>: **Command not found.**', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)

    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(description=f'<:cross:967762235743150121> <@{ctx.author.id}>: **This command is disabled.**', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)
        
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description=f"<:cross:967762235743150121> <@{ctx.author.id}>: **You don't have requied permissions.**", color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)
    
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f'<:cross:967762235743150121> <@{ctx.author.id}>: **Missing required argument.**', color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)

    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(description=f"<:cross:967762235743150121> <@{ctx.author.id}>: **You are not the owner.**", color=0x303136)
        await ctx.reply(embed=embed, mention_author=False, delete_after=5)


client.run(TOKEN)
