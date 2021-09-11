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
failedCommandTumnail = "https://media.giphy.com/media/3og0IvGtnDyPHCRaYU/giphy.gif"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.name'):
        parser = Parser(message.content.split(".name")[1].strip())
        known_args, unkown_args = parser.parse()
        if known_args.username == [""]:
            await sendMessage(message, "You need to specify a user to check her/his past names", True, "No user specified error")
            return
        if len(unkown_args) > 0:
            await sendMessage(message, "Invalid argument(s): {}".format(unkown_args), True, "Command error")
            return
        nicknames = {}
        for member in client.get_all_members():
            name_to_add = ""
            if member.nick is None:
                name_to_add = member.name
            else:
                name_to_add = member.nick
            if name_to_add in nicknames:
                nicknames[name_to_add].append(member.id)
            else:
                nicknames[name_to_add] = [member.id]
        print(nicknames)


@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        history.handle_new_name(after.guild.id, after.id, after.display_name)

async def sendMessage(message, messageToDisplay, error, title):
    embedVar = discord.Embed(title=title, description=messageToDisplay, color=0x00FF00)
    if error:
      embedVar.set_thumbnail(url = failedCommandTumnail)
      embedVar.__setattr__("color", 0xFF0000)
    await message.channel.send(embed=embedVar)

client.run(os.getenv('TOKEN'))