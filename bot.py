import discord
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Import model handler
from model_handler import model_handler

# Basic bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

def should_respond(message):
    # Only respond when mentioned
    if message.author.bot:
        return False
    
    return bot.user.mentioned_in(message)

def clean_mention_content(content, bot_user):
    # Remove bot mention from message
    cleaned =  content

    for mention in [f'<@{bot_user.id}>', f'<@!{bot_user.id}>']:
        cleaned = cleaned.replace(mention, '').strip()

    return cleaned

async def load_model_async():
    try:
        await model_handler.load_model()
        await bot.change_presence(activity=discord.Game(name="ready to chat!"))
        print("Model loaded successfully")
    except Exception as e:
        print(f"Failed to load model: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="loading AI..."))

    asyncio.create_task(load_model_async())

@bot.event
async def on_message(message):
    if not should_respond(message):
        return

    user_input = clean_mention_content(message.content, bot.user)

    # React when no message with mention
    if not user_input.strip():
        await message.add_reaction('🤔')
        return

    # Show typing indicator
    async with message.channel.typing():
        # Generate AI response
        response = model_handler.generate_response(user_input)
        await message.reply(response, mention_author=False)
    

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not found in .env")
        exit(1)
    bot.run(TOKEN)