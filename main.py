import discord.ext.commands
import discord.ext.tasks
import discord
import datetime
import json
import scheduler.asyncio
import random
import logging
import asyncio

logging.basicConfig(format="%(asctime)s\t%(level)s:\t%(message)s", level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bonk_bot = discord.ext.commands.Bot(command_prefix="&", intents=intents)
bonk_channels: dict[discord.Guild, discord.TextChannel] = {}
sched = scheduler.asyncio.Scheduler(loop=asyncio.get_event_loop())
with open("config.json", "r") as config_file:
    config = json.load(config_file)


@discord.ext.tasks.loop(**{config["interval"]["unit"]: config["interval"]["quantity"]})
async def do_bonks():
    for channel in bonk_channels.values():
        await channel.send(f"{random.choice(channel.guild.members).mention} has been bonked!")


@bonk_bot.command()
async def setbonkchannel(ctx, *, channel: discord.TextChannel):
    bonk_channels[ctx.guild] = channel


@bonk_bot.event
async def on_ready():
    do_bonks.start()


bonk_bot.run(config["bot_token"])
