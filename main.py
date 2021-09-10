from Parser import Parser
from data_model.History import History
import discord
import os
from dotenv import load_dotenv
# load .env variables
load_dotenv()

from discord.ext import commands
from discord import Intents

intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

history = History()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.name'):
        parser = Parser()
        args = message.content.split(".name")[1].strip().split(" ")
        valid_args, unknown_args = parser.parse(args)
        print(valid_args)
        print(unknown_args)

@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        history.handle_new_name(after.guild.id, after.id, after.display_name)

client.run(os.getenv('TOKEN'))