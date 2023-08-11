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
from config import OWNER

# Command imports
import textwrap
import traceback
import io
from contextlib import redirect_stdout
from functions.embeds import error_embed, arguments_error_embed

now = datetime.now()
time_log = now.strftime("[%d/%m/%Y %H:%M:%S]")

class Eval(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command(aliases=["e"], enabled=True, usage='<code>', description='Evaluate code.')
    @commands.is_owner()
    async def eval(self, ctx, *, body: str = None):
        if body is None:
            await ctx.reply(embed=arguments_error_embed(ctx), mention_author=False, delete_after=5)
        else:


            try:

                def cleanup_code(content):
                    """Automatically removes body blocks from the body."""
                    if content.startswith('```') and content.endswith('```'):
                        return '\n'.join(content.split('\n')[1:-1])

                    return content.strip('` \n')

                env = {
                    'client': self.client,
                    'bot': self.client,
                    'ctx': ctx,
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'message': ctx.message,
                }

                env.update(globals())

                body = cleanup_code(body)
                stdout = io.StringIO()
                to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

                try:
                    exec(to_compile, env)
                except Exception as e:
                    embed = discord.Embed(f'```py\n>>> {body} \n \n{e.__class__.__name__}: {e}\n```', color=0x303136)
                    await ctx.reply(embed=embed, mention_author=False, delete_after=10)

                func = env['func']
                try:
                    with redirect_stdout(stdout):
                        ret = await func()
                except Exception as e:
                    value = stdout.getvalue()
                    embed = discord.Embed(description=f'```py\n>>> {body} \n \n{traceback.format_exc()}\n```', color=0x303136)
                    await ctx.send(embed=embed, delete_after=10, mention_author=False)
                else:
                    value = stdout.getvalue()
                    try:
                        await ctx.message.add_reaction('<:check:967823940162568303>')
                    except:
                        pass

                    if ret is None:
                        if value:
                            embed = discord.Embed(description=f'```py\n>>> {body} \n \n{value}\n```', color=0x303136)
                            await ctx.reply(embed=embed, mention_author=False)
                    else:
                        self._last_result = ret
                        embed = discord.Embed(description=f'```py\n>>>> {body} \n \n{value}{ret}\n```', color=0x303136)
                        await ctx.reply(embed=embed, mention_author=False)

            except Exception as e:
                embed = discord.Embed(description=f'```py\n >>> {body}\n \n {e}```', color=0x303136)
                await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(Eval(client))
