import discord
import os
from dotenv import load_dotenv

load_dotenv()

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

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am your Discord bot.')

    user_input = clean_mention_content(message.content, bot.user)

    # React when no message with mention
    if not user_input.strip():
        await message.add_reaction('🤔')
        return

    # Simple echo for testing
    await message.reply(f"You said: {user_input}", mention_author=False)
    

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not found in .env")
        exit(1)
    bot.run(TOKEN)