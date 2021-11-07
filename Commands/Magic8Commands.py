import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext

#Magic 8 Ball admin functions are below.....
#Add new options to magic8ball.txt
@commands.command()
@commands.has_permissions(administrator=True)
async def addmagic8(ctx, *, arg):
     with open('DiscordRPBot/magic8ball.txt', 'a') as ball_file:
          ball_file.write(str(arg)+'\n')
          await ctx.send(f'I updated the Magic 8 Ball responses')

#returns all of the available magic 8 ball commands, with index number to use for deletion
@commands.command()
@commands.has_permissions(administrator=True)
async def viewmagic8(ctx):
    file1 = open('DiscordRPBot/magic8ball.txt', 'r')
    Lines = file1.readlines()
    count = 0
    for line in Lines:
        count += 1
        await ctx.send("Index {}: {}".format(count, line.strip()))

#Deletes the line specified from magic8ball.txt
@commands.command()
@commands.has_permissions(administrator=True)
async def deletemagic8(ctx, index):
    with open("DiscordRPBot/magic8ball.txt", "r+") as f:
        lines = f.readlines()
        del lines[int(index)-1]
        f.seek(0)
        f.truncate()
        f.writelines(lines)
        new_index = int(index)-1
        await ctx.send("Deleted.")

#Provides a magic 8 ball response
@commands.command()
async def magic8(ctx):
     responses = open('DiscordRPBot/magic8ball.txt').read().splitlines()
     random.seed(a=None)
     response =random.choice(responses)
     user = ctx.author.name
     embed = discord.Embed(colour = discord.Colour.purple())
     embed.set_author(name='{} shook the Magic 8 Ball...'.format(user))
     file = discord.File("Commands/Assets/magic8.png", filename="magic8.png")
     embed.set_thumbnail(url="attachment://magic8.png")
     embed.add_field(name='Magic 8 Ball', value = '{}'.format(response), inline = False)
     await ctx.send(file=file,embed=embed)

def setup(client):
    # Every extension should have this function
    client.add_command(addmagic8)
    client.add_command(viewmagic8)
    client.add_command(deletemagic8)
    client.add_command(magic8)
