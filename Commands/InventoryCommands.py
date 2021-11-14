import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3
connection = sqlite3.connect("RPBot.db")

#Open your inventory or someone elses
@commands.command(pass_context = True)
async def inventory(ctx, type = 'u', user = None):
     hasPermiss = True
     if type == 'u':
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
              rows = cursor.execute("SELECT item, quantity, cost FROM items WHERE owner = ? ORDER BY item ASC;",(str(username),),).fetchall()
              embed = discord.Embed(colour = discord.Colour.purple())
              file = discord.File("Commands/Assets/backpack.png", filename="backpack.png")
              embed.set_thumbnail(url="attachment://backpack.png")
              for a, b, c in rows:
                   embed.set_author(name='INVENTORY: {}'.format(username))
                   embed.add_field(name='{}'.format(a), value = 'Qty: {}  Value: {}'.format(b,c), inline = False)
              await ctx.send(file=file,embed=embed)
     if type = 'c':
           if hasPermiss == True:
              c = connection.cursor()
              cursor = connection.cursor()
              rows = cursor.execute("SELECT item, quantity, cost FROM items AS I INNER JOIN character AS C WHERE I.owner = C.user AND I.owner =  ? ORDER BY item ASC;",(str(username),),).fetchall()
              embed = discord.Embed(colour = discord.Colour.purple())
              file = discord.File("Commands/Assets/backpack.png", filename="backpack.png")
              embed.set_thumbnail(url="attachment://backpack.png")
              for a, b, c in rows:
                   embed.set_author(name='INVENTORY: {}'.format(username))
                   embed.add_field(name='{}'.format(a), value = 'Qty: {}  Value: {}'.format(b,c), inline = False)
              await ctx.send(file=file,embed=embed)

#Use an item from your inventory
@commands.command()
async def use(ctx,item, qty = "1"):
     username = ctx.author.name
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT quantity, cost, owner FROM items WHERE owner = ? AND item = ?;", (str(username), str(item)),).fetchone()
     if not rows:  #did not find that item
          await ctx.send('You dont have that item to use.  Check your spelling, or choose a new item.')
     else:
         qty_to_use = int(rows[0]) - int(qty)
         if (qty_to_use < 0):  #if the quantity you're trying to use is greater than the quantity you have...
             await ctx.send("You don't have that many.  Choose a quantity of {} or less.".format(str(rows[0])))
         else:  #otherwise, deduct the number used from your inventory
             new_qty = int(rows[0]) - int(qty)
             if (new_qty == 0):  #if there's none left, delete the line from the user.
                    cursor.execute("DELETE from ITEMS where owner = ? and item = ?;",(str(username), str(item),),)
                    await ctx.send("You used {} {}.  You have none left.".format(str(qty), str(item)))
                    connection.commit()
             else:
                    cursor.execute("UPDATE items SET quantity = ? WHERE owner = ? AND item = ?;", (str(new_qty), str(username), str(item)))
                    await ctx.send("You used {} {}.".format(str(qty), str(item)))
                    connection.commit()


#Donate to the Treasury
@commands.command()
async def donate(ctx,amt: int):
    username = ctx.author.name
    c=connection.cursor()
    cursor = connection.cursor()
    target_treasury_name = "Treasury"
    rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(str(username),),).fetchone()
    treasury = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(target_treasury_name,),).fetchone()
    if not rows:
        await ctx.send("I didn't find a balance for you.  Make sure you have a balance.")
    else:
        have_enough = int(rows[0]) - int(amt)
        short = abs(have_enough)
        if (have_enough < 0):
            await ctx.send("You're  short {} coins to donate.  You can only donate {} coins".format(str(short), rows[0]))
        else:
            new_balance = int(rows[0]) - int(amt)
            if not treasury:
                cursor.execute("INSERT into wallet (balance, user) values (?,?);", (str(amt), target_treasury_name))
                cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_balance), str(username)))
                connection.commit()
                await ctx.send("You donated {} coins.".format(str(amt)))
            else:
                new_treasury_balance = int(treasury[0]) + int(amt)
                cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_treasury_balance), target_treasury_name))
                cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_balance), str(username)))
                connection.commit()
                await ctx.send("You donated {} coins.".format(str(amt)))


