import os

import discord
from discord import Intents
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = Intents.all()

def post_alert(message):
    
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():

        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(f'{client.user} is connected to the following guild:\n'f'{guild.name}(id:{guild.id})')

        maintenance_channel = client.get_channel(978438215348420658)
        await maintenance_channel.send(message)
        
        print("sent")
        
        await client.close()
        
    client.run(TOKEN)
    
#post_alert("testing troubleshot code on RPi")
