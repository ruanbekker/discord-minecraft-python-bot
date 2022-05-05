import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import random
import multiprocessing

# Variables
BOT_NAME = "MinecraftBot"
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

minecraft_server_url = "lightmc.fun" # this is just an example, and you should use your own minecraft server

bot_help_message = """
:: Bot Usage ::
`!mc help`                   : shows help
`!mc serverusage`   : shows system load in percentage
`!mc serverstatus` : shows if the server is online or offline
`!mc whoisonline`   : shows who is online at the moment
"""

available_commands = ['help', 'serverusage', 'serverstatus', 'whoisonline']

# Set the bot command prefix
bot = commands.Bot(command_prefix="!")

# Executes when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

# Executes whenever there is an incoming message event
@bot.event
async def on_message(message):
    print(f'Guild: {message.guild.name}, User: {message.author}, Message: {message.content}')
    if message.author == bot.user:
        return

    if message.content == '!mc':
        await message.channel.send(bot_help_message)

    if 'whosonline' in message.content:
        print(f'{message.author} used {message.content}')
    await bot.process_commands(message)

# Executes when the command mc is used and we trigger specific functions
# when specific arguments are caught in our if statements
@bot.command()
async def mc(ctx, arg):
    if arg == 'help':
        await ctx.send(bot_help_message)

    if arg == 'serverusage':
        cpu_count = multiprocessing.cpu_count()
        one, five, fifteen = os.getloadavg()
        load_percentage = int(five / cpu_count * 100)
        await ctx.send(f'Server load is at {load_percentage}%')

    if arg == 'serverstatus':
        response = requests.get(f'https://api.mcsrvstat.us/2/{minecraft_server_url}').json()
        server_status = response['online']
        if server_status == True:
            server_status = 'online'
        await ctx.send(f'Server is {server_status}')

    if arg == 'whoisonline':
        response = requests.get('https://api.mcsrvstat.us/2/{minecraft_server_url}').json()
        players_status = response['players']
        if players_status['online'] == 0:
            players_online_message = 'No one is online'
        if players_status['online'] == 1:
            players_online_username = players_status['list'][0]
            players_online_message = f'1 player is online: {players_online_username}'
        if players_status['online'] > 1:
            po = players_status['online']
            players_online_usernames = players_status['list']
            joined_usernames = ", ".join(players_online_usernames)
            players_online_message = f'{po} players are online: {joined_usernames}'
        await ctx.send(f'{players_online_message}')

bot.run(DISCORD_TOKEN)
