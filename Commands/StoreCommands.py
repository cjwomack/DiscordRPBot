import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3
connection = sqlite3.connect("RPBot.db")

#adds an item to the store - admin only
@commands.command()
@commands.has_permissions(administrator=True)
async def storeadd(ctx,item, qty: int, cost: int, owner = None):
     cursor = connection.cursor()
     cursor.execute("insert into items (item, quantity, cost, owner) values (?, ?, ?, ?)", (item, qty, cost,'Store'))
     await ctx.send(f'Item was added to the store')
     connection.commit()

#Delete an Item from the store
@commands.command()
@commands.has_permissions(administrator=True)
async def deleteitem(ctx,item):
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT item, quantity, cost, owner FROM items WHERE owner = 'Store' and item = ?;", (str(item),),).fetchone()
     if not rows:
          await ctx.send("That item isn't in the store. Check your spelling or choose a valid item.")
     else:
          cursor.execute("DELETE from ITEMS where owner = 'Store' and item = ?;",(str(item),),)
          await ctx.send("Deleted {} from the store.".format(str(item)))
          connection.commit()

#Edit an item in the store
@commands.command()
@commands.has_permissions(administrator=True)
async def edititem(ctx,item, new_item, new_qty, new_cost):
    c = connection.cursor()
    cursor = connection.cursor()
    rows = cursor.execute("SELECT item, quantity, cost, owner FROM items WHERE owner = 'Store' and item = ?;", (str(item),),).fetchone()
    if not rows:
        await ctx.send("I can't find that item.  Check your spelling or choose an existing item.  View the current inventory with the !store command.")
    else:  #delete the original line and insert a new one with the new information.
        cursor.execute("DELETE from ITEMS where owner = 'Store' and item = ?;",(str(item),),)
        cursor.execute("insert into items (item, quantity, cost, owner) values (?, ?, ?, ?)", (str(new_item), str(new_qty), str(new_cost),'Store'))
        connection.commit()
        await ctx.send("The store has been updated.")


#view items in the store
@commands.command()
async def store(ctx):
     c = connection.cursor()
     target_store_name = 'Store'
     rows = c.execute("SELECT item, quantity, cost FROM items Where owner = ? ORDER BY item ASC;",(target_store_name,),).fetchall()
     embed = discord.Embed(colour = discord.Colour.purple())
     embed.set_author(name='See below for available inventory:')
     file = discord.File("Commands/Assets/store.png", filename="store.png")
     embed.set_thumbnail(url="attachment://store.png")
     if not rows:
          embed.add_field(name='No Items', value = 'I am all sold out!', inline = True)
          await ctx.send(file=file,embed=embed)
     else:
          for a, b, c in rows:
               embed.add_field(name='{}'.format(a), value = 'Qty: {}  Value: {}'.format(b,c), inline = False)
          await ctx.send(file=file,embed=embed)





def setup(client):
    # Every extension should have this function
    client.add_command(storeadd)
    client.add_command(deleteitem)
    client.add_command(edititem)
    client.add_command(store)
