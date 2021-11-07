import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext


#Dice rolling function that supports multiple dice
@commands.command()
async def roll(ctx, arg: str, mult = "Empty"):

     if arg[0] == 'd':    #if the command starts with d[some numer]:
          x = arg
          dieroll = x[1:]
          rollresult = random.randint(1, int(dieroll))
          if mult[0] == "+":
               y = mult
               multiplier = y[1:]
               totalresult = rollresult + int(multiplier)
               user = ctx.author.name
               embed = discord.Embed(colour = discord.Colour.purple())
               embed.set_author(name='{} rolled the dice...'.format(user))
               file = discord.File("Commands/Assets/dice.png", filename="dice.png")
               embed.set_thumbnail(url="attachment://dice.png")
               embed.add_field(name='d{}'.format(dieroll), value = 'You rolled a {}. Roll of {} + {} modifier = {}.'.format(rollresult,rollresult, multiplier, totalresult), inline = False)
               await ctx.send(file=file,embed=embed)
          else:
               user = ctx.author.name
               embed = discord.Embed(colour = discord.Colour.purple())
               embed.set_author(name='{} rolled the dice...'.format(user))
               file = discord.File("Commands/Assets/dice.png", filename="dice.png")
               embed.set_thumbnail(url="attachment://dice.png")
               embed.add_field(name='d{}'.format(dieroll), value = 'You rolled a {}'.format(rollresult), inline = False)
               await ctx.send(file=file,embed=embed)
     else:     #if the command starts with a multiplier...
          user = ctx.author.name
          embed = discord.Embed(colour = discord.Colour.purple())
          embed.set_author(name='{} rolled the dice...'.format(user))
          file = discord.File("Commands/Assets/dice.png", filename="dice.png")
          embed.set_thumbnail(url="attachment://dice.png")
          x = arg
          multiplier = int(x[0])
          dieroll = x[2:]
          rolltotals = 0
          for i in range(multiplier):
               rollresult = random.randint(1,int(dieroll))
               #check if there is a multiplier and add it to the roll, otherwise just print the roll.
               if mult[0] == "+":
                   y = mult
                   multiplier = y[1:]
                   totalresult = rollresult + int(multiplier)
                   embed.add_field(name='d{}'.format(dieroll), value = 'You rolled a {}. Roll of {} + {} modifier = {}.'.format(rollresult,rollresult, multiplier, totalresult), inline = False)
               else:
                   embed.add_field(name='Roll #{} - d{}'.format(i+1, dieroll), value = 'You rolled a {}'.format(rollresult), inline = False)
          await ctx.send(file=file,embed=embed)



def setup(client):
    # Every extension should have this function
    client.add_command(roll)
