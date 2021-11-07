import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3
connection = sqlite3.connect("RPBot.db")

#Admin give a user money
@commands.command()
@commands.has_permissions(administrator=True)
async def givecash(ctx, user, amt):
     person = user
     username = person
     c = connection.cursor()
     cursor = connection.cursor()
     #if doesn't have the item, make a new line.  If they have some, add more to the qty
     rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;", (str(username),),).fetchone()
     if not rows:
          cursor.execute("INSERT into wallet (balance, user) values (?, ?)", (str(amt),str(username)))
          await ctx.send('You gave {} {} coins'.format(user, str(amt)))
          connection.commit()
     else:      #There's a match - add the quantity to the existing quantity
          for a in rows:
               new_amount = int(amt) +int(rows[0])
               cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_amount), str(username)))
               await ctx.send("you gave {} {} coins.  Updated balance is {} coins.".format(user,str(amt), str(new_amount)))
               connection.commit()
     connection.commit()


#sets store wallet balance
@commands.command()
@commands.has_permissions(administrator=True)
async def setstorecash(ctx,amt):
     username = "Store"
     c = connection.cursor()
     cursor = connection.cursor()
     rows = cursor.execute("SELECT balance FROM wallet WHERE user = ?;", (str(username),),).fetchone()
     if not rows:
          cursor.execute("INSERT into WALLET (balance, user) values (?, ?);", (str(amt), str(username)))
          connection.commit()
          await ctx.send("Store balance is now: {}".format(str(amt)))
     else:
          cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(amt), str(username)))
          await ctx.send("Store balance is now: {}".format(str(amt)))

#Set maximum  cash with cashmax
@commands.command()
@commands.has_permissions(administrator=True)
async def cashmax(ctx, amt):
    c = connection.cursor()
    cursor = connection.cursor()
    cursor.execute("UPDATE globalvariables SET variable = ? WHERE purpose = 'maxcash';", (str(amt),))
    connection.commit()
    await ctx.send("Maximum user cash has been set to {} coins.".format(str(amt)))


#Designate channel names for comment payments
@commands.command()
@commands.has_permissions(administrator=True)
async def paidchannel(ctx,*, arg):
    c = connection.cursor()
    cursor = connection.cursor()
    cursor.execute("insert into channels (channel) values (?)", (str(arg),))
    connection.commit()
    await ctx.send("Updated paid channel list with {}".format(str(arg),))

#Removes a paid channel from the list
@commands.command()
@commands.has_permissions(administrator=True)
async def removepaidchannel(ctx,*, arg):
    c = connection.cursor()
    cursor = connection.cursor()
    rows = cursor.execute("SELECT channel FROM channels WHERE channel = ?;", (str(arg),),).fetchone()
    if not rows:
        await ctx.send("That's not a current channel that is in the Paid Channel list.  Try again.")
    else:
        cursor.execute("DELETE from channels where channel = ?;",(str(arg),),)
        await ctx.send("Deleted {} from the list of paid channels.".format(str(arg)))
        connection.commit()

#!setpayment sets the payment amount per message in the designated Channels
@commands.command()
@commands.has_permissions(administrator=True)
async def setpayment(ctx, amt):
    c = connection.cursor()
    cursor = connection.cursor()
    cursor.execute("UPDATE globalvariables SET variable = ? WHERE purpose = 'payment';", (str(amt),))
    connection.commit()
    await ctx.send("Updated paid channel payment to {} coins per message.".format(str(amt),))


#Set the tax rate per @bot.event
@commands.command()
@commands.has_permissions(administrator=True)
async def settaxes(ctx, amt):
    c = connection.cursor()
    cursor = connection.cursor()
    cursor.execute("UPDATE globalvariables SET variable = ? WHERE purpose = 'taxes';", (str(amt),))
    connection.commit()
    await ctx.send("Updated tax payment to {} coins.".format(str(amt),))


#tax people the rate set by the tax amount - give the money to the Treasury.  Do not go below $0 for users.
@commands.command()
@commands.has_permissions(administrator=True)
async def tax(ctx):
    c = connection.cursor()
    cursor = connection.cursor()
    taxsetting = cursor.execute("Select variable FROM globalvariables WHERE purpose = 'taxes'").fetchone()
    rows = cursor.execute("Select balance, user from wallet").fetchall()
    old_treasury_balance = cursor.execute("select balance from wallet where user = 'Treasury'").fetchone()
    tax_take = 0
    target_treasury_name = "Treasury"
    for a,b in rows:  # for all of the users with a wallet, deduce the amount up to zero
        if b != 'Store' and  b != 'Treasury':
            new_amount = int(a) - int(taxsetting[0])
            if new_amount >= 0:
                cursor.execute("Update wallet SET balance = ? Where user = ?;", (str(new_amount), str(b)))
                tax_take += 1
                connection.commit()
            else:
                cursor.execute("Update wallet SET balance = '0' Where user = ?;",(str(b),))
    new_treasury_add = int(taxsetting[0]) * tax_take
    new_treasury_balance = new_treasury_add + int(old_treasury_balance[0])
    cursor.execute("Update wallet SET balance = ? WHERE user = ?", (str(new_treasury_balance), str(target_treasury_name)))
    connection.commit()
    await ctx.send("Tax day came!  Everyone donated (except those without any money...You know who you are...)")


#spend money from the treasury - makes it disappear forever.
@commands.command()
@commands.has_permissions(administrator=True)
async def spendtreasury(ctx, arg):
    c=connection.cursor()
    cursor = connection.cursor()
    target_treasury_name = "Treasury"
    treasury = cursor.execute("SELECT balance FROM wallet WHERE user = ?;",(target_treasury_name,),).fetchone()
    current_value = int(treasury[0])
    new_value = current_value - int(arg)
    cursor.execute("Update wallet SET balance = ? WHERE user = ?", (str(new_value), str(target_treasury_name)))
    connection.commit()
    await ctx.send("You spent {} coins from the Treasury.  New Balance is: {} coins.".format(str(arg),str(new_value)))



def setup(client):
    # Every extension should have this function
    client.add_command(givecash)
    client.add_command(setstorecash)
    client.add_command(tax)
    client.add_command(settaxes)
    client.add_command(setpayment)
    client.add_command(removepaidchannel)
    client.add_command(paidchannel)
    client.add_command(cashmax)
    client.add_command(spendtreasury)
