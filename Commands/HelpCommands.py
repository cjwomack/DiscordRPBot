import discord, random, sys, time, os #import all of the libraries needed
from discord.ext import commands #imports the commands from the Discord ext
#Help and other menus:

#Embeded help with list and details of available commands

@commands.command(pass_context=True)
async def help(ctx):
     embed = discord.Embed(colour =discord.Colour.purple())
     embed.set_author(name='Welcome to RPBot : See below for the list of available commands...')
     file = discord.File("Commands/Assets/questionmark.png", filename="questionmark.png")
     embed.set_thumbnail(url="attachment://questionmark.png")
     embed.add_field(name='!roll [multiplier]d[dice sides] [+modifer]', value = 'Rolls a dice of user specified sides.  e.g. !roll 2d20 to roll 2 d20 or !roll d20 +5 for a single d20 plus 5.  Multiplier is limited to 9.', inline = False)
     embed.add_field(name='!magic8',value = 'RPBot will shake a magic 8 ball and tell you the response.', inline = False)
     embed.add_field(name='!store', value = 'Shows the store inventory.', inline = False)
     embed.add_field(name='!buy [item] [qty]', value = 'Buy an item from the store. Qty defaults to 1 if left blank.', inline = False)
     embed.add_field(name='!sell [item] [qty]', value = 'Sell an item to the store from your inventory. Qty defaults to 1 if left blank.', inline = False)
     embed.add_field(name='!use [item] [qty]', value = 'Use an item from your inventory. Qty defaults to 1 if left blank.', inline = False)
     embed.add_field(name='!equip [item]', value = 'Equip an item from your inventory.', inline = False)
     embed.add_field(name='!unequip [item]', value = 'Move an equipped item back to your inventory.', inline = False)
     embed.add_field(name='!gift [username] [item] [qty]', value = 'Gift an item to someone.  No money changes hands. Qty defaults to 1 if left blank.', inline = False)
     embed.add_field(name='!donate [amount]', value = 'Donate to the treasury.', inline = False)
     embed.add_field(name='!create [name]', value = 'Creates a new character.', inline = False)
     embed.add_field(name='!stats [username]', value = 'Shows the character sheet for a user.  !stats with no username will show your own stats.', inline = False)
     embed.add_field(name='!inventory [username]', value = 'Shows the user inventory.  !inventory with no username will show your own inventory', inline = False)
     embed.add_field(name='!wallet', value = 'Shows the user wallet balance.', inline = False)
     embed.add_field(name='!givemoney [user] [amount]', value = 'Give some of your money to the user named.', inline = False)
     embed.add_field(name='!editname [old name] [new name]', value = 'Edit the name of an existing character.  e.g !editname Joe Hank', inline = False)
     embed.add_field(name='!help_character', value = 'A list of Admin commands for character management.', inline = False)
     embed.add_field(name='!help_admin',value = 'For Admin specific commands.', inline = False)
     await ctx.send(file=file,embed=embed)

