# Create a discord bot that at 12 PM everyday it resets and then generates one coin for a user.
# The user can then use that coin to buy something from the store.
#The store will have a list of items that the user can buy.
#To do:
# 1. add a timer for the generate coins
# 2. Add a Marketplace 
# 3. Add way to buy items from the marketplace
#  4. Add a way to add new items to marketplace from in the bot
# 5. Maybe hook up a sql database to store the items and the users coins 
# 6. when you buy from the store. You can use a command to show a little image of what you bought in a menu/ inventory
# 7. Add a way for people to give each other coins
# 8. Add a way to gamble coins
# This bot is essentially a system for an inside joke in a discord server that I was in.
#There is no use case for this bot, it is quite literally a joke bot.



#imports 
import discord
from  discord.ext import commands, tasks
import random
import asyncio
import sqlite3



#

intents = discord.Intents.default()
intents.message_content= True

bot = commands.Bot(command_prefix='!', intents=intents)


#Database connection
db_file_path = 'D:\\File\\Test.db'









user_coins = {}

store_items = {
    'Soul-less Ginger Fairy': 10,
    'Cat Band': 15,
    'Fairy Dust': 5,

}

@bot.event 
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def register(ctx):
    user_id = ctx.author.id
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE discord_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()

    if result:
        await ctx.send("You are already registered!")
        return
    

    await ctx.send("Please Provide your selected username:")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        username_message = await bot.wait_for('message', timeout=30.0, check=check)
        username = username_message.content
        # store data in sqlite
        connection = sqlite3.connect(db_file_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (discord_id, username, balance) VALUES (?, ?, ?)", (ctx.author.id, username, 0))
        connection.commit()
        connection.close()

        await ctx.send(f"Thank you {username}! You have been registered.")
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
    


#Generate Coins for all users
@bot.command()
async def gen(ctx):
    user_id = str(ctx.author.id)

    #get user's username from the database
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE discord_id = ?", (ctx.author.id,))
    result = cursor.fetchone()

    if result:
        username = result[0]
    else: 
        username = ctx.author.name
        print("User not found, using the discord username instead.")
    



    if user_id not in user_coins:
        user_coins[user_id] = 0
    
    user_coins[user_id] += 1
    await ctx.send(f"Hello {username}! Generating Cat Coin: Please Wait...")
    #Delay to represent coin generation
    await asyncio.sleep(2)


    await ctx.send(f" Hello {username}! Your new Balance is " + str(user_coins[user_id]) + " Cat Coins!")
    await ctx.send("Generating Cat Coin: Done!")
    
    cursor.execute("UPDATE users SET balance = ? WHERE discord_id = ?", (user_coins[user_id], ctx.author.id))
    connection.commit()
    connection.close()


    

@tasks.loop(hours=24)
async def daily_reset():
    gen()

@bot.command()
async def bal(ctx):
    user_id = str(ctx.author.id)

    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE discord_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        discord_id , username, balance = result
    else: 
        username = ctx.author.name
        balance = 0
    if user_id not in user_coins:
        user_coins[user_id] = 0

    await ctx.send(f'Hello {username}! You have {user_coins[user_id]} coins!')
    connection.commit()
    connection.close()


# @bot.command()
# async def end(ctx):
#     bot.close()


# @bot.command()

# async def store(ctx):
#     store_list = "\n".join([f"{item}: {price}" for item, price in store_items.items()])
#     await ctx.send("Welcome to the Cat Coin Store!\n\nAvailable Items:\n" + store_list)



#Work In Progresss buy command
# @bot.command()
# async def buy(ctx, item):
#     user_id = str(ctx.author.id)
#     if user_id not in user_coins:
#         user_coins[user_id] = 0
#     if item not in store_items:
#         await ctx.send("That item is not in the store!")
#         return
#     if user_coins[user_id] < store_items[item]:
#         await ctx.send("You do not have enough coins to buy that!")
#         return
#     user_coins[user_id] -= store_items[item]
#     await ctx.send("You have bought " + item + "!")
#     await ctx.send("Your new balance is " + str(user_coins[user_id]) + " Cat Coins!")



    #Create a bot command where users can gamble their coins.
    #The bot command will have levels with varying chances of winning and a multiplier for the cashout/
    #Level 1 is 80% for a 1.1x multiplier
    #Level 2 is 50% for a 1.5x multiplier
    #Level 3 is 30% for a 2x multiplier
    #Level 4 is 20% for a 3x multiplier
    #Level 5 is 10% for a 5x multiplier
    #Level 6 is 5% for a 10x multiplier
    #Level 7 is 0.5% for a 20x multiplier
    #Level 8 is 0.1% for a 50x multiplier
    #Level 9 is 0.01% for a 100x multiplier


@bot.command()
async def gamble(ctx, level: int, amount: int):
    user_id = str(ctx.author.id)
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE discord_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        user_coins = result[0]
    else:
        user_coins = 0
        await ctx.send("You don't have enough coins to gamble.")
        connection.close()
        return
    if user_id not in user_coins:
        await ctx.send("You don't have any coins to gamble.")
        return
    if amount <=0 or amount > user_coins[user_id]:
        await ctx.send("Invalid amount to gamble.")
        return
    levels = {
        1: {'chance': 80, 'multiplier': 1.1},
        2: {'chance': 50, 'multiplier': 1.5},
        3: {'chance': 30, 'multiplier': 2},
        4: {'chance': 20, 'multiplier': 3},
        5: {'chance': 10, 'multiplier': 5},
        6: {'chance': 5, 'multiplier': 10},
        7: {'chance': 0.5, 'multiplier': 20},
        8: {'chance': 0.1, 'multiplier': 50},
        9: {'chance': 0.01, 'multiplier': 100}
        }
    
    #Work In progress:
    # embed = discord.Embed(title="Select a Gambling Level", description="Please select a level to gamble on.", color=0xeee657)
    # for level, info in levels.items():
    #     embed.add_field(name=f"Level {level}", value=f"Winning Chance: {info['chance']}%, Multiplier: {info['multiplier']}x", inline=False)
    #     await ctx.send(embed=embed)
    await ctx.send("Please select the level that you want to gamble on (1-9):")

    if level not in levels:
        await ctx.send("Invalid level to gamble.")
        return 
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() 

    await ctx.send("Please select the level that you want to gamble on (1-9:")
    try:
        level_message = await ctx.bot.wait_for('message', check=check, timeout=30.0)
        selected_level = int(level_message.content)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
        return
        
    await ctx.send("Please select the amount you want to gamble?")
    try:
        amount_message = await ctx.bot.wait_for('message', check=check, timeout=30.0)
        selected_amount = int(amount_message.content)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
        return


    winning_chance, multiplier = levels[selected_level]
    result = random.randint(1, 1000)

    if result <= winning_chance:
        winnings = int(selected_amount * multiplier)
        user_coins[user_id] += winnings
        await ctx.send(f"Congratulations! You won {winnings} coins!")
    else:
        user_coins[user_id] -= selected_amount
        await ctx.send("Sorry, you lost the gamble. Good luck next time kid.")







bot.run('')