#equip an item from your inventory.
@commands.command()
async def equip(ctx, item):
     cursor = connection.cursor()
     username = ctx.author.name
     #rows = cursor.execute("SELECT item FROM equipment WHERE user = ?;", (str(username),),).fetchone()
     inv = cursor.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?;", (str(username),str(item),),).fetchone()
     if not inv:  #if you don't have it in inventory
         await ctx.send("You don't have that item to equip.")
     else: #if you do have it in INVENTORY
         item_count = (int(inv[0]) - 1)
         cursor.execute("INSERT into equipment (item, user, cost) values (?,?,?);", (str(item), str(username),str(inv[1])))
         connection.commit()
         if item_count > 0:  #If there are more than 1 of this item, remove only one from the inventory, otherwise remove all of it
             cursor.execute("UPDATE items SET quantity = ? WHERE owner = ? AND item = ?;", (str(item_count), str(username), str(item)))
             connection.commit()
         else:  # there aren't any left, so remove the item from the INVENTORY
             cursor.execute("DELETE from ITEMS where owner = ? and item = ?;",(str(username), str(item),),)
             connection.commit()

         await ctx.send("You equipped {}".format(str(item)))

#unequip the item and put it back into INVENTORY
@commands.command()
async def unequip(ctx, item):
     cursor = connection.cursor()
     username = ctx.author.name
     rows = cursor.execute("SELECT item, user, cost FROM equipment WHERE item =? and user = ?;", (str(item),str(username),),).fetchone()
     inv = cursor.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?;", (str(username),str(item),),).fetchone()
     if not rows:
         await ctx.send("You don't have that item equipped.")
     else:  #delete the item from equipment and add it to INVENTORY
         if not inv:  #you don't have any of that in your inventory, so insert 1
            new_qty = 1
            cursor.execute("INSERT into items (item, owner, quantity, cost) values (?,?,?,?);", (str(item), str(username), str(new_qty), str(rows[2])))
            connection.commit()
         else:
            item_count = int(inv[0]) + 1
            cursor.execute("UPDATE items SET quantity = ? WHERE owner = ? AND item = ?;", (str(item_count), str(username), str(item)))
            connection.commit()
     cursor.execute("DELETE from equipment where user = ? and item = ?;",(str(username), str(item),),)
     connection.commit()
     await ctx.send("Unequipped {}".format(str(item)))

#Give an item to a user
@commands.command()
@commands.has_permissions(administrator=True)
async def giveitem(ctx, user, item, qty, cost):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     #if doesn't have the item, make a new line.  If they have some, add more to the qty
     rows = cursor.execute("SELECT quantity, cost, owner FROM items WHERE owner = ? AND item = ?;", (str(username), str(item)),).fetchall()
     if not rows:
          cursor.execute("INSERT into items (item, quantity, cost, owner) values (?, ?, ?, ?)", (item, qty, cost,str(username)))
          await ctx.send('You gave {} {} {}'.format(user, qty, item))
          connection.commit()
     else:      #There's a match - add the quantity to the existing quantity
          for a, b, c in rows:
               new_qty = int(a) + int(qty)
               cursor.execute("UPDATE items SET quantity = ? WHERE owner = ? and item = ?;", (str(new_qty), str(username), str(item)))
               await ctx.send("{} already has some of that - quantity has been updated to {}".format(user, str(new_qty)))
               connection.commit()
     connection.commit()


#Check your balance in your wallet
@commands.command()
async def wallet(ctx, user = None):
     if user == None:
          username = ctx.author.name
     else:
          person = user
          username = person
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(str(username),),).fetchone()
     embed = discord.Embed(colour = discord.Colour.purple())
     file = discord.File("Commands/Assets/wallet.png", filename="wallet.png")
     embed.set_thumbnail(url="attachment://wallet.png")
     embed.set_author(name='Wallet: {}'.format(username))
     embed.add_field(name='Current Balance: ', value = '{}'.format(rows[0]), inline = True)
     await ctx.send(file=file,embed=embed)

#Get the full list of users and their money
@commands.command()
@commands.has_permissions(administrator=True)
async def bank(ctx):
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT user, Balance FROM wallet").fetchall()
     embed = discord.Embed(colour = discord.Colour.purple())
     file = discord.File("Commands/Assets/bank.png", filename="bank.png")
     embed.set_thumbnail(url="attachment://bank.png")
     if not rows:
          await ctx.send('hmm...Banks empty.')
     else:
          for a,b in rows:
              embed.set_author(name='BANK')
              embed.add_field(name='{}'.format(a), value = 'Balance: {}'.format(b), inline = False)
     await ctx.send(file=file,embed=embed)

