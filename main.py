from Parser import Parser
from data_model.History import History
import discord
import os
import datetime
from dotenv import load_dotenv
# load .env variables
load_dotenv()

from discord.ext import commands
from discord import Intents

intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

history = History()
failedCommandTumnail = "https://cdn.discordapp.com/emojis/831963313889476648.gif?v=1"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.nickname'):
        parser = Parser(message.content.split(".nickname")[1].strip())
        known_args, unkown_args = parser.parse()
        if known_args.username == [""]:
            await sendMessage(message, "You need to specify a user to check her/his past names", True, "No user specified error")
            return
        if len(unkown_args) > 0:
            await sendMessage(message, "Invalid argument(s): {}".format(unkown_args), True, "Command error")
            return
    if not known_args.name:
        await search_by_nicknames(message, known_args)
    else:
        await search_by_name(message, known_args)

async def search_by_nicknames(message, known_args):
    nicknames = get_all_nicknames()
    username = " ".join(known_args.username)
    if username not in nicknames:
        await sendMessage(message, "The nicknames {} does not exist in this guild".format(username), True, "This nicknames does not exist")
        return
    ids = nicknames[username]
    if len(ids) > 1:
        await sendMessage(message, "Multiple person have the same nickname on the server, try searching with there real name with the --name option".format(username), True, "Multiple person with same nickname")
        return
    await display_names(message, ids[0], known_args.max)

async def search_by_name(message, known_args):
    split_name = " ".join(known_args.username).split("#")
    name = split_name[0]
    if len(split_name) == 2:
        if len(split_name[1]) == 4:
            discriminator = split_name[1]
        else:
            discriminator = ""
    else:
        discriminator = ""
    if discriminator != "":
        member = discord.utils.get(client.get_all_members(), name=name, discriminator=discriminator)
    else:
        member = discord.utils.get(client.get_all_members(), name=name)
    if member is None:
        if discriminator != "":
            discriminator = "#" + discriminator
        await sendMessage(message, "The name {}{} is invalid".format(name, discriminator), True, "Invalid name")
        return
    await display_names(message, member.id, known_args.max)

@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        history.handle_new_name(after.guild.id, after.id, after.display_name, before.display_name)

async def sendMessage(message, messageToDisplay, error, title):
    embedVar = discord.Embed(title=title, description=messageToDisplay, color=0x00FF00)
    if error:
      embedVar.set_thumbnail(url = failedCommandTumnail)
      embedVar.__setattr__("color", 0xFF0000)
    await message.channel.send(embed=embedVar)

async def display_names(message, user_id, max):
    user = message.guild.get_member(user_id)
    if user.nick is None:
        current_name = user.name
    else:
        current_name = user.nick

    names = history.get_history(message.guild.id, user_id, current_name)
    message_to_display = ""
    count = 0
    for i in range(len(names) - 1, -1, -1):
        if count >= max:
            break
        time = ""
        if names[i].date is None:
            time += "Unknown"
        else:
            time += "first use on the {} of {} {} at {}:{}:{}".format(
                names[i].date["day"],
                datetime.datetime.strptime(str(names[i].date["month"]), "%m").strftime("%B"),
                names[i].date["year"],
                names[i].date["hour"],
                names[i].date["minute"],
                names[i].date["second"],
            )
        message_to_display += "{}) **{}**   *{}* \n\n".format(str(count + 1), names[i].name, time)
        count += 1
    await sendMessage(message, message_to_display, False, "{}#{}".format(user.name, user.discriminator))

def get_all_nicknames():
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

    return nicknames

client.run(os.getenv('TOKEN'))