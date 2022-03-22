import discord
from discord.ext import commands
import time
import datetime
from discord.utils import get
import asyncio
import json
import enchant
d = enchant.Dict('en_IN')
from random_word import RandomWords
r = RandomWords()
import random



class Wordle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wordle(self, ctx):
        with open('wordle_streak.json', 'r') as f:
            streak = json.load(f)

        if str(ctx.author.id) not in streak:
            streak[str(ctx.author.id)] = '0'

        line = 6
        with open('grey.json', 'r') as f:
            grey = json.load(f)
        with open('yellow.json', 'r') as f:
            yellow = json.load(f)
        with open('green.json', 'r') as f:
            green = json.load(f)
        l1= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        l2= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        l3= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        l4= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        l5= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        l6= [grey["box"],grey["box"],grey["box"],grey["box"],grey["box"]]
        def lay():
            line1 = ''
            line2 = ''
            line3 = ''
            line4 = ''
            line5 = ''
            line6 = ''
            for i in l1:
                line1 = line1 + i
            for i in l2:
                line2 = line2 + i
            for i in l3:
                line3 = line3 + i
            for i in l4:
                line4 = line4 + i
            for i in l5:
                line5 = line5 + i
            for i in l6:
                line6 = line6 + i

            return f'{line1}\n{line2}\n{line3}\n{line4}\n{line5}\n{line6}'


        
        while True:
            ans = r.get_random_word(minLength= 5, maxLength= 5,hasDictionaryDef="true")
            if d.check(ans) == True:
                ans = ans.lower()
                break
            else:
                continue

        with open('wordle.json ', 'r') as f:
            data = json.load(f)

        if str(ctx.author.id) in data:
            await ctx.send('Your game is already running somewhere! Please complete that game or quit it before starting new game!')

        else:
            print(ans)
            screen = lay()
            emb = discord.Embed(
                title='❓ ==> `React to know about game`\n ⚠️ ==> `React to get hint!`',
                description=screen,
                colour=0x87CEEB,
                timestamp=datetime.datetime.utcnow()
            )
            emb.set_author(name=ctx.author.name,
                            icon_url="https://avatars.githubusercontent.com/u/16879430")
            main_msg = await ctx.send(embed=emb)
            await main_msg.add_reaction('❓')
            await main_msg.add_reaction('⚠️')

            hint = random.choice(ans)

            with open('wordle.json ', 'r') as f:
                data = json.load(f)
            data[str(ctx.author.id)] = {}
            data[str(ctx.author.id)]['ans'] = ans
            data[str(ctx.author.id)]['wordle_userid'] = str(ctx.author.id)
            data[str(ctx.author.id)]['wordle_msgid'] = str(main_msg.id)
            data[str(ctx.author.id)]['hint'] = hint
            with open('wordle.json ', 'w') as f:
                json.dump(data, f, indent=4)
                
            while line>0:
                while True:
                    try:
                        msg = await self.bot.wait_for(
                            'message', 
                            timeout= 600,
                            check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                        )

                        messg = msg.content.lower()
                        await msg.delete()
                        print(messg)
                        if len(messg) != 5:
                            await ctx.send('Please enter only 5 letters word!', delete_after= 10)
                        else:
                            if d.check(messg) == False:
                                await ctx.send('Please enter meaningful word', delete_after = 10)
                            else:
                                
                                if messg == ans:
                                    if line == 6:
                                        l1.clear()
                                        for j in messg:
                                            l1.append(green[j])
                                    if line == 5:
                                        l2.clear()
                                        for j in messg:
                                            l2.append(green[j])
                                    if line == 4:
                                        l3.clear()
                                        for j in messg:
                                            l3.append(green[j])
                                    if line == 3:
                                        l4.clear()
                                        for j in messg:
                                            l4.append(green[j])
                                    if line == 2:
                                        l5.clear()
                                        for j in messg:
                                            l5.append(green[j])
                                    if line == 1:
                                        l6.clear()
                                        for j in messg:
                                            l6.append(green[j])

                                    streak[str(ctx.author.id)] = str(int(streak[str(ctx.author.id)])+1)
                                    with open('wordle_streak.json', 'w') as f:
                                        json.dump(streak, f, indent=4)

                                    emb = discord.Embed(
                                        title = f'You won!\n`Your winning streak is {streak[str(ctx.author.id)]}!`',
                                        description=lay(),
                                        colour=0x87CEEB,
                                        timestamp=datetime.datetime.utcnow()
                                    )
                                    emb.set_author(name=ctx.author.name,
                                                icon_url="https://avatars.githubusercontent.com/u/16879430")
                                    await main_msg.edit(embed = emb)
                                    
                                    with open('wordle.json ', 'r') as f:
                                        data = json.load(f)
                                    del data[str(ctx.author.id)]
                                    with open('wordle.json ', 'w') as f:
                                        json.dump(data, f, indent=4)


                                    line = 0
                                    break
                                else:
                                    if line == 6:
                                        l1.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l1.append(green[ans[k]])
                                                else:
                                                    l1.append(yellow[messg[k]])
                                            else:
                                                l1.append(grey[messg[k]])
                                    elif line == 5:
                                        l2.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l2.append(green[ans[k]])
                                                else:
                                                    l2.append(yellow[messg[k]])
                                            else:
                                                l2.append(grey[messg[k]])
                                    elif line == 4:
                                        l3.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l3.append(green[ans[k]])
                                                else:
                                                    l3.append(yellow[messg[k]])
                                            else:
                                                l3.append(grey[messg[k]])
                                    elif line == 3:
                                        l4.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l4.append(green[ans[k]])
                                                else:
                                                    l4.append(yellow[messg[k]])
                                            else:
                                                l4.append(grey[messg[k]])
                                    elif line == 2:
                                        l5.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l5.append(green[ans[k]])
                                                else:
                                                    l5.append(yellow[messg[k]])
                                            else:
                                                l5.append(grey[messg[k]])
                                    elif line == 1:
                                        l6.clear()
                                        for k in range(len(messg)):
                                            if messg[k] in ans:
                                                if messg[k] == ans[k]:    
                                                    l6.append(green[ans[k]])
                                                else:
                                                    l6.append(yellow[messg[k]])
                                            else:
                                                l6.append(grey[messg[k]])
                                    emb = discord.Embed(
                                        title='❓ ==> `React to know about game`\n ⚠️ ==> `React to get hint!`',
                                        description=lay(),
                                        colour=0x87CEEB,
                                        timestamp=datetime.datetime.utcnow()
                                    )
                                    emb.set_author(name=ctx.author.name,
                                                icon_url="https://avatars.githubusercontent.com/u/16879430")
                                    await main_msg.edit(embed = emb)
                                    line = line -1
                                    if line == 0:
                                        with open('wordle.json ', 'r') as f:
                                            data = json.load(f)
                                        del data[str(ctx.author.id)]
                                        with open('wordle.json ', 'w') as f:
                                            json.dump(data, f, indent=4)

                                        streak[str(ctx.author.id)] = '0'
                                        with open('wordle_streak.json', 'w') as f:
                                            json.dump(streak, f, indent=4)

                                        emb = discord.Embed(
                                            title=f'**You lost!, Better luck next time**\n`Your Streak is now 0`\nAnswer--> *{ans}*',
                                            description=lay(),
                                            colour=0x87CEEB,
                                            timestamp=datetime.datetime.utcnow()
                                        )
                                        emb.set_author(name=ctx.author.name,
                                                    icon_url="https://avatars.githubusercontent.com/u/16879430")
                                        await main_msg.edit(embed = emb)
                                        break

                    except asyncio.TimeoutError:
                        await main_msg.delete()
                        await ctx.send('Game over due to timeout' , delete_after= 10)
                        with open('wordle.json ', 'r') as f:
                                data = json.load(f)
                        del data[str(ctx.author.id)]
                        with open('wordle.json ', 'w') as f:
                            json.dump(data, f, indent=4)
                        break
    
    @wordle.error
    async def wordle_error(self, ctx: commands.Context, error: commands.CommandError):
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

    

def setup(bot):
    bot.add_cog(Wordle(bot))