#give another player money and subtract from own funds
@commands.command()
async def givemoney(ctx,user,amt):
     giver = ctx.author.name
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(str(giver),),).fetchone()
     recipient_rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(str(person),),).fetchone()
     toggle_value = cursor.execute("SELECT variable FROM globalvariables WHERE purpose = 'cashtoggle'").fetchone()
     status = str(toggle_value[0])
     if not recipient_rows:
         await ctx.send("That isn't a real person!  Check your spelling and try again.")
     else:
         if (status == "On"):
             for a in rows:
                  if int(rows[0]) < int(amt):
                       await ctx.send('You dont have that much money to give away.')
                  else:
                       new_balance = int(rows[0]) - int(amt)
                       cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_balance), str(giver)))
                       await ctx.send("you gave {} {} coins.  Updated balance is {} coins.".format(user,str(amt), str(new_balance)))
                       connection.commit()
                       givenrows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(str(username),),).fetchone()
                       for b in givenrows:
                            updated_balance = int(givenrows[0]) + int(amt)
                            cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(updated_balance), str(username)))
                            await ctx.send('{} has a new wallet balance of: {} coins.'.format(str(username),str(updated_balance)))
                            connection.commit()
             connection.commit()
         else:
             await ctx.send('The admin has turned this function off.')

