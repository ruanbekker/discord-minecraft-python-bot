import discord
import os
from dotenv import load_dotenv

BOT_NAME = "MinecraftBot"

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hello':
        await message.channel.send(f'Hey {message.author}')
    if message.content == 'goodbye':
        await message.channel.send(f'Goodbye {message.author}')

bot.run(DISCORD_TOKEN)
