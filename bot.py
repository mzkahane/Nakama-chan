import discord
import os
from dotenv import load_dotenv

load_dotenv()

# Basic bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Discord bot.')

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not found in .env")
        exit(1)
    bot.run(TOKEN)