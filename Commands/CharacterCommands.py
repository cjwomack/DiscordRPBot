import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3
connection = sqlite3.connect("RPBot.db")

#creates the character initially, writes to the DB character table, and logs the name as the users.  Kicks off the messages to further edit.
@commands.command()
async def create(ctx,*, arg):
     username = ctx.author.name
     c = connection.cursor()
     rows = c.execute("SELECT name FROM character Where user = ?",(str(username),),).fetchall()
     if not rows:
          cursor = connection.cursor()
          cursor.execute("INSERT into character (name, user) values (?, ?);", (str(arg), str(username)))
          await ctx.send('Created Character.  To continue creating your character, enter !createstats [str] [dex] [con] [int] [will] [char] [health] [mana], eg: !createstats 2 3 4 4 3 2 10 10')
          connection.commit()
     else:
          for a in rows:
               await ctx.send('WARNING: You already have a character named {}.  You should edit your character instead of creating a new one.  Use !createstats and !createinfo to overwrite the character stats'.format(a))


#adds the stats of the character to the character
@commands.command()
async def createstats(ctx, strength, dexterity, constitution, integrity, will, charisma, health, mana):
     username = ctx.author.name
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET str = ?, dex = ?, con = ?, int = ?, will = ?, char = ?, health = ?, mana = ? WHERE user = ?;", (strength, dexterity, constitution, integrity, will, charisma, health, mana, str(username)))
     await ctx.send('Character stats updated.  To continue, enter !createinfo [age] [height] [weight] [race] [class], eg !createinfo 94 1m 199 dwarf mage')
     connection.commit()


#Add info the character
@commands.command()
async def createinfo(ctx, age:str, height:str, weight: str, race:str, class_1: str):
     username = ctx.author.name
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character SET age = ?, height = ?, weight = ?, race = ?, class = ? WHERE user = ?;", (age, height, weight, race, class_1, str(username)))
     await ctx.send('Character info has been updated.  To include a photo, use !addphoto [url of image].  Or, use !stats to view your character stats.')
     connection.commit()

#Add a photo url to the character
@commands.command()
async def addphoto(ctx, arg):
     username = ctx.author.name
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character SET url = ? WHERE user = ?", (arg, str(username)))
     await ctx.send('Photo has been added to character info.  use !stats to see your character sheet.')
     connection.commit()


