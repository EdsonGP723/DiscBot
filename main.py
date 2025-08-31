import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, time, timedelta

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def send_daily_dm(user_id, message, target_time):
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now()
        send_time = datetime.combine(now.date(), target_time)
        if send_time < now:
            send_time += timedelta(days=1)
        wait_seconds = (send_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        try:
            user = await bot.fetch_user(user_id)
            await user.send(message)
        except Exception as e:
            print(f"Error sending DM: {e}")
        await asyncio.sleep(1)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    user_id = int(os.getenv("USER_ID"))
    mensaje = "Buenos díaaaassss preciosa hermosaaaa, TE AMOOOOOOOO."
    hora_objetivo = time(10, 00)
    bot.loop.create_task(send_daily_dm(user_id, mensaje, hora_objetivo))

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
