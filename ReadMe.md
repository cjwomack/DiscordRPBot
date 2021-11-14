# Introduction and getting started

## **Welcome to RPBot**

This is a Discord bot for assisting in managing roleplaying/ DnD servers, written in Python 3.8 using the Discord API.

It is intentionally simple and meant to assist Discord driven Roleplaying games, without attempting to do too much. It is intended to be self-hosted with a single instance.

**Dependencies:**

* Discord.py
* sqlite3


Update token.txt by pasting your discord bot token into the first line.


The primary functions include:
* An economy system
  - User currency tracking
  - Item store
  - Item inventories
  - Purchasing, selling, using and trading of items
  - Payments for participating in specified servers
* A dice rolling system
* Basic Character stat tracking
* A "Magic 8 Ball" randomized function with Admin controlled responses
* Server Admin functions


# Command List

  All commands use the ! prefix by default.  Arguments are shown with brackets [].  Do not include the bracket in your commands.

  Note:  You can issue commands to RPBot via DM if you don't wish users to see a command, or want to keep the main chat


## **Help Commands:**

* help
      Shows a help screen with a listing of commands.

* help_admin
      Shows a help screen with a listing of Admin and server commands.

* help_character
      Shows a help screen with character related commands.

## **Chance Commands:**

* roll [multiplier]d[dice sides][+modifer]

      Rolls a dice of user specified sides.  
      e.g. !roll 2d20 to roll 2 d20 or !roll d20 for a single d20 or !roll 2d20+6 for adding 6 to each roll.
      Multiplier is limited to 9.

* magic8

      RPBot will shake a magic 8 ball and tell you the response.


## **Character Commands:**

* create [name]

      Creates a new character, then guides you through the next steps.
      It may be best to do this in a private message to avoid spamming.

* stats [username]

      Shows the character sheet for a user.  stats command with no username will show your own stats.

* editname [old name] [new name]

      Edit the name of an existing character.  e.g !editname Joe Hank will change the name of Joe to Hank.

## **Items, Inventory, and Wallet Commands:**

* inventory [username]

      Shows the user inventory.  Admin can view any inventory, users can only view their own.

* wallet

      Shows the user wallet balance.

* store

      Shows the store inventory.

* buy [item] [qty]

      Buy an item from the store. Qty defaults to 1 if left blank.

* sell [item] [qty]

      Sell an item to the store from your inventory. Qty defaults to 1 if left blank.

* use [item] [qty]

      Use an item from your inventory. Qty defaults to 1 if left blank.

* gift [username] [item] [qty]

      Gift an item to someone.  No money changes hands. Qty defaults to 1 if left blank.

* givemoney [user] [amount]

      Give some of your money to the user named.

* equip [item]

      Equip an item from your inventory.

* Unequip [item]

      Unequip an item from your inventory.

## **Admin Commands:**

* addmagic8

      Admin Function - Add new options to the magic 8 ball.

* storeadd [item] [qty] [cost]

      Admin Function - add items to the store.  e.g. !storeadd shovel 10 40.

* giveitem [user] [item] [qty] [value]

      Admin Function - Give an item to the specified user.  e.g. !give user hammer 1 100

* edititem [item] [new item] [new qty] [new cost]

      Admin Function - Updates the item when given new values.

* deleteitem [item]

      Admin Function - Displays every users wallet balance.

* bank

      Admin Function - Displays every users wallet balance.

* setstorecash [amount]
      Admin Function - Set the store balance.

* cashtoggle

      Admin Function - Toggle on or off the ability for users to use the !givemoney function.

* givecash [user] [amount]

      Admin Function - Give a user some money.

* cashmax

      Admin Function - sets the maximum amount of cash a user can have before comment payments stop.

* setpayment

      Admin Function - Set the amount that each comment in designated channels gets paid.

* paidchannel

      Admin Function - Add the name of a channel to the list that pay money for commenting.


## **Admin Character Commands:**

* strength [user] [new value]

      Admin Function - updates the str value with a new one.

* dexterity [user] [new value]

      Admin Function - updates the dex value with a new one.

* constitution [user] [new value]

      Admin Function - updates the con value with a new one.

* intelligence [user] [new value]

      Admin Function - updates the int value with a new one.

* willpower [user] [new value]

      Admin Function - updates the will value with a new one.

* charisma [user] [new value]

      Admin Function - updates the char value with a new one.

* health [user] [new value]

      Admin Function - updates the health value with a new one.

* mana [user] [new value]

      Admin Function - updates the mana value with a new one.


## **Server Commands:**

* ping

      Any User - returns bot response time in milliseconds.

* server

      Any User - returns server stats and values for maximum cash, chat payment amount, and tax amount.

* goaway

      Admin Function - Shuts down the bot.
__________________________________________________________________
