import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='market!', intents=intents)

bot.remove_command('help')

try:
    with open('sellers.json', 'r') as file:
        current_sellers = json.load(file)
except FileNotFoundError:
    current_sellers = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name='Managing Stocks'))

@bot.command()
async def stock(ctx):
    sellers_list = "\n".join([f"{product}: {seller}" for product, seller in current_sellers.items()]) or "No current stock."
    embed = discord.Embed(title="Marketplace Stock", description=sellers_list, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx, *, item):
    seller = ctx.author.mention
    current_sellers[item] = seller
    with open('sellers.json', 'w') as file:
        json.dump(current_sellers, file)
    embed = discord.Embed(title="Product Added", description=f"Added '{item}' to the product list.", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def contact(ctx, seller_name):
    if seller_name in current_sellers:
        seller = current_sellers[seller_name]
        embed = discord.Embed(title=f"Contact {seller} for '{seller_name}'", color=discord.Color.orange())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"'{seller_name}' is not listed in the marketplace.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age=86400)
    embed = discord.Embed(title="Invite the Bot", description=f"[Click here to invite the bot to your server]({link})", color=discord.Color.purple())
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Marketplace Bot Help", color=discord.Color.blue())
    embed.add_field(name="Commands:", value="market!stock\nmarket!add <item>\nmarket!contact <seller_name>\nmarket!invite", inline=False)
    embed.add_field(name="Usage:", value="Use `market!command` to execute a command.", inline=False)
    embed.set_footer(text="For more info, type market!help <command>.")
    await ctx.send(embed=embed)

bot.run(YOUR TOKEN)
