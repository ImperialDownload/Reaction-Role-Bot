import discord
from discord.ext import commands, tasks
import csv

client = commands.Bot(command_prefix = 'rr*')
with open('message.txt') as f:
    rrmessage = int(f.read())

#Bot startup routines
@client.event
async def on_ready():
    print('Bot is ready.')

#Reaction Roles
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == rrmessage:
        await handle_reaction(payload, True)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == rrmessage:
        await handle_reaction(payload, False)

async def handle_reaction(payload, action):
    with open('rroles.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if str(payload.emoji.name) == line['reaction']:
                guild = client.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(int(line['role']))
                if action:
                    await user.add_roles(role)
                else:
                    await user.remove_roles(role)

#Bot start up
with open('token.txt') as f:
    client.token = f.read()
client.run(client.token)
