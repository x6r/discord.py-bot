import discord, json
import random, time
from discord.ext import commands

with open("config.json", "r") as read_file:
    config = json.load(read_file)

##############################################
##############################################
########### VARS + READY EVENT
##############################################
##############################################

token = config.get('token')
prefix = config.get('prefix')
desc = config.get('description')
status = config.get('playingstatus')
owner_id = config.get('id')

bot = commands.Bot(command_prefix = prefix)
bot.remove_command('help')

@bot.event
async def on_command_error(error, ctx):
    print("Error: Missing argument?")

responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
]


@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(activity=discord.Game(status))

##############################################
##############################################
########### GENERAL COMMANDS
##############################################
##############################################

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: | Pong! {round(bot.latency * 1000)}ms')

@bot.command(aliases=["stats"])
async def version(ctx):
    embed=discord.Embed(title=f"{bot.user.display_name} Stats", description=desc, color=0xff0000)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    await ctx.send(embed=embed)

##############################################
##############################################
########### FUN COMMANDS
##############################################
##############################################

@bot.command(aliases=["gay"])
async def gayrate(ctx, member:discord.Member=None):
    gr = random.randint(1, 100)
    if not member:
        embed=discord.Embed(title=f"{ctx.author.display_name} is {gr}% gay", description="\n", color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"{member.display_name} is {gr}% gay", description="\n", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(aliases=["thot"])
async def thotrate(ctx, member:discord.Member=None):
    gr = random.randint(1, 100)
    if not member:
        embed=discord.Embed(title=f"{ctx.author.display_name} is {gr}% thot", description="\n", color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"{member.display_name} is {gr}% thot", description="\n", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    embed=discord.Embed(title="8ball", color=0xff0000)
    embed.add_field(name="Question:", value=question, inline=True)
    embed.add_field(name="Answer:", value=random.choice(responses), inline=True)
    await ctx.send(embed=embed)

##############################################
##############################################
########### MODERATION COMMANDS
##############################################
##############################################

@bot.command()
@commands.has_permissions(administrator=True)
async def randomban(ctx):
    member = random.choice(ctx.guild.members)
    embed=discord.Embed(title="randomban", description=f"{member.mention} was banned", color=0xff0000)
    await member.ban()
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def randomkick(ctx):
    member = random.choice(ctx.guild.members)
    embed=discord.Embed(title="randomkick", description=f"{member.mention} was kicked", color=0xff0000)
    await member.kick()
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member=None):
    if not member:
        await ctx.send("Error: Missing mention")
    else:
        embed=discord.Embed(title="kick", description=f"{member.mention} was kicked", color=0xff0000)
        await member.kick()
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None):
    if not member:
        await ctx.send("Error: Missing mention")
    else:
        embed=discord.Embed(title="ban", description=f"{member.mention} was banned", color=0xff0000)
        await member.ban()
        await ctx.send(embed=embed)

##############################################
##############################################
########### INFORMATION COMMANDS
##############################################
##############################################

@bot.command(aliases=["whois", "uinfo"])
async def userinfo(ctx, member:discord.Member=None):
    if not member:
        embed=discord.Embed(title="User Info", url=f"https://discoid.cc/{ctx.author.id}", description=f"<@{ctx.author.id}>", color=0xff0000)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Joined", value=ctx.author.joined_at.strftime("%a, %b %d, %Y"), inline=True)
        embed.add_field(name="Created", value=ctx.author.created_at.strftime("%a, %b %d, %Y"), inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="User Info", url=f"https://discoid.cc/{member.id}", description=f"<@{member.id}>", color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%a, %b %d, %Y"), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%a, %b %d, %Y"), inline=True)
        await ctx.send(embed=embed)

@bot.command(aliases=["guildinfo", "ginfo"])
async def serverinfo(ctx):
    embed=discord.Embed(title="Server Info", color=0xff0000)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Created", value=ctx.guild.created_at.strftime("%a, %b %d, %Y"), inline=True)
    embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Channel Count (t/v)", value=f"{len(ctx.guild.text_channels)} / {len(ctx.guild.voice_channels)}", inline=True)
    embed.add_field(name="Role Count", value=f"{len(ctx.guild.roles)}", inline=True)
    embed.add_field(name="Region", value=ctx.guild.region, inline=True)
    embed.add_field(name="Owner", value=f"<@{ctx.guild.owner_id}>", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=["cmds", "commands", "help"])
async def _help(ctx):
    embed=discord.Embed(title="Help Menu", description=f"{desc}", color=0xff0000)
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.add_field(name=f"{prefix}moderation", value="Moderation commands", inline=True)
    embed.add_field(name=f"{prefix}fun", value="Fun commands", inline=True)
    embed.add_field(name=f"{prefix}general", value="General commands", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def moderation(ctx):
    embed=discord.Embed(title="Moderation Menu", description=f"{desc}", color=0xff0000)
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.add_field(name=f"{prefix}ban", value=f"Bans mentioned user", inline=False)
    embed.add_field(name=f"{prefix}kick", value=f"Kicks mentioned user", inline=False)
    embed.add_field(name=f"{prefix}randomban", value=f"Bans a random person from the guild", inline=False)
    embed.add_field(name=f"{prefix}randomkick", value=f"Kicks a random person from the guild", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def fun(ctx):
    embed=discord.Embed(title="Fun Menu", description=f"{desc}", color=0xff0000)
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.add_field(name=f"{prefix}gay", value=f"Rates how gay you or a mentioned user is", inline=False)
    embed.add_field(name=f"{prefix}thot", value=f"Rates how much of a thot you or a mentioned user is", inline=False)
    embed.add_field(name=f"{prefix}8ball", value=f"Gives a random answer for your question", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def general(ctx):
    embed=discord.Embed(title="General Menu", description=f"{desc}", color=0xff0000)
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.add_field(name=f"{prefix}stats", value=f"Shows the version of the bot and Discord.py", inline=False)
    embed.add_field(name=f"{prefix}ping", value=f"Shows the ping", inline=False)
    await ctx.send(embed=embed)

bot.run(token)
