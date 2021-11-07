import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3
connection = sqlite3.connect("RPBot.db")

#Exits the program if you want the Bot to go away
@commands.command()
@commands.has_permissions(administrator=True)
async def goaway(ctx):
     await ctx.send(f'Bye, Everybody!')
     sys.exit()


#Server Stats
@commands.command()
async def server(ctx):
     cursor = connection.cursor()

     cash = cursor.execute("Select variable FROM globalvariables WHERE purpose = 'cashtoggle'").fetchone()
     maximumcash = cursor.execute("Select variable FROM globalvariables WHERE purpose = 'maxcash'").fetchone()
     taxsetting = cursor.execute("Select variable FROM globalvariables WHERE purpose = 'taxes'").fetchone()
     paymentsetting = cursor.execute("Select variable FROM globalvariables WHERE purpose = 'payment'").fetchone()

     embed = discord.Embed(colour = discord.Colour.purple())
     file = discord.File("Commands/Assets/server.png", filename="server.png")
     embed.set_thumbnail(url="attachment://server.png")
     embed.set_author(name='Server Statistics:')
     embed.add_field(name="Users:", value=ctx.guild.member_count, inline=False)
     embed.add_field(name='Text Channels:', value = len(ctx.guild.text_channels), inline=False)
     embed.add_field(name='Voice Channels:', value = len(ctx.guild.voice_channels), inline=False)
     embed.add_field(name='!givemoney Command:', value = str(cash[0]), inline=False)
     embed.add_field(name='Maximum Cash:', value = str(maximumcash[0]), inline=False)
     embed.add_field(name='Tax Amount:', value = str(taxsetting[0]), inline=False)
     embed.add_field(name='Participation Payment Amount:', value = str(paymentsetting[0]), inline=False)
     await ctx.send(file=file,embed=embed)



def setup(client):
    # Every extension should have this function
    client.add_command(server)
    client.add_command(goaway)
