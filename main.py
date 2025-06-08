import discord
import asyncio
import aiohttp
import json
import string
import random
from discord.ext import commands
import os

with open("settings.json") as f:
    settings = json.load(f)

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())

# Dictionary to keep track of running tasks in each channel
running_tasks = {}

async def check_user(username):
    async with aiohttp.ClientSession() as session:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
            'Client-Session-Id': 'cab427f35656d6c4',
            'Client-Version': '121dfb28-b6c3-48e2-8a3b-588128a7fae5',
            'Connection': 'keep-alive',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://www.twitch.tv',
            'Referer': 'https://www.twitch.tv/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = '{"operationName":"UsernameValidator_User","variables":{"username":"' + username + '"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660"}}}'
        async with session.post('https://gql.twitch.tv/gql', headers=headers, data=data) as response:
            r = await response.json()
            r1 = r["data"]["isUsernameAvailable"]
            return r1, username

def generate_random_username(length, option):
    if option == 1:
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    elif option == 2:
        return ''.join(random.choices(string.digits, k=length))
    elif option == 3:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

async def run_option(ctx, option, length):
    while True:
        if ctx.channel.id not in running_tasks:
            running_tasks[ctx.channel.id] = asyncio.current_task()
        username = generate_random_username(length, option)
        r1 = await check_user(username)
        if r1[0] == True:
            await ctx.send(f'Username **{username}** **available**.')
            # Perform actions for the available username
        else:
            await ctx.send(f'Username **{username}** not available.')
        await asyncio.sleep(1)  # Adjust sleep time as per your requirement

def is_admin_or_owner():
    async def predicate(ctx):
        if ctx.guild is not None and (ctx.author.guild_permissions.administrator or ctx.author == ctx.guild.owner):
            return True
        else:
            owner = ctx.guild.owner.mention if ctx.guild is not None else 'server owner'
            await ctx.send(f"This command can only be used by the server owner ({owner}) or users with administrator permissions but if you would want this bot for your server you can add it by clicking here [add bot](https://discord.com/api/oauth2/authorize?client_id=1142305796785438750&permissions=8&scope=applications.commands%20bot) {ctx.author.mention}.")
            return False
    return commands.check(predicate)

@bot.command()
@is_admin_or_owner()
async def option1(ctx, length: int):
    """
    Generates usernames with only ASCII lowercase letters.

    Parameters:
    - length: Length of the usernames to generate.

    Example Usage:
    ",option1 8"
    This command will continuously generate usernames of whatever length chosen consisting of only ASCII lowercase letters until stopped manually.
    """
    await run_option(ctx, 1, length)

@bot.command()
@is_admin_or_owner()
async def option2(ctx, length: int):
    """
    Generates usernames with only digits.

    Parameters:
    - length: Length of the usernames to generate.

    Example Usage:
    ",option2 6"
    This command will continuously generate usernames of whatever length chosen consisting of only digits until stopped manually.
    """
    await run_option(ctx, 2, length)

@bot.command()
@is_admin_or_owner()
async def option3(ctx, length: int):
    """
    Generates usernames with ASCII lowercase letters and digits.

    Parameters:
    - length: Length of the usernames to generate.

    Example Usage:
    ",option3 8"
    This command will continuously generate usernames of whatever length chosen consisting of ASCII lowercase letters and digits until stopped manually.
    """
    await run_option(ctx, 3, length)

@bot.command()
@is_admin_or_owner()
async def stop(ctx):
    """
    Stops the currently running task in the channel.
    """
    if ctx.channel.id in running_tasks:
        channel = bot.get_channel(ctx.channel.id)
        await channel.send(f"Command stopped in {channel.mention} by {ctx.author.mention}")
        task = running_tasks[ctx.channel.id]
        task.cancel()
        del running_tasks[ctx.channel.id]
    else:
        await ctx.send("No task is running in this channel.")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def cmds(ctx):
    commands_list = "\n".join([f"{command.name}: {command.help}" for command in bot.commands])
    await ctx.send(f"blend in\n```{commands_list}```")

token = os.environ['token']
bot.run(token)