#buy stuff from the store - change inventory qty and store qty.  Deduct wallet amount.
@commands.command()
async def buy(ctx, item, qty = "1"):
     username = ctx.author.name
     c = connection.cursor()
     target_store_name = 'Store'
     rows = c.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?",(target_store_name,str(item),),).fetchone()  #Store item lookup
     user_rows = c.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?", (str(username), str(item),),).fetchone()  #User item lookup
     user_wallet = c.execute("SELECT balance FROM wallet WHERE user = ?;",(str(username),),).fetchone()  #User wallet lookup
     store_wallet = c.execute("SELECT balance FROM wallet WHERE user = ?;",(target_store_name,),).fetchone()
     new_user_balance = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
     if not rows:
          await ctx.send('The store doesnt have that item.  Check your spelling, or choose a new item.')
     else:
          new_store_qty = int(rows[0]) - int(qty)
          if (int(new_user_balance) < 0):
              await ctx.send("You don't have enough money to buy that.")
          elif new_store_qty < 0:   #if there aren't enough
               await ctx.send('The store doesnt have that many.  Choose a quantity equal to or less than the Stores quantity.')
          elif new_store_qty == 0: #delete the item from the DB if there are none left.
               c.execute("DELETE FROM items WHERE item = ? and owner = ?;",(str(item),target_store_name,),)
               await ctx.send('That was the last of that item in the store - it is now out of stock')
               connection.commit()
               if not user_rows: #add the item to the inventory with the qty argument
                    c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(rows[1]), str(username)))
                    updated_user_wallet = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
                    update_store_wallet = (int(store_wallet[0]) + (int(rows[1]) * int(qty)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                    await ctx.send('{} has purchased {} {}'.format(str(username), str(qty), str(item)))
                    connection.commit()
               else:
                    new_user_qty = int(user_rows[0]) + int(qty)
                    c.execute("UPDATE items SET quantity = ?, cost = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(user_rows[1]), str(username), str(item)))
                    updated_user_wallet = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
                    update_store_wallet = (int(store_wallet[0]) + (int(rows[1]) * int(qty)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                    await ctx.send('{} has purchased {} {}'.format(str(username), str(qty), str(item)))
                    connection.commit()
          else:
               c.execute("UPDATE items SET quantity = ? WHERE item = ? and owner = ?;", (str(new_store_qty),str(item), target_store_name))
               updated_user_wallet = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
               update_store_wallet = (int(store_wallet[0]) + (int(rows[1]) * int(qty)))
               c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
               c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
               connection.commit()
               if not user_rows: #add the item to the inventory with the qty argument
                    c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(rows[1]), str(username)))
                    updated_user_wallet = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
                    update_store_wallet = (int(store_wallet[0]) + (int(rows[1]) * int(qty)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                    await ctx.send('{} has purchased {} {}'.format(str(username), str(qty), str(item)))
                    connection.commit()
               else:
                    new_user_qty = int(user_rows[0]) + int(qty)
                    c.execute("UPDATE items SET quantity = ?, cost = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(user_rows[1]), str(username), str(item)))
                    updated_user_wallet = (int(user_wallet[0]) - (int(rows[1]) * int(qty)))
                    update_store_wallet = (int(store_wallet[0]) + (int(rows[1]) * int(qty)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                    c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                    await ctx.send('{} has purchased {} {}'.format(str(username), str(qty), str(item)))
                    connection.commit()


#sell an item to the store
@commands.command()
async def sell(ctx, item, qty = "1"):
     username = ctx.author.name
     c = connection.cursor()
     target_store_name = 'Store'
     rows = c.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?",(target_store_name,str(item),),).fetchone()  #Store item lookup
     user_rows = c.execute("SELECT quantity, cost FROM items WHERE owner = ? AND item = ?", (str(username), str(item),),).fetchone()  #User item lookup
     user_wallet = c.execute("SELECT balance FROM wallet WHERE user = ?;",(str(username),),).fetchone()  #User wallet lookup
     store_wallet = c.execute("SELECT balance FROM wallet WHERE user = ?;",(target_store_name,),).fetchone() #Store wallet lookup
     new_store_balance = int(store_wallet[0]) - (int(qty) * int(user_rows[1]))
     if not store_wallet:
         await ctx.send("The store doesn't have any money to buy that.")
     elif (new_store_balance < 0):
         await ctx.send("The store doesn't have enough money.  Reduce the qty, or trade with another person.")
     else:
         if store_wallet:
             new_store_balance = int(store_wallet[0]) - (int(qty) * int(user_rows[1]))
         if not user_rows:  #did not find that item
              await ctx.send('You dont have that item.  Check your spelling, or choose a new item.')
         else:
              new_user_qty = int(user_rows[0]) - int(qty)
              if new_user_qty < 0:  #You dont have enough of that item
                   await ctx.send("You don't have enough of that item.  Choose {} or fewer.".format(str(user_rows[0])))
              elif new_user_qty == 0:  #need to delete the item from the user inventory - they have none left after selling
                   c.execute("DELETE FROM items WHERE item = ? and owner = ?;",(str(item),str(username),),)
                   connection.commit()
                   if not rows: #add the item to the store with the qty argument
                        c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(user_rows[1]), target_store_name))
                        updated_user_wallet = (int(user_wallet[0]) + (int(user_rows[1]) * int(qty)))
                        update_store_wallet = (int(store_wallet[0]) - (int(user_rows[1]) * int(qty)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                        await ctx.send('{} has sold {} {}'.format(str(username), str(qty), str(item)))
                        connection.commit()
                   else: #the item is already in the store and needs the qty updated
                        new_user_qty = int(user_rows[0]) - int(qty)
                        c.execute("UPDATE items SET quantity = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(username), str(item)))
                        updated_user_wallet = (int(user_wallet[0]) + (int(user_rows[1]) * int(qty)))
                        update_store_wallet = (int(store_wallet[0]) - (int(user_rows[1]) * int(qty)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                        await ctx.send('{} has sold {} {}'.format(str(username), str(qty), str(item)))
                        connection.commit()
              else: #User still has some, update the store and deduct the users quantity
                   c.execute("UPDATE items SET quantity = ? WHERE item = ? and owner = ?;", (str(new_store_qty),str(item), target_store_name))
                   updated_user_wallet = (int(user_wallet[0]) + (int(user_rows[1]) * int(qty)))
                   update_store_wallet = (int(store_wallet[0]) - (int(user_rows[1]) * int(qty)))
                   c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                   c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                   connection.commit()
                   if not rows: #add the qty to the store
                        c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(user_rows[1]), target_store_name))
                        updated_user_wallet = (int(user_wallet[0]) + (int(user_rows[1]) * int(qty)))
                        update_store_wallet = (int(store_wallet[0]) - (int(user_rows[1]) * int(qty)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                        await ctx.send('{} has sold {} {}'.format(str(username), str(qty), str(item)))
                        connection.commit()
                   else:
                        new_user_qty = int(user_rows[0]) - int(qty)
                        c.execute("UPDATE items SET quantity = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(username), str(item)))
                        updated_user_wallet = (int(user_wallet[0]) + (int(user_rows[1]) * int(qty)))
                        update_store_wallet = (int(store_wallet[0]) - (int(user_rows[1]) * int(qty)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;",(str(updated_user_wallet), str(username)))
                        c.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(update_store_wallet), target_store_name))
                        await ctx.send('{} has sold {} {}'.format(str(username), str(qty), str(item)))
                        connection.commit()

#Gift an item to someone - it makes the item move, but no money changes hands.
@commands.command()
async def gift(ctx,user, item, qty = "1"):
     username = ctx.author.name
     person = user
     other_user = person
     c = connection.cursor()
     cursor = connection.cursor()
     owner_rows = cursor.execute("SELECT quantity, cost, owner FROM items WHERE owner = ? AND item = ?;", (str(username), str(item)),).fetchone()
     gift_rows = cursor.execute("SELECT quantity, cost, owner FROM items WHERE owner = ? AND item = ?;", (str(other_user), str(item)),).fetchall()
     character_rows = cursor.execute("SELECT name from character where user = ?;", (str(other_user),),).fetchone()
     if not character_rows:
         await ctx.send("That doesn't seem to be a person with a character.  You can only gift to people with a character setup.")
     else:
         if not owner_rows:  #did not find that item
              await ctx.send('You dont have that item.  Check your spelling, or choose a new item.')
         else:
              new_user_qty = int(owner_rows[0]) - int(qty)
              if new_user_qty < 0:  #You dont have enough of that item
                   await ctx.send("You don't have enough of that item.  Choose {} or fewer.".format(str(owner_rows[0])))
              elif new_user_qty == 0:  #need to delete the item from the user inventory - they have none left after selling
                   c.execute("DELETE FROM items WHERE item = ? and owner = ?;",(str(item),str(username),),)
                   connection.commit()
                   if not gift_rows: #add the item to the store with the qty argument
                        c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(owner_rows[1]), other_user))
                        await ctx.send('{} has gifted {} {} to {}'.format(str(username), str(qty), str(item), str(other_user)))
                        connection.commit()
                   else: #the item is already in the store and needs the qty updated
                        new_user_qty = int(owner_rows[0]) - int(qty)
                        c.execute("UPDATE items SET quantity = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(other_user), str(item)))
                        await ctx.send('{} has gifted {} {} to {}'.format(str(username), str(qty), str(item), str(other_user)))
                        connection.commit()
              else: #User still has some, update the store and deduct the users quantity
                   c.execute("UPDATE items SET quantity = ? WHERE item = ? and owner = ?;", (str(new_user_qty),str(item), str(username)))
                   connection.commit()
                   if not gift_rows: #add the qty to the store
                        c.execute("INSERT into items (item, quantity, cost, owner) values (?,?,?,?);", (str(item), str(qty), str(owner_rows[1]), other_user))
                        await ctx.send('{} has gifted {} {} to {}'.format(str(username), str(qty), str(item), str(other_user)))
                        connection.commit()
                   else:
                        new_user_qty = int(owner_rows[0]) - int(qty)
                        c.execute("UPDATE items SET quantity = ? WHERE owner = ? and item = ?;",(str(new_user_qty), str(username), str(item)))
                        await ctx.send('{} has gifted {} {} to {}'.format(str(username), str(qty), str(item), str(other_user)))
                        connection.commit()

#Delete an item from a user inventory
@commands.command()
@commands.has_permissions(administrator=True)
async def inventorydelete(ctx, user, item):
    person = user
    username = person
    c = connection.cursor()
    cursor = connection.cursor()
    rows = c.execute("SELECT quantity from items where owner = ? and item = ?;",(str(username),str(item),),).fetchone()
    if not rows:
        await ctx.send("I can't find that.  Check your spelling and try again.")
    else:
        cursor.execute("DELETE from ITEMS where owner = ? and item = ?;",(str(username), str(item),),)
        await ctx.send("You deleted {} from {}'s inventory.".format(str(item), str(username)))
        connection.commit()


def setup(client):
    # Every extension should have this function
    client.add_command(inventory)
    client.add_command(use)
    client.add_command(donate)
    client.add_command(equip)
    client.add_command(unequip)
    client.add_command(giveitem)
    client.add_command(wallet)
    client.add_command(bank)
    client.add_command(givemoney)
    client.add_command(buy)
    client.add_command(sell)
    client.add_command(gift)
    client.add_command(inventorydelete)
