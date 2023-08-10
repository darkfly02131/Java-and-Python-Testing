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
    

#Q: buddy c what am I doing wrong
#Q: and how is it that I'm not using it?
#Q: I am calling it through the connection
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
        disord_id , username, balance = result
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



#Create a bot command that will allow a user to buy something from the store.
#Q: Ho
@bot.command()
async def buy(ctx, item):
    user_id = str(ctx.author.id)
    if user_id not in user_coins:
        user_coins[user_id] = 0
    if item not in store_items:
        await ctx.send("That item is not in the store!")
        return
    if user_coins[user_id] < store_items[item]:
        await ctx.send("You do not have enough coins to buy that!")
        return
    user_coins[user_id] -= store_items[item]
    await ctx.send("You have bought " + item + "!")
    await ctx.send("Your new balance is " + str(user_coins[user_id]) + " Cat Coins!")



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


    # @bot.command(ctx)
    # async def gamblin(ctx, level: int, amount: int):
    #     user_id = str(ctx.author.id)
    #     if user_id not in user_coins:
    #         await ctx.send("You don't have any coins to gamble.")
    #         return
    #     if amount <=0 or amount > user_coins[user_id]:
    #         await ctx.send("Invalid amount to gamble.")
    #         return
        
    #     levels = {
    #         1: {80, 1.1},
    #         2: {50, 1.5},
    #         3: {30, 2},
    #         4: {20, 3},
    #         5: {10, 5},
    #         6: {5, 10},
    #         7: {0.5, 20},
    #         8: {0.1, 50},
    #         9: {0.01, 100}
    #     }

    #     await ctx.send("Please select he level that you want to gamble on (1-9) and the amount of coins that you want to gamble.")

    #     def  check(m):
    #         return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= 9


    #     if level not in levels:
    #         await ctx.send("Invalid level to gamble.")
    #         return 
        

    #     try:
    #         level_message = await ctx.bot.wait_for('message', check=check, timeout=30.0)
    #         selected_level = int(level_message.content)
    #     except asyncio.TimeoutError:
    #         await ctx.send("You took too long to respond.")
    #         return
        
    #     winning_chance, multiplier = levels[level]

    #     if random.randint(1, 1000) <= winning_chance * 100:
    #         winnings = int(amount * multiplier)
    #         user_coins[user_id] += winnings
    #         await ctx.send(f"Congratulations!!! You won {winnings} coins! Your new balance is {user_coins[user_id]} coins!")
    #     else:
    #         user_coins[user_id] -= amount
    #         await ctx.send(f"Sorry, you lost {amount} coins. Your new balance is {user_coins[user_id]} coins!")

    
       
@bot.command()

async def womp(ctx):
    while True:
        await ctx.send("Womp Womp")
        await asyncio.sleep(5)
        break    

    
@bot.command()

async def gif(ctx):
    gif_url = 'https://media.tenor.com/34qt8w3xnHEAAAAd/angy-angry.gif'
    await ctx.send(discord.File(gif_url))




bot.run('MTEzNzg4MzY1MzQ0ODQwMTA1Nw.GydjoK.9PczQvn-DvsQFiAxtg-ZRetiR7gqTmrFtkY8Rc')
