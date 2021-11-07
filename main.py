#This program communicates with the Discord API and runs a bot that assists in Dungeons and Dragons or Roleplay gameplay.

#Imports:

import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
import sqlite3

#__________________________________________________________________________________________________________________________________
#Bot Setup Stuff:

print('Starting Bot...')

#Reads the authorization token for the Discord Bot
TOKEN = open("token.txt","r").readline()

#Command Prefix
client = commands.Bot(command_prefix = '!')    #sets the prefix for entering commands as a '!'

#Delete the default Help command before replacing with a new one
client.remove_command('help')


#setup the item database - create it if it doesn't exist and setup the table, or connect to it if it does exist
connection = sqlite3.connect("RPBot.db")
if os.path.isfile('RPBot.db'):
     print('RPBot.db already exists')
else:
     cursor = connection.cursor()
     cursor.execute("CREATE TABLE items (item, quantity, cost, owner)")
     cursor.execute("CREATE Table character (name, age, height, weight, race, class, health, mana, str, dex, will, int, char, con, user, url)")
     cursor.execute("CREATE TABLE wallet (balance, user)")
     cursor.execute("CREATE TABLE globalvariables (purpose, variable)")
     cursor.execute("CREATE TABLE channels (channel)")
     cursor.execute("CREATE TABLE equipment (item, user, cost)")
     cursor.execute("INSERT into wallet (balance, user) values ('0', 'Store');")
     cursor.execute("INSERT into wallet (balance, user) values ('0', 'Treasury');")
     cursor.execute("INSERT into globalvariables (purpose, variable) values ('cashtoggle', 'On');")
     cursor.execute("INSERT into globalvariables (purpose, variable) values ('maxcash', '100000000');")
     cursor.execute("INSERT into globalvariables (purpose, variable) values ('taxes', '0');")
     cursor.execute("INSERT into globalvariables (purpose, variable) values ('payment', '0');")
     connection.commit()
     print(connection.total_changes)

#____________________________________________________________________________________________________________________________________

client.load_extension("Commands.HelpCommands")
client.load_extension("Commands.EconomyCommands")
client.load_extension("Commands.ServerCommands")
client.load_extension("Commands.StoreCommands")
client.load_extension("Commands.Dice")
client.load_extension("Commands.Magic8Commands")
client.load_extension("Commands.CharacterCommands")
client.load_extension("Commands.InventoryCommands")

#_________________________________________________________________________________________________________________________________________
@client.event
async def on_message(message):
    participant = str(message.author.name)
    this_channel = "('"+str(message.channel.id)+"',)"
    c = connection.cursor()
    cursor = connection.cursor()
    result = cursor.execute("SELECT channel from channels")
    rows = result.fetchall()
    user_wallet = cursor.execute("SELECT balance FROM wallet WHERE user = ?;", (str(participant),),).fetchone()
    payment_amt = cursor.execute("SELECT variable from globalvariables WHERE purpose = 'payment';").fetchone()
    max_amt = cursor.execute("SELECT variable from globalvariables WHERE purpose = 'maxcash'").fetchone()
    max_cash = int(max_amt[0])
    if participant == "RPBot":
        return
    else:
        for row in rows:
            if this_channel == str(row):    #if the message was in one of the specified channels
                 if not user_wallet:  #if they don't have a wallet entry already, set them up and give them the money
                      added_amt = payment_amt[0]
                      cursor.execute("INSERT into wallet (balance, user) values (?, ?)", (str(added_amt),str(participant)))
                      connection.commit()
                 else:      #There's a match - add the quantity to the existing quantity, also check that cashmax isn't exceeded.
                      for a in user_wallet:
                          added_amt = payment_amt[0]
                          new_amount = int(added_amt) +int(user_wallet[0])
                          if new_amount < max_cash:
                               cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(new_amount), str(participant)))
                               connection.commit()
                          else:
                               cursor.execute("UPDATE wallet SET balance = ? WHERE user = ?;", (str(max_cash), str(participant)))
                               connection.commit()

    await client.process_commands(message)


#Error Checking or Messages:

#If there is an error, answers with an error message
@client.event
async def on_command_error(ctx,error):
     await ctx.send(f'Error. Try using !help for valid commands. ({error})')

#answers with the ms latency
@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! {round (client.latency*1000)}ms ')

print('Bot is ready!')
print('Beep Beep Boop!')
client.run(TOKEN)
