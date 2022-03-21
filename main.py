# -------------------------------IMPORTS----------------------------------
import random
import discord
from discord.ext import commands
import json
from datetime import datetime
import os
# -------------------------------IMPORTS----------------------------------


intents = discord.Intents.default()
intents.members = True

def get_prefix(bot, msg):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(msg.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    bot.load_extension("cogs.wordle")
    await bot.change_presence(activity=discord.Game(name='My prefix is on my nickname on the server!'))
    print('bot is ready')


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '>'
    await guild.me.edit(nick='(>)Wordle')
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title="Commands",
        description="""
        **This is my list of commands.**
        `My prefix is on my nickname!`
        """,
        colour=0x87CEEB,
        timestamp=datetime.utcnow())
    embed.set_author(name=ctx.message.author.name,
                     icon_url="https://avatars.githubusercontent.com/u/16879430")
    embed.add_field(
        name="wordle",
        value="""
        Will start your game!\n`{prefix}wordle`
        """,
        inline=False
    )
    embed.add_field(
        name="changeprefix",
        value="""
        Will change your prefix!\n`{current prefix}prefix {new prefix}`
        """,
        inline=False
    )
    embed.set_footer(text="Wow! A footer!",
                     icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
    await ctx.send(embed=embed)

@bot.command(name='changeprefix')
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix=None):
    if prefix == None:
        await ctx.send(f'Please provide your prefix after "changeprefix"')
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f'your prefix is now "{prefix}"')
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.guild.me.edit(nick=f'({prefix})Wordle')


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot:
        return

    else:
        with open('wordle.json', 'r') as f:
            data = json.load(f)

        if data[str(user.id)]['wordle_userid'] == str(user.id) and data[str(user.id)]['wordle_msgid'] == str(reaction.message.id) and str(reaction.emoji) == '❓':
            dm = await user.create_dm()
            embed = discord.Embed(
                title="How to play?",
                description="""
                Grey letter means that letter is not in the word! \nYellow letter means that is in the word but not at the right place! \nGreen letter means that letter is in the word and at right place!
                """,
                colour=0x87CEEB,
                timestamp=datetime.utcnow())
            embed.set_author(name=user.name,
                            icon_url="https://avatars.githubusercontent.com/u/16879430")
            embed.set_footer(text="Wow! A footer!",
                            icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
            await dm.send(embed=embed)
            await reaction.remove(user)
            channel = reaction.message.channel
            await channel.send('Check your dm!', delete_after= 10)

        if data[str(user.id)]['wordle_userid'] == str(user.id) and data[str(user.id)]['wordle_msgid'] == str(reaction.message.id) and str(reaction.emoji) == '⚠️':
            dm = await user.create_dm()
            embed = discord.Embed(
                title="Hint!",
                description=f"""
                ||{data[str(user.id)]['hint']}|| is present in your word!
                """,
                colour=0x87CEEB,
                timestamp=datetime.utcnow())
            embed.set_author(name=user.name,
                            icon_url="https://avatars.githubusercontent.com/u/16879430")
            embed.set_footer(text="Wow! A footer!",
                            icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png")
            await dm.send(embed=embed)
            await reaction.remove(user)
            channel = reaction.message.channel
            await channel.send('Check your dm!', delete_after= 10)

            



@changeprefix.error
async def changeprefix_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return  # Return because we don't want to show an error for every command not found
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)


bot.run('OTU1NTEzNDYwNDU0NzI3ODIx.YjixQQ.i7mbFm8cyGSN9c7UO-Yo1fIadJc')