#help menu for the inventory/store options
@commands.command()
async def help_admin(ctx):
     embed = discord.Embed(colour = discord.Colour.purple())
     embed.set_author(name='See below for the list of available Admin commands...')
     file = discord.File("Commands/Assets/questionmark.png", filename="questionmark.png")
     embed.set_thumbnail(url="attachment://questionmark.png")
     embed.add_field(name='!help_character', value = 'A list of Admin commands for character management.', inline = False)
     embed.add_field(name='!addmagic8', value = 'Admin Function - Add new options to the magic 8 ball.', inline = False)
     embed.add_field(name='!viewmagic8', value = 'Admin Function - Returns a list of all magic 8 ball responses.  The index is used for deletion.', inline = False)
     embed.add_field(name='!deletemagic8 [index]', value = 'Admin Function - Deletes a line from the magic 8 ball responses.  Use the !viewmagic8 command for the index.', inline = False)
     embed.add_field(name='!storeadd [item] [qty] [cost]', value = 'Admin Function - add items to the store.  e.g. !storeadd shovel 10 40.', inline = False)
     embed.add_field(name='!giveitem [user] [item] [qty] [value]', value = 'Admin Function - Give an item to the specified user.  e.g. !give user hammer 1 100', inline = False)
     embed.add_field(name='!edititem [item] [new item] [new qty] [new cost]', value = 'Admin Function - Updates the item when given new values.', inline = False)
     embed.add_field(name='!deleteitem [item]', value = 'Admin Function - Displays every users wallet balance', inline = False)
     embed.add_field(name='!inventorydelete [user] [item]', value = 'Admin Function - Deletes an item from a users inventory', inline = False)
     embed.add_field(name='!tax', value = 'Admin Function - Taxes all users the amount set by !settaxes.  Money goes to the treasury.', inline = False)
     embed.add_field(name='!bank', value = 'Admin Function - Displays every users wallet balance', inline = False)
     embed.add_field(name='!spendtreasury', value = 'Admin Function - Allows Admin to spend money from the treasury.  This can go negative.', inline = False)
     embed.add_field(name='!setstorecash [amount]', value = 'Admin Function - Set the store balance.', inline = False)
     embed.add_field(name='!cashtoggle', value = 'Admin Function - Toggle on or off the ability for users to use the !givemoney function. Default is On.', inline = False)
     embed.add_field(name='!givecash [user] [amount]', value = "Admin Function - Give a user some money.", inline = False)
     embed.add_field(name='!cashmax [amount]', value = 'Admin Function - sets the maximum amount of cash a user can have before comment payments stop.', inline = False)
     embed.add_field(name='!setpayment', value = 'Admin Function - Set the amount that each comment in designated channels gets paid. Default value is 0.', inline = False)
     embed.add_field(name='!paidchannel [channel ID]', value = 'Admin Function - Add the ID of a channel to the list that pay money for commenting.', inline = False)
     embed.add_field(name='!removepaidchannel [channel ID]', value = 'Admin Function - Remove the ID of a channel from the paid channel list.', inline = False)
     embed.add_field(name='!settaxes [amount]', value = 'Admin Function - Set the amount of taxes charged per day.  Taxes go to the Treasury. Default value is 0.', inline = False)
     embed.add_field(name='!ping', value = 'Any User - Returns bot response time in milliseconds.', inline = False)
     embed.add_field(name='!server', value = 'Any User - Displays server stats.', inline = False)
     embed.add_field(name='!goaway', value = 'Admin Function - Turns off the bot.', inline = False)
     await ctx.send(file=file,embed=embed)

#help menu for administrating characters
@commands.command()
async def help_character(ctx):
     embed = discord.Embed(colour = discord.Colour.purple())
     embed.set_author(name='See below for the list of available Admin commands...')
     ffile = discord.File("Commands/Assets/questionmark.png", filename="questionmark.png")
     embed.set_thumbnail(url="attachment://questionmark.png")
     embed.add_field(name='!strength [user] [new value]', value = 'Admin Function - updates the str value with a new one.', inline = False)
     embed.add_field(name='!dexterity [user] [new value]', value = 'Admin Function - updates the dex value with a new one.', inline = False)
     embed.add_field(name='!constitution [user] [new value]', value = 'Admin Function - updates the con value with a new one.', inline = False)
     embed.add_field(name='!intelligence [user] [new value]', value = 'Admin Function - updates the int value with a new one.', inline = False)
     embed.add_field(name='!willpower [user] [new value]', value = 'Admin Function - updates the will value with a new one.', inline = False)
     embed.add_field(name='!charisma [user] [new value]', value = 'Admin Function - updates the char value with a new one.', inline = False)
     embed.add_field(name='!health [user] [new value]', value = 'Admin Function - updates the health value with a new one.', inline = False)
     embed.add_field(name='!mana [user] [new value]', value = 'Admin Function - updates the mana value with a new one.', inline = False)
     await ctx.send(file=file,embed=embed)


def setup(client):
    # Every extension should have this function
    client.add_command(help)
    client.add_command(help_admin)
    client.add_command(help_character)
