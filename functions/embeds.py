import discord

def error_embed(ctx, content):
    embed = discord.Embed(description=f'<:cross:967762235743150121> {content}', color=0x303136)
    return embed

def arguments_error_embed(ctx):
    embed = discord.Embed(title=ctx.command.description, description=f'**Usage:** \n```{ctx.command.name} {ctx.command.usage}```\n**Aliases:**\n{", ".join(ctx.command.aliases)}', color=0x303136)
    embed.set_footer(text=f'Cog {ctx.command.cog_name}')
    return embed