#Shows the character stats on a single view
@commands.command(pass_context = True)
async def stats(ctx,user = None):
     hasPermiss = True
     if user == None:
          username = ctx.author.name
     else:
         if ctx.message.author.guild_permissions.administrator:
             person = user
             username = person
         else:
             await ctx.send("Keep your eyes to yourself, snoop!")
             hasPermiss = False
     if hasPermiss == True:
         c = connection.cursor()
         cursor = connection.cursor()
         rows = cursor.execute("SELECT name, age, height, weight, race, class, str, dex, con, int, will, char, health, mana, url FROM character WHERE user = ?;",(str(username),),).fetchall()
         equip_rows = cursor.execute("SELECT item, user FROM equipment WHERE user = ?",(str(username),),).fetchall()
         embed = discord.Embed(colour = discord.Colour.purple())
         if not rows:
              await ctx.send('This user has no character stats.')

         else:
              for a, b, c, d, e, f, g, h, i, j, k, l, m , n, o in rows:
                   if not o:
                        embed.set_author(name='STATS')
                        embed.add_field(name='Name', value = '{}'.format(a), inline = True)
                        embed.add_field(name='Age', value = '{}'.format(b), inline = True)
                        embed.add_field(name='Height', value = '{}'.format(c),inline = True)
                        embed.add_field(name='Weight', value = '{}'.format(d),inline = True)
                        embed.add_field(name='Race', value = '{}'.format(e),inline = True)
                        embed.add_field(name='Class', value = '{}'.format(f),inline = True)
                        embed.add_field(name='Str', value = '{}'.format(g),inline = True)
                        embed.add_field(name='Dex', value = '{}'.format(h),inline = True)
                        embed.add_field(name='Con', value = '{}'.format(i),inline = True)
                        embed.add_field(name='Int', value = '{}'.format(j),inline = True)
                        embed.add_field(name='Will', value = '{}'.format(k),inline = True)
                        embed.add_field(name='Char', value = '{}'.format(l),inline = True)
                        embed.add_field(name='Health', value = '{}'.format(m),inline = True)
                        embed.add_field(name='Mana', value = '{}'.format(n),inline = True)

                   else:
                        embed.set_thumbnail(url= "{}".format(o))
                        embed.set_author(name='STATS')
                        embed.add_field(name='Name', value = '{}'.format(a), inline = True)
                        embed.add_field(name='Age', value = '{}'.format(b), inline = True)
                        embed.add_field(name='Height', value = '{}'.format(c),inline = True)
                        embed.add_field(name='Weight', value = '{}'.format(d),inline = True)
                        embed.add_field(name='Race', value = '{}'.format(e),inline = True)
                        embed.add_field(name='Class', value = '{}'.format(f),inline = True)
                        embed.add_field(name='Str', value = '{}'.format(g),inline = True)
                        embed.add_field(name='Dex', value = '{}'.format(h),inline = True)
                        embed.add_field(name='Con', value = '{}'.format(i),inline = True)
                        embed.add_field(name='Int', value = '{}'.format(j),inline = True)
                        embed.add_field(name='Will', value = '{}'.format(k),inline = True)
                        embed.add_field(name='Char', value = '{}'.format(l),inline = True)
                        embed.add_field(name='Health', value = '{}'.format(m),inline = True)
                        embed.add_field(name='Mana', value = '{}'.format(n),inline = True)

              await ctx.send(embed=embed)
              if equip_rows:
                  equip = discord.Embed(colour = discord.Colour.green())
                  for a in equip_rows:
                      equip.set_author(name='EQUIPPED ITEMS')
                      equip.add_field(name='{}'.format(a[0]), value = ':small_blue_diamond:', inline = False)
                  await ctx.send(embed=equip)

#edit the character name
@commands.command()
async def editname(ctx,old_name: str, new_name: str):
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT name FROM character WHERE name = ?;",(str(old_name),),).fetchall()
     if not rows:
          await ctx.send('I did not find a character by that name.  Try again with a valid name')
     else:
          cursor.execute("UPDATE character  SET name = ? WHERE name = ?;", (str(new_name), str(old_name)))
          await ctx.send('Character {} has been updated to {}'.format(old_name, new_name))
          connection.commit()

#Update strength
@commands.command()
@commands.has_permissions(administrator=True)
async def strength(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET str = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Str value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update dexterity
@commands.command()
@commands.has_permissions(administrator=True)
async def dexterity(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET dex = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Dex value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update constitution
@commands.command()
@commands.has_permissions(administrator=True)
async def constitution(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET con = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Con value has been changed to {} for {}'.format(arg, user))
     connection.commit()


#Update intuition
@commands.command()
@commands.has_permissions(administrator=True)
async def intelligence(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET int = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Int value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update constitution
@commands.command()
@commands.has_permissions(administrator=True)
async def willpower(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET will = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('will value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update constitution
@commands.command()
@commands.has_permissions(administrator=True)
async def charisma(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET char = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Char value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update constitution
@commands.command()
@commands.has_permissions(administrator=True)
async def health(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET health = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Health value has been changed to {} for {}'.format(arg, user))
     connection.commit()

#Update constitution
@commands.command()
@commands.has_permissions(administrator=True)
async def mana(ctx, user, arg):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     cursor.execute("UPDATE character  SET mana = ? WHERE user = ?;", (str(arg),str(username)))
     await ctx.send('Mana value has been changed to {} for {}'.format(arg, user))
     connection.commit()

def setup(client):
    # Every extension should have this function
    client.add_command(mana)
    client.add_command(health)
    client.add_command(charisma)
    client.add_command(willpower)
    client.add_command(intelligence)
    client.add_command(constitution)
    client.add_command(dexterity)
    client.add_command(strength)
    client.add_command(editname)
    client.add_command(stats)
    client.add_command(addphoto)
    client.add_command(createinfo)
    client.add_command(createstats)
    client.add_command(create)
