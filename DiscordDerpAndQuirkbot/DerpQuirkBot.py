from fileinput import filename
from glob import glob
import random
import os
import discord
from discord.ext import commands

userList = []
colors = [discord.Color.blue(), discord.Color.purple(), discord.Color.orange(), discord.Color.random()]
derpHigh = 10
derpLow = 1
derpHit = 1
derpsEnabled = True

bot = commands.Bot(command_prefix=':)')
client = discord.Client()
file = "TheOGPack"
fileName = '%s.txt' % file

derpFile = "DerpsForAll.txt"

GetTarget = "Target"

triggerQuirk = False

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name = "SetDerpOdds")
async def setDerpOdds(ctx, message):
    global derpHigh
    if (message.isnumeric() == True):
        derpHigh = int(message)
        await ctx.send("Cool beans odds changed to 1 in " + str(derpHigh))
    else:
        await ctx.send("Sorry but apparently " + message + " isn't a number")

@bot.command(name = "DisableDerps")
async def disableDerps():
    global derpsEnabled
    derpsEnabled = False

@bot.command(name = "EnableDerps")
async def enableDerps():
    global derpsEnabled
    derpsEnabled = True

@bot.command(name = "OGDeck")
async def setPackOG(ctx):
    global fileName
    fileName = "TheOGPack.txt"
    await ctx.send("OG Deck Selected!")

@bot.command(name = "StreamDeck")
async def setPackStream(ctx):
    global fileName
    fileName = "StreamPack.txt"
    await ctx.send("Stream Pack Selected!")

@bot.command(name = "CactusDeck")
async def setPackCactus(ctx):
    global fileName
    fileName = "CactusDeck.txt"
    await ctx.send("Cactus Deck Selected!")

@bot.command(name = "CurrentDeck")
async def getPackName(ctx):
    message = fileName.replace(".txt", "")
    await ctx.send("Current Pack: " + message)

@bot.command(name = "DM")
async def message(ctx, user:discord.Member, *, message=None):
    message = "If i could prove that I never touched my balls would you promise not to tell another soul what you saw?"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

@bot.command(name = "JoinGame")
async def joinGame(ctx):
    userList.append(ctx.message.author)
    await ctx.send(f"{ctx.author.name} Joined Quirk And Derps!")

@bot.command(name = "KickUser")
async def message(ctx, user:discord.Member, *, message=None):
    userList.remove(user)
    await ctx.send("Kicked them if they were in the game lol")


@bot.command(name = "LeaveGame")
async def leaveGame(ctx):
    userList.remove(ctx.message.author)
    await ctx.send(f"{ctx.author.name} has left Quirk And Derps!")

@bot.command(name = "StartGame")
async def sendMessage(ctx):

    global triggerQuirk
    triggerQuirk = False

    if ((random.randint(derpLow, derpHigh) == derpHit) and derpsEnabled == True):
        derpEmbed = getDerp()
        for i in userList:
            await i.send(embed = derpEmbed)

            if ("Quite Quirky" in derpEmbed.description):
                embedQ1 = getQuirk(i)
                embedQ2 = getQuirk(i)
                await i.send(embed = embedQ1)
                await i.send(embed = embedQ2)


    for i in userList:
        embed = getQuirk(i)
        await i.send(embed = embed)

        if (triggerQuirk):
            await i.send("Someone has a trigger quirk (A phrase or word will trigger them to do an action)")


@bot.command(name = "GiveQuirk")
async def message(ctx, user:discord.Member, *, message=None):
    embed = getQuirk(user)
    await user.send(embed = embed)

def getDerp():
    fileraw = open(derpFile, 'r')
    derps = fileraw.readlines() 
    chosen_Derp = random.choice(derps)

    if ("QUIRK" in chosen_Derp):
        fileraw = open(fileName, 'r')
        quirks = fileraw.readlines() 
        chosen_Quirk = random.choice(quirks)
        chosen_Derp = chosen_Derp.replace("QUIRK", chosen_Quirk)
    
    if ("Target" in chosen_Derp):
        target = random.choice(userList)
        chosen_Derp = chosen_Derp.replace("Target", target.name)
    
    chosen_Color = random.choice(colors)
    derp = discord.Embed(title="GLOBAL DERP")
    derp.description = chosen_Derp
    derp.color = discord.Color.gold()

    fileraw.close()

    return derp
    

def getQuirk(user):
    fileraw = open(fileName, 'r')
    quirks = fileraw.readlines() 
    chosen_Quirk = random.choice(quirks)
   
   
    if (GetTarget in chosen_Quirk):
        Target = random.choice(userList)
        while (Target == user):
            Target = random.choice(userList)
        chosen_Quirk = chosen_Quirk.replace("Target", Target.name)
    
    if ("TRIGGER" in chosen_Quirk):
        global triggerQuirk 
        triggerQuirk = True
        chosen_Quirk = chosen_Quirk.replace("TRIGGER", "")

    chosen_Color = random.choice(colors)
    embed = discord.Embed(title=chosen_Quirk)
    embed.title = "Your Quirk"
    embed.description = chosen_Quirk
    embed.color = chosen_Color

    fileraw.close()
    return embed
    

@bot.command(name = "test")
async def test(ctx):
     await ctx.send(userList[0])


@bot.command(name = "Party")
async def test(ctx):
    await ctx.send("Current Party:")
    PartyText = ""
    for i in userList:
        PartyText += i + "\n"

       
    await ctx.send(PartyText)

bot.run("{INSERT TOKEN ERE}